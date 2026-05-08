# Deployment Runbook — High-Intent Propensity Model

## 1. Overview
This runbook details the procedures for deploying, monitoring, and maintaining the High-Intent Propensity Model. It covers steps from batch scoring to alerting and retraining, ensuring the model remains operational and effective.

## 2. Model Artifacts & Location
- **Model:** `high_intent_propensity_model.pkl` (e.g., Logistic Regression or XGBoost)
- **Scaler:** `scaler.pkl` (StandardScaler used for clustering/modeling)
- **Feature Columns:** `feature_cols.json`
- **Location:** Google Cloud Storage (GCS) bucket: `gs://driiiportfolio-model-artifacts/high_intent/latest/`

## 3. Batch Scoring Pipeline

### 3.1 Trigger
- **Frequency:** Daily, triggered by a scheduled job (e.g., Cloud Composer/Airflow, or BigQuery Scheduled Query + Cloud Function).
- **Time:** `02:00 UTC` (after daily ETL completes).

### 3.2 Steps
1.  **Extract Features:**
    -   Run BigQuery query to extract `features_for_modeling` into a Pandas DataFrame in the Colab/Python scoring environment.
    ```sql
    SELECT * FROM `driiiportfolio.bumble_portfolio.features_for_modeling`;
    ```
2.  **Load Model & Preprocessing Assets:**
    -   Download `high_intent_propensity_model.pkl`, `scaler.pkl`, and `feature_cols.json` from GCS.
    -   Load Python objects using `joblib` or `pickle`.
3.  **Preprocess Data:**
    -   Apply loaded `scaler` to numerical features (`X_cluster` or relevant columns).
    -   Handle missing values as per `04_models/01_clustering_notebook.ipynb` (e.g., `fillna(0)`).
4.  **Score Users:**
    -   Predict propensity scores using the loaded model: `model.predict_proba(X_scaled)[:, 1]`.
    -   Assign users to clusters using the KMeans model: `kmeans.predict(X_cluster)`.
5.  **Save Results to BigQuery:**
    -   Create a DataFrame with `user_id`, `propensity_score`, `cluster`, `is_high_intent` (if derived post-scoring), and `scored_ts`.
    -   Write to BigQuery table: `driiiportfolio.bumble_portfolio.propensity_scores`.
    -   Ensure table is partitioned by `scored_ts` (DATE) for efficient querying.

## 4. Monitoring & Alerting

### 4.1 Dashboard
- **Tool:** Looker Studio dashboard (`06_visuals/01_looker_dashboard_spec.md`).
- **Key Metrics:**
    -   Model AUC (trended daily/weekly).
    -   Precision/Recall/F1 for high-intent class.
    -   Distribution of propensity scores (overall and by key segments: gender, country, intent_level).
    -   Distribution of cluster sizes.
    -   Key feature distributions (`sessions_30d`, `matches_30d`, `verification_passed`).

### 4.2 Automated Alerts (via Cloud Functions/BigQuery + Cloud Monitoring)
- **Model Performance:**
    -   If AUC drops by > 0.05 from baseline (e.g., last 30-day average).
    -   If F1-score for high-intent class drops by > 0.05.
- **Data Drift:**
    -   If mean/median of `sessions_30d` or `matches_30d` changes by > 2 standard deviations from historical average.
    -   If `verification_passed` rate changes by > 10% from historical average.
- **Prediction Drift:**
    -   If the proportion of users with `propensity_score > 0.7` changes by > 15% week-over-week.
- **Recipients:** Core Data Science team, relevant Product Managers.

## 5. Retraining Plan

### 5.1 Scheduled Retraining
- **Frequency:** Monthly, 1st Monday of the month.
- **Process:** Automate the execution of the Phase III notebook (`04_models/01_clustering_notebook.ipynb` equivalent) to generate a new model. This includes EDA, clustering, propensity modeling, and validation.
- **Output:** New model artifacts pushed to GCS: `gs://driiiportfolio-model-artifacts/high_intent/<DATE>/`.

### 5.2 Event-Driven Retraining
- **Triggers:**
    -   Sustained alerts from model performance or data/prediction drift.
    -   Major product changes (e.g., Dates UX overhaul, significant Bee AI updates, new onboarding flow).
    -   Changes in business strategy (e.g., new definition of high-intent).
- **Procedure:** Manual review by DRI Data Scientist, followed by re-execution of Phase III notebook.

### 5.3 Model Promotion (Shadow Deployment)
1.  **Deploy New Model to Shadow Environment:** New model scores a subset of production data alongside the existing model, but its predictions are not used for live decisions.
2.  **Monitor Shadow Performance:** Compare new model's AUC, calibration, and propensity distributions against the old model for 1-2 weeks.
3.  **A/B Test (Optional but Recommended):** For significant changes, A/B test the new model's impact on business KPIs (e.g., Match->Message, OfflineProgressionEfficiency) in a small, controlled user segment.
4.  **Full Rollout:** If shadow and A/B tests are positive, promote the new model artifacts to `gs://driiiportfolio-model-artifacts/high_intent/latest/`.

## 6. Rollback Procedures
- **Trigger:** Critical issues post-deployment (e.g., system errors, unexpected negative business impact).
- **Procedure:** Revert model artifacts in GCS `gs://driiiportfolio-model-artifacts/high_intent/latest/` to the previous stable version. This will automatically be picked up by the next scheduled batch scoring run.

## 7. Documentation & Communication
- **Model Card:** Update `08_reports/02_model_card_high_intent.md` for each new model version.
- **Validation Summary:** Update `08_reports/04_model_validation_summary.md`.
- **Communication:** Document all major deployments, retraining events, and performance changes in a central log accessible to stakeholders.

This runbook ensures a structured and robust approach to managing the High-Intent Propensity Model, aligning with Bumble's commitment to data-driven decision-making and platform health.