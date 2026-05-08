# BigQuery Folder — Bumble Portfolio Project

This folder documents the BigQuery structures used in the Bumble High‑Intent Propensity & Behavioral Segmentation project.

## 1. Project & Dataset

- **Project ID:** `driiiportfolio`
- **Dataset:** `bumble_portfolio`

All tables and views are defined under this dataset.

---

## 2. Tables

### 2.1 Staging Tables (`stg_*`)
- `stg_users`
- `stg_events`
- `stg_matches`
- `stg_messages`
- `stg_payments`
- `stg_verifications`

These are loaded from synthetic CSVs and represent raw event and user data.

### 2.2 Core Tables
- `propensity_scores_raw`  
  - Batch scoring output from the Colab modeling notebook.  
  - One row per user with propensity score, cluster, and high‑intent label.

---

## 3. Views

### 3.1 Analytical Views
- `ssot_members`  
  - Single Source of Truth for member‑level features.

- `features_for_modeling`  
  - Feature store used for clustering and propensity modeling.

### 3.2 Scoring & Reporting Views
- `propensity_scores`  
  - Clean view over `propensity_scores_raw` for Looker Studio.

- `cluster_profiles`  
  - Cluster‑level averages of key behavioral metrics.

- `high_intent_summary`  
  - Aggregated metrics by `is_high_intent`.

- `dates_feature_insights`  
  - User‑level metrics focused on the Dates feature.

- `safety_verification_summary`  
  - Aggregated metrics by `verification_passed`.

---

## 4. Usage

- **Modeling:**  
  - `features_for_modeling` and `propensity_scores_raw` are consumed by Colab notebooks.

- **Dashboarding:**  
  - Looker Studio connects to `propensity_scores`, `cluster_profiles`, `high_intent_summary`, `dates_feature_insights`, and `safety_verification_summary`.

- **Governance:**  
  - All transformations are defined in SQL and documented in this repository.  
  - Validation and monitoring are described in `08_reports/04_model_validation_summary.md`.

---

## 5. Refresh & Maintenance

- Staging tables are refreshed when synthetic data is regenerated.  
- `propensity_scores_raw` is refreshed by the batch scoring pipeline.  
- Views always reflect the latest underlying data.
