# Grammy Awards Database

This directory contains a complete PostgreSQL database of Grammy Awards data.

## Quick Start

### Prerequisites
- Docker installed and running
- PostgreSQL container running (see setup below if you don't have one)

### Setup PostgreSQL Container (if needed)

If you don't already have a PostgreSQL container running:

```bash
docker run --name databases-course \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5440:5432 \
  -d postgres
```

### Create and Populate the Database

Run these two commands:

```bash
# Create the database
docker exec -i databases-course psql -U postgres -c "CREATE DATABASE grammys;"

# Load the schema and data
docker exec -i databases-course psql -U postgres -d grammys < grammys_complete.sql
```

### Connect to the Database

**From your terminal:**
```bash
docker exec -it databases-course psql -U postgres -d grammys
```

**Or using local psql client:**
```bash
psql -h localhost -p 5440 -U postgres -d grammys
# Password: mysecretpassword
```

## Database Schema

The database contains four tables:

### 1. `grammy_awards_winners` (311 rows)
All Grammy award winners with detailed information.

**Columns:**
- `id` - Primary key
- `year` - Year of the ceremony
- `ceremony_number` - Grammy ceremony number
- `decade` - Decade (e.g., "2020")
- `era` - Era description (e.g., "2020s", "Early Grammys (1959-1969)")
- `category` - Award category
- `award_group` - Category group (e.g., "Big Four")
- `winner` - Name of the winning work
- `artist` - Artist name(s)
- `status` - "Winner"
- `total_wins` - Total wins for this winner
- `category_total_winners` - Total winners in this category historically
- `data_source` - Source of the data
- `collection_date` - When the data was collected

### 2. `grammy_big_four_awards` (278 rows)
Winners of the "Big Four" Grammy categories:
- Album of the Year
- Record of the Year
- Song of the Year
- Best New Artist

**Columns:** Same as `grammy_awards_winners`

### 3. `grammy_top_artists` (20 rows)
Top 20 Grammy-winning artists by total wins.

**Columns:**
- `id` - Primary key
- `artist` - Artist name
- `total_wins` - Total number of Grammy wins
- `first_win_year` - Year of first win
- `last_win_year` - Year of most recent win
- `sample_categories` - Example categories won
- `rank` - Ranking by total wins

### 4. `grammy_winners_by_decade` (36 rows)
Summary of winners by decade and category.

**Columns:**
- `id` - Primary key
- `decade` - Decade (e.g., "1950", "2020")
- `category` - Award category
- `total_winners` - Number of winners in this decade/category

## Example Queries

### Get all winners from 2026
```sql
SELECT year, category, winner, artist
FROM grammy_awards_winners
WHERE year = 2026;
```

### Find top artists
```sql
SELECT artist, total_wins, first_win_year, last_win_year
FROM grammy_top_artists
ORDER BY total_wins DESC
LIMIT 10;
```

### Big Four winners by decade
```sql
SELECT decade, category, COUNT(*) as num_winners
FROM grammy_big_four_awards
GROUP BY decade, category
ORDER BY decade, category;
```

### Artists with multiple Album of the Year wins
```sql
SELECT artist, COUNT(*) as wins
FROM grammy_awards_winners
WHERE category = 'Album of the Year'
GROUP BY artist
HAVING COUNT(*) > 1
ORDER BY wins DESC;
```

## Data Source

Data collected from Wikipedia on February 8, 2026.

## Files

- `grammys_complete.sql` - Complete database setup script (schema + data)
- `setup_grammys.sql` - Schema only (table definitions)
- `grammy/` - Original CSV files
- `README.md` - This file
