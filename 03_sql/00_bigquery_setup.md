### BigQuery Setup Notes (Project: driiiportfolio)

This document provides guidance for setting up the necessary dataset and tables in Google BigQuery for the `bumble-dates-ssot-portfolio` project.

#### 1. Google Cloud Project Setup
Ensure you have a Google Cloud Project with billing enabled (if exceeding free-tier limits, though this project is designed for free-tier).

#### 2. Create BigQuery Dataset
Create a BigQuery dataset named `bumble_portfolio` within your `driiiportfolio` project.

```sql
-- 03_sql/00_bigquery_setup.md
-- Create dataset (run once)
CREATE SCHEMA IF NOT EXISTS `driiiportfolio.bumble_portfolio`;
```

#### 3. Upload CSVs as Staging Tables
After generating the synthetic data using `02_data/01_generate_synthetic_data.py` (or `02_data/01_generate_synthetic_data_colab.ipynb`),
 upload the following CSV files into the `driiiportfolio.bumble_portfolio` dataset:

- `users.csv`  -> Table: `stg_users`
- `verifications.csv` -> Table: `stg_verifications`
- `events.csv` -> Table: `stg_events`
- `matches.csv` -> Table: `stg_matches`
- `messages.csv` -> Table: `stg_messages`
- `payments.csv` -> Table: `stg_payments`

**Instructions for UI Upload:**
1.  Navigate to your `bumble_portfolio` dataset in the BigQuery UI.
2.  Click on '+ CREATE TABLE'.
3.  For 'Source', select 'Upload' and choose a CSV file from `02_data/sample_data/`.
4.  For 'Destination', set 'Table name' with the `stg_` prefix (e.g., `stg_users`).
5.  Ensure 'Schema' is set to 'Auto detect' or manually define it based on `02_data/00_schema.md`.
6.  Repeat for all six CSV files.

#### 4. Partitioning & Clustering (Emulation)
To emulate Snowflake-like partitioning and clustering, create partitioned tables in BigQuery.
For example, the `stg_events` table would typically be partitioned by `event_ts` and clustered by `user_id`.

```sql
-- Example for events_partitioned (from 01_generate_synthetic_data.py notes)
CREATE TABLE `driiiportfolio.bumble_portfolio.events_partitioned`
PARTITION BY DATE(event_ts)
AS
SELECT *
FROM `driiiportfolio.bumble_portfolio.stg_events`;
```

**Note:** For local testing or if free-tier limits are strict, you might skip creating partitioned tables directly and rely on the staging tables first, moving to partitioned tables when optimizing performance.
