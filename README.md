# bumble-dates-ssot-portfolio


**Data Scientist:** Daniel Rodriguez III

**Date:** May 8, 2026


## Project Overview
This project builds a reproducible SSOT and measurement pipeline for Bumble’s Dates experience, enabling behavioral segmentation, causal evaluation of product changes, and safety scoring. It demonstrates end-to-end skills (Python, SQL, BigQuery, visualization) mapped to Bumble’s Core Data Science responsibilities.

### Project Framing & Business Scenario
**Top challenges:**

* **Quality reset trade-off (Pruning vs. Scale):** balancing a deliberate 21.1% reduction in paying users with network-effect risks.

* **Modeling intent beyond swipes:** moving from binary swipe signals to richer “Dates” and intent/storytelling signals.

* **Causal measurement & incrementality:** product changes (removing swipe → Dates) require causal frameworks beyond short A/B tests.

* **AI orchestration & safety:** integrating the front-facing “Bee” assistant while preserving authenticity and refining safety models (Private Detector).

* **Marketplace dynamics & multi-sided trade-offs:** ensuring balanced discovery across gender, intent, and geography.

#### **Business Problem (DRI scenario):**  
*You are the Directly Responsible Individual (DRI) Data Scientist in Bumble’s Austin Core Data Science team. Your mission is to design, implement, and operationalize an end-to-end measurement and modeling pipeline that (1) creates a Single Source of Truth (SSOT) for member behavior across the new “Dates” experience, (2) produces behavioral segmentations and propensity models that optimize offline progression and ARPPU, and (3) delivers causal evidence on the Dates rollout and AI “Bee” interventions while preserving safety and marketplace balance.*

## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Setup Instructions](#setup-instructions)
- [How to Run the Project](#how-to-run-the-project)
- [Key Findings & Highlights](#key-findings--highlights)
- [Technologies Used](#technologies-used)
- [License](#license)

## Repository Structure

| Path | Purpose |
|---|---|
| `README.md` | Project overview, setup, and run instructions |
| `01_project/01_business_case.md` | Business scenario, KPIs, DRI responsibilities |
| `01_project/02_success_metrics.md` | Definitions: ARPPU, Match→Message, OfflineProgressionEfficiency |
| `02_data/00_schema.md` | Synthetic schema spec (tables & fields) |
| `02_data/01_generate_synthetic_data_colab.ipynb` | Google Colab notebook (Python) to generate datasets |
| `02_data/01_generate_synthetic_data.py` | Standalone Python script (same logic as notebook) |
| `02_data/sample_data/README.md` | Sample CSVs exported for BigQuery load |
| `03_sql/00_bigquery_setup.md` | BigQuery dataset & table creation notes (project: **driiiportfolio**) |
| `03_sql/01_raw_ingest.sql` | SQL to create raw staging tables (DDL/LOAD guidance) |
| `03_sql/02_transform_ssot.sql` | SSOT transformation (CTEs, window functions) |
| `03_sql/03_feature_store.sql` | Feature engineering queries for modeling |
| `04_models/01_clustering_notebook.ipynb` | Python notebook: clustering & segmentation |
| `04_models/02_propensity_model.py` | Python script: propensity modeling (sklearn) |
| `05_experiments/01_causal_design.md` | Causal strategy: synthetic control, difference-in-diff |
| `06_visuals/01_looker_dashboard_spec.md` | Looker/Data Studio dashboard spec & mock screenshots |
| `07_docs/01_code_review_checklist.md` | Code review & peer validation checklist |
| `07_docs/02_deployment_runbook.md` | Monitoring, retraining, alerting SOP |
| `08_reports/01_executive_summary.pdf` | Executive summary (findings & recommendations) |
| `08_reports/02_model_card_high_intent.md` | Model Card for High-Intent Propensity Model |
| `08_reports/03_target_diagnostic_high_value_vs_high_intent.md` | Target Diagnostic Report |
| `08_reports/04_model_validation_summary.md` | Model Validation Summary |
| `08_reports/05_peer_review_checklist.md` | Peer Review Checklist |
| `08_reports/06_phase_v_plan.md` | Phase V Plan: Deployment, Dashboards, Causal Measurement |
| `08_reports/07_looker_dashboard_spec.md` | Looker Studio Dashboard Specification |
| `08_reports/08_shap_interpretability.md` | SHAP Interpretability Section |
| `08_reports/09_phase_vi_monitoring_and_iteration.md` | Phase VI Monitoring & Iteration Plan |
| `LICENSE` | License |
| `.gitignore` | Standard ignores |

## Setup Instructions
This project utilizes Google Colab (Python) and BigQuery free-tier (SQL). 

1.  **Google Colab:** Ensure you have access to Google Colab and necessary Python libraries (`pandas`, `numpy`, `scikit-learn`, `xgboost`, `shap`, `google-cloud-bigquery`). These are typically pre-installed or can be installed via `!pip install`.
2.  **BigQuery Setup:**
    *   Create a Google Cloud Project if you don't have one.
    *   Enable the BigQuery API.
    *   In your BigQuery project, create a dataset named `driiiportfolio.bumble_portfolio`.
    *   Authenticate your Colab notebook to BigQuery using `from google.colab import auth; auth.authenticate_user()`.
3.  **Load CSVs to BigQuery:** After generating synthetic data (see below), upload the CSV files (`users.csv`, `events.csv`, `matches.csv`, `messages.csv`, `payments.csv`, `verifications.csv`) to your `driiiportfolio.bumble_portfolio` dataset in BigQuery. Name the tables: `stg_users`, `stg_events`, `stg_matches`, `stg_messages`, `stg_payments`, `stg_verifications`.

## How to Run the Project
Follow these steps to reproduce the project's outputs:

1.  **Generate Synthetic Data:**
    *   Run the Google Colab notebook `02_data/01_generate_synthetic_data_colab.ipynb` (or the script `02_data/01_generate_synthetic_data.py`) to generate the required CSV datasets.
    *   Ensure the generated CSVs are saved to `02_data/sample_data/` (or a location you can upload from) and then uploaded to BigQuery as staging tables as described in the Setup Instructions.
2.  **Execute SQL Transformations:**
    *   Run the SQL scripts in BigQuery in the following order:
        *   `03_sql/01_raw_ingest.sql` (to ensure dataset exists and staging tables are conceptually ready)
        *   `03_sql/02_transform_ssot.sql` (to create the `ssot_members` view)
        *   `03_sql/03_feature_store.sql` (to create the `features_for_modeling` view)
3.  **Run Analytical Models:**
    *   Execute the Python notebooks in Colab, starting with `04_models/01_clustering_notebook.ipynb` (or a similar notebook combining EDA, clustering, and propensity modeling). These notebooks will connect to BigQuery to fetch the `features_for_modeling` view.
    *   The `04_models/02_propensity_model.py` script (if used standalone) will also consume the exported features.
4.  **Visualize Results:**
    *   Build Looker Studio (formerly Data Studio) dashboards using the specifications in `06_visuals/01_looker_dashboard_spec.md` and connecting to your BigQuery `ssot_members` and `propensity_scores` tables.
5.  **Review Documentation & Reports:**
    *   Refer to the markdown files in the `07_docs/` and `08_reports/` directories for detailed information on causal design, model cards, validation summaries, and deployment runbooks.

## Key Findings & Highlights
-   **Single Source of Truth (SSOT):** A robust data pipeline establishes an `ssot_members` view in BigQuery, integrating user profiles, verifications, events, and payments.
-   **Behavioral Segmentation:** K-Means clustering identifies distinct user segments (e.g., "Low-Engagement", "High-Intent Verified") based on 30-day activity metrics.
-   **High-Intent Propensity Model:** A Logistic Regression and tree-based models (RandomForest, XGBoost) predict user propensity for "high-intent" behavior (defined by verification, match rate, and sessions). Key drivers include `verification_passed`, `sessions_30d`, and `matches_30d`.
-   **Causal Measurement Readiness:** The project structure supports causal evaluation of product changes (like the "Dates" rollout and AI "Bee" interventions) using methods like Difference-in-Differences and Synthetic Control.
-   **Operationalization:** Includes plans for model monitoring, retraining, bias checks, and comprehensive documentation to ensure a production-ready system.

## Technologies Used
-   **Data Storage & Warehousing:** Google BigQuery
-   **Data Generation & Transformation:** Python (Pandas, NumPy), Google Colab, SQL
-   **Machine Learning:** Scikit-learn (KMeans, StandardScaler, RandomForestClassifier, LogisticRegression), XGBoost
-   **Visualization:** Google Looker Studio (specifications provided)
-   **Version Control:** Git, GitHub

## License
This project is licensed under the [MIT License](LICENSE).
