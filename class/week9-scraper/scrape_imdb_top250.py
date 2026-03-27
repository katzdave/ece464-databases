# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "playwright",
# ]
# ///

import asyncio
import csv
import re
from playwright.async_api import async_playwright


async def scrape_movie_details(context, title_url):
    """Visit a movie's detail page and fullcredits page to get director, producer, and runtime."""
    page = await context.new_page()
    await page.route("**/*.{png,jpg,jpeg,gif,svg,ico,woff,woff2}", lambda route: route.abort())
    await page.route("**/ads/**", lambda route: route.abort())
    await page.route("**/tracking/**", lambda route: route.abort())

    director = []
    producers = []
    runtime = ""

    # --- Movie detail page: get director + runtime ---
    try:
        await page.goto(title_url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_selector('li[data-testid="title-pc-principal-credit"]', timeout=15000)

        detail = await page.evaluate("""
            () => {
                // Director(s)
                const credits = document.querySelectorAll('li[data-testid="title-pc-principal-credit"]');
                let director = [];
                for (const c of credits) {
                    const label = c.querySelector('span, a.ipc-metadata-list-item__label');
                    if (label && (label.textContent.trim() === 'Director' || label.textContent.trim() === 'Directors')) {
                        director = Array.from(
                            c.querySelectorAll('a.ipc-metadata-list-item__list-content-item--link')
                        ).map(a => a.textContent.trim());
                        break;
                    }
                }

                // Runtime
                const rtEl = document.querySelector(
                    'li[data-testid="title-techspec_runtime"] .ipc-metadata-list-item__content-container'
                );
                const runtime = rtEl ? rtEl.textContent.trim() : '';

                return { director, runtime };
            }
        """)
        director = detail["director"]
        runtime = detail["runtime"]
    except Exception as e:
        print(f"    Warning: could not get details from {title_url}: {e}")

    # --- Full credits page: get producers ---
    credits_url = title_url.split("?")[0].rstrip("/") + "/fullcredits/"
    try:
        await page.goto(credits_url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_selector("section.ipc-page-section", timeout=15000)

        producers = await page.evaluate("""
            () => {
                const sections = document.querySelectorAll('section.ipc-page-section');
                for (const section of sections) {
                    const heading = section.querySelector('h3');
                    if (heading && heading.textContent.trim() === 'Producers') {
                        const links = section.querySelectorAll('a[href*="/name/"]');
                        return [...new Set(Array.from(links).map(a => a.textContent.trim()))];
                    }
                }
                return [];
            }
        """)
    except Exception as e:
        print(f"    Warning: could not get producers from {credits_url}: {e}")

    await page.close()

    # Clean runtime: "2h 22m(142 min)" -> "2h 22m"
    runtime_clean = re.sub(r"\(.*?\)", "", runtime).strip()

    return {
        "director": "; ".join(director),
        "producers": "; ".join(producers),
        "runtime": runtime_clean,
    }


async def scrape_imdb_top250():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            ),
        )

        # --- Step 1: Scrape the Top 250 list page ---
        list_page = await context.new_page()
        await list_page.route("**/*.{png,jpg,jpeg,gif,svg,ico,woff,woff2}", lambda route: route.abort())
        await list_page.route("**/ads/**", lambda route: route.abort())
        await list_page.route("**/tracking/**", lambda route: route.abort())

        await list_page.goto(
            "https://www.imdb.com/chart/top/", wait_until="domcontentloaded", timeout=60000
        )
        await list_page.wait_for_selector("li.ipc-metadata-list-summary-item", timeout=30000)

        # Scroll to load all 250 movies (lazy-loaded)
        prev_count = 0
        for _ in range(50):
            count = await list_page.evaluate(
                "document.querySelectorAll('li.ipc-metadata-list-summary-item').length"
            )
            if count >= 250:
                break
            if count == prev_count:
                await list_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(0.5)
            prev_count = count
            await list_page.evaluate("window.scrollBy(0, 2000)")
            await asyncio.sleep(0.3)

        movies = await list_page.evaluate("""
            () => {
                const items = document.querySelectorAll('li.ipc-metadata-list-summary-item');
                return Array.from(items).map((item, index) => {
                    const titleEl = item.querySelector('h3.ipc-title__text');
                    const ratingEl = item.querySelector('span.ipc-rating-star--imdb');
                    const metadataSpans = item.querySelectorAll('span.cli-title-metadata-item');
                    const link = item.querySelector('a.ipc-title-link-wrapper');

                    return {
                        rank: index + 1,
                        title: titleEl ? titleEl.textContent.trim() : '',
                        rating: ratingEl ? ratingEl.textContent.trim() : '',
                        year: metadataSpans.length > 0 ? metadataSpans[0].textContent.trim() : '',
                        url: link ? link.href : '',
                    };
                });
            }
        """)
        await list_page.close()
        print(f"Found {len(movies)} movies on the Top 250 list.\n")

        # --- Step 2: Visit each movie page for director, producer, runtime ---
        # Process in batches of 5 concurrent pages to be polite but fast
        BATCH_SIZE = 5
        results = []

        for i in range(0, len(movies), BATCH_SIZE):
            batch = movies[i : i + BATCH_SIZE]
            tasks = [scrape_movie_details(context, m["url"]) for m in batch]
            details = await asyncio.gather(*tasks)

            for movie, detail in zip(batch, details):
                rating_match = re.match(r"([\d.]+)", movie["rating"])
                rating = float(rating_match.group(1)) if rating_match else None
                results.append(
                    {
                        "rank": movie["rank"],
                        "title": movie["title"],
                        "year": movie["year"],
                        "rating": rating,
                        "runtime": detail["runtime"],
                        "director": detail["director"],
                        "producers": detail["producers"],
                    }
                )

            last = results[-1]
            print(
                f"  [{last['rank']:>3}/250] {last['title'][:40]:<40}  "
                f"dir={last['director'][:30]}  prod={last['producers'][:30]}"
            )

        await browser.close()

    # --- Step 3: Write CSV ---
    output_file = "imdb_top250.csv"
    fieldnames = ["rank", "title", "year", "rating", "runtime", "director", "producers"]
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nScraped {len(results)} movies to {output_file}")
    print()
    for m in results[:5]:
        print(
            f"  {m['rank']:>3}. {m['title']:<40} ({m['year']})  "
            f"★{m['rating']}  {m['runtime']:<8}  dir: {m['director']}"
        )
    print("  ...")
    for m in results[-3:]:
        print(
            f"  {m['rank']:>3}. {m['title']:<40} ({m['year']})  "
            f"★{m['rating']}  {m['runtime']:<8}  dir: {m['director']}"
        )


if __name__ == "__main__":
    asyncio.run(scrape_imdb_top250())
