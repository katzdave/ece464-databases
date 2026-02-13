-- Create tables for Grammy data

-- Grammy Awards Winners table
DROP TABLE IF EXISTS grammy_awards_winners CASCADE;
CREATE TABLE grammy_awards_winners (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    ceremony_number INTEGER,
    decade VARCHAR(10),
    era TEXT,
    category TEXT,
    award_group VARCHAR(50),
    winner TEXT,
    artist TEXT,
    status VARCHAR(50),
    total_wins INTEGER,
    category_total_winners INTEGER,
    data_source VARCHAR(50),
    collection_date DATE
);

-- Grammy Big Four Awards table
DROP TABLE IF EXISTS grammy_big_four_awards CASCADE;
CREATE TABLE grammy_big_four_awards (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    ceremony_number INTEGER,
    decade VARCHAR(10),
    era TEXT,
    category TEXT,
    award_group VARCHAR(50),
    winner TEXT,
    artist TEXT,
    status VARCHAR(50),
    total_wins INTEGER,
    category_total_winners INTEGER,
    data_source VARCHAR(50),
    collection_date DATE
);

-- Grammy Top Artists table
DROP TABLE IF EXISTS grammy_top_artists CASCADE;
CREATE TABLE grammy_top_artists (
    id SERIAL PRIMARY KEY,
    artist TEXT,
    total_wins INTEGER,
    first_win_year INTEGER,
    last_win_year INTEGER,
    sample_categories TEXT,
    rank INTEGER
);

-- Grammy Winners By Decade table
DROP TABLE IF EXISTS grammy_winners_by_decade CASCADE;
CREATE TABLE grammy_winners_by_decade (
    id SERIAL PRIMARY KEY,
    decade VARCHAR(10),
    category TEXT,
    total_winners INTEGER
);
