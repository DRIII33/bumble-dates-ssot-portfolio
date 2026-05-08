-- 03_sql/01_raw_ingest.sql
-- Guidance for creating external/staging tables for raw CSV data.
-- These commands assume CSV files are already uploaded to a GCS bucket or local path accessible by BigQuery.
-- For this portfolio, the recommended method is to upload CSVs via the BigQuery UI and name them as stg_<table>.

-- Create dataset (if not already done via 03_sql/00_bigquery_setup.md)
CREATE SCHEMA IF NOT EXISTS `driiiportfolio.bumble_portfolio`;

-- Example DDL for an external table (if using GCS, replace 'gs://your-bucket/users.csv')
-- CREATE EXTERNAL TABLE `driiiportfolio.bumble_portfolio.stg_users`
-- OPTIONS (
--   format = 'CSV',
--   uris = ['gs://your-bucket/users.csv'],
--   schema = 'user_id STRING, signup_ts TIMESTAMP, country STRING, zip_code STRING, gender STRING, age INTEGER, intent_level STRING, is_paying INTEGER, initial_right_swipe_rate FLOAT, is_pruned INTEGER'
-- );

-- Since the instruction is to upload CSVs via UI, these SQL statements serve as documentation
-- for what a raw ingest typically entails (creating staging tables from raw sources).
-- For this project, you will manually load the CSVs into BigQuery tables named:
-- `stg_users`, `stg_verifications`, `stg_events`, `stg_matches`, `stg_messages`, `stg_payments`.

-- No direct executable SQL for table creation here, as the UI upload is preferred for this setup.
-- Validate staging tables using the checks in the next section.
