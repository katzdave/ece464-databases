# Grammy Database "Insights" - Cheat Sheet

Run the queries from `interesting_queries.sql` and use these talking points:

## Query 1: Instant Icons
**What to say:** "Only 11 artists in Grammy history have dominated so completely in their debut that they won Best New Artist PLUS another Big Four award in the same year. Notice Billie Eilish in 2020 - she's one of only THREE artists EVER to sweep 3 Big Four awards in their debut year."

**Key findings:**
- Only 3 artists swept 3 Big Four awards as newcomers: Billie Eilish (2020), Norah Jones (2003), Christopher Cross (1981)
- This is extremely rare - shows immediate cultural dominance
- Last time it happened before Billie: 17 years prior (Norah Jones)

---

## Query 2: Longevity Champions
**What to say:** "U2 shows remarkable staying power - winning Big Four Grammys across 18 years (1988-2006). This demonstrates sustained excellence and multi-generational appeal."

**Key findings:**
- Among top artists, only U2 has 15+ years between first and last Big Four win
- Shows the difficulty of maintaining Grammy-level excellence over decades
- Most artists have concentrated success periods, not sustained dominance

---

## Query 3: Era of Competition
**What to say:** "The data reveals how the Grammys evolved. The 1950s had only 4 total winners across 3 categories - the awards were just getting started. The 2000s and 2010s each had 50 unique winners, showing increased diversity in music and/or category expansion. Interestingly, the 2020s show a drop to 39 winners so far."

**Key findings:**
- 2000s & 2010s: Peak competition with 50 winners each
- 1950s: Only 4 winners total (1.3 per category) - Grammys just started
- 2020s: 39 winners but decade incomplete (data through 2026)
- Consistent ~10 winners per category from 1970s onward

---

## Query 4: The Sweep Artists
**What to say:** "Winning multiple Big Four awards in a single year is incredibly rare. In 67 years of Grammy history, only 21 artists have done it, and just 3 have won THREE Big Four awards in one year. When this happens, that artist essentially owns that entire year of music."

**Key findings:**
- **Triple sweeps (3 Big Four in one year):** Only Billie Eilish (2020), Norah Jones (2003), Christopher Cross (1981)
- **Double wins:** 18 artists, including Adele (twice!), Michael Jackson, Eric Clapton
- Most recent sweep: Silk Sonic in 2022 (Record + Song of the Year)
- Adele is the only artist to double-sweep in TWO different years (2012 & 2017)

---

## Query 5: One-Year Wonders vs Repeat Champions
**What to say:** "Here's the harsh reality: 90% of Big Four Grammy winners (201 out of 223 artists) only win in a single year - they never repeat. Only 2 artists have managed to win across 4+ different years, making them true 'Consistent Champions.' This shows how difficult it is to sustain Grammy-level success."

**Key findings:**
- **One-Year Winners:** 201 artists (90%) - most artists never win a Big Four award again
- **Multi-Year Winners (2-3 years):** 20 artists - rare repeat success
- **Consistent Champions (4+ years):** Only 2 artists across entire Grammy history
- Average wins: One-year wonders get 1.1 awards, consistent champions get 4.0

**The takeaway:** Grammy success is typically a flash, not a career-long pattern.

---

## Bonus Talking Points

- "Notice how SQL aggregations and JOINs reveal patterns that aren't visible in raw data"
- "The WITH clause (CTEs) makes complex analysis readable and maintainable"
- "STRING_AGG is powerful for creating human-readable summaries from normalized data"
- "Always think about what questions your data can answer, not just what data you have"

## Pro Tip
When a student asks if you ran these before class, just say: "I was exploring the data and these patterns jumped out at me. That's the power of SQL - you can ask the data questions and get immediate answers."
