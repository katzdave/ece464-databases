-- 5 Interesting Grammy Queries to Impress Students
-- Run these in the grammys database

-- 1. The "Instant Icons" - Artists who won a Big Four award as a Best New Artist
-- Insight: "Notice how some artists immediately dominated - winning both Best New Artist
-- and another major award in the same year. This is quite rare!"
SELECT
    bna.year,
    bna.artist,
    bna.category as new_artist_category,
    bf.category as other_big_four_award,
    bf.winner as winning_work
FROM grammy_big_four_awards bna
JOIN grammy_big_four_awards bf
    ON bna.artist = bf.artist
    AND bna.year = bf.year
    AND bf.category != 'Best New Artist'
WHERE bna.category = 'Best New Artist'
ORDER BY bna.year DESC;


-- 2. The "Longevity Champions" - Artists with 15+ years between first and last win
-- Insight: "These artists show remarkable staying power - continuing to produce
-- Grammy-worthy work across decades. Notice the multi-generational appeal!"
SELECT
    artist,
    total_wins,
    first_win_year,
    last_win_year,
    (last_win_year - first_win_year) as years_of_dominance,
    sample_categories
FROM grammy_top_artists
WHERE (last_win_year - first_win_year) >= 15
ORDER BY years_of_dominance DESC, total_wins DESC;


-- 3. The "Era of Competition" - Which decades had the most unique winners?
-- Insight: "Interesting pattern here - we can see how the music industry has evolved.
-- More winners might indicate more diversity, or more categories being added."
SELECT
    decade,
    COUNT(DISTINCT category) as num_categories,
    SUM(total_winners) as total_unique_winners,
    ROUND(AVG(total_winners), 1) as avg_winners_per_category
FROM grammy_winners_by_decade
GROUP BY decade
ORDER BY decade DESC;


-- 4. The "Sweep Artists" - Artists who won multiple Big Four awards in a single year
-- Insight: "These are the truly dominant years in Grammy history. When an artist
-- sweeps multiple Big Four awards, they're basically owning that entire year of music."
SELECT
    year,
    artist,
    COUNT(DISTINCT category) as big_four_wins,
    STRING_AGG(category || ': ' || winner, ' | ') as awards_won
FROM grammy_big_four_awards
GROUP BY year, artist
HAVING COUNT(DISTINCT category) >= 2
ORDER BY big_four_wins DESC, year DESC;


-- 5. The "One-Year Wonders" vs "Repeat Champions" in Big Four Categories
-- Insight: "This tells us about consistency vs. flash-in-the-pan success.
-- Are Big Four wins a one-time thing, or do great artists keep winning?"
WITH artist_appearances AS (
    SELECT
        artist,
        COUNT(DISTINCT year) as years_won,
        COUNT(*) as total_big_four_wins,
        MIN(year) as first_win,
        MAX(year) as last_win,
        STRING_AGG(DISTINCT category, ', ') as categories_won
    FROM grammy_big_four_awards
    GROUP BY artist
)
SELECT
    CASE
        WHEN years_won = 1 THEN 'One-Year Winners'
        WHEN years_won BETWEEN 2 AND 3 THEN 'Multi-Year Winners (2-3)'
        ELSE 'Consistent Champions (4+)'
    END as winner_type,
    COUNT(*) as num_artists,
    ROUND(AVG(total_big_four_wins), 1) as avg_total_wins
FROM artist_appearances
GROUP BY
    CASE
        WHEN years_won = 1 THEN 'One-Year Winners'
        WHEN years_won BETWEEN 2 AND 3 THEN 'Multi-Year Winners (2-3)'
        ELSE 'Consistent Champions (4+)'
    END
ORDER BY num_artists DESC;
