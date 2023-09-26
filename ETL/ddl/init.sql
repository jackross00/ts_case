-- Note: I'm making this all in one schema for sake of speed. --

--------------------
-- STAGING TABLES --
--------------------

CREATE TABLE stg_website_visits
(
    date VARCHAR,
    website VARCHAR,
    visits VARCHAR
);

CREATE TABLE stg_brand_healthyfeet
(
    date VARCHAR,
    website VARCHAR,
    brand VARCHAR,
    impressions VARCHAR,
    clicks VARCHAR,
    conversions VARCHAR,
    revenue VARCHAR
);


CREATE TABLE stg_brand_runnation
(
    date VARCHAR,
    webpage VARCHAR,
    brand VARCHAR,
    impressions VARCHAR,
    clicks VARCHAR,
    revenue VARCHAR,
    rev_conv VARCHAR
);

CREATE TABLE stg_brand_sneakerheads
(
    date VARCHAR,
    brand VARCHAR,
    imp VARCHAR,
    clicks VARCHAR,
    conv VARCHAR,
    rev VARCHAR
);

--------------------------
-- STANDARDIZING TABLES --
--------------------------

CREATE TABLE std_website_visits
(   
    web_seq int,
    load_time timestamp,
    entry_date date,
    website VARCHAR(500),
    visits int
);

CREATE TABLE std_brand_healthyfeet
(
    web_seq int,
    brand_seq int,
    load_time timestamp,
    entry_date date,
    website VARCHAR(500),
    brand VARCHAR(500),
    impressions int,
    clicks int,
    conversions int,
    revenue int
);


CREATE TABLE std_brand_runnation
(
    web_seq int,
    brand_seq int,
    load_time timestamp,
    entry_date date,
    website VARCHAR(500),
    brand VARCHAR(500),
    impressions int,
    clicks int,
    conversions int,
    revenue int
);

CREATE TABLE std_brand_sneakerheads
(
    web_seq int,
    brand_seq int,
    load_time timestamp,
    entry_date date,
    website VARCHAR(500),
    brand VARCHAR(500),
    impressions int,
    clicks int,
    conversions int,
    revenue int
);

----------------------
-- DATAVAULT TABLES --
----------------------

-- These hubs might seem overkill right now, but later we can easily add more to the bk later if needed. --
CREATE TABLE hub_website (
    web_seq serial PRIMARY KEY,
    load_time timestamp,
    web_bk varchar(500),
    website varchar(500)   
);

CREATE TABLE hub_brand (
    brand_seq serial PRIMARY KEY,
    load_time timestamp,
    brand_bk varchar(500),
    brand varchar(500)
);

-- Satelites, description events --
CREATE TABLE sat_website_visits
(
    web_seq serial,
    load_time timestamp,
    entry_date date,
    visits int
);

CREATE TABLE sat_metrics (
    web_seq serial,
    brand_seq serial,
    load_time timestamp,
    entry_date date,
    impressions int,
    clicks int,
    conversions int,
    revenue int  
);

-- Links -- 
-- Not very applicable in this application until data gets more complex --

-- Views --

CREATE VIEW vw_brand_performance AS (
    SELECT  c.website,
            b.brand,
            a.entry_date,
            a.impressions,
            a.clicks,
            a.conversions,
            a.revenue
    FROM sat_metrics a
    LEFT JOIN hub_brand b
    ON a.brand_seq = b.brand_seq 
    LEFT JOIN hub_website c 
    ON a.web_seq = c.web_seq
);