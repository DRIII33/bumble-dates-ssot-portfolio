# Executive Summary — Bumble Dates Experience: Measurement & Modeling Pipeline

## 1. Project Objective & Business Problem
This project addresses Bumble's strategic goal to operationalize an end-to-end measurement and modeling pipeline for the new 'Dates' experience. As the DRI Data Scientist, the mission was to create a Single Source of Truth (SSOT) for member behavior, develop behavioral segmentations and propensity models to optimize offline progression and ARPPU, and deliver causal evidence on the Dates rollout and AI 'Bee' interventions, all while preserving safety and marketplace balance. The context includes a deliberate 21.1% reduction in paying users to prioritize intentional engagement.

## 2. Methodology & Technical Approach

### 2.1 Data Generation & SSOT
Synthetic datasets (`users.csv`, `events.csv`, `matches.csv`, `messages.csv`, `payments.csv`, `verifications.csv`) were generated to mimic Bumble's ecosystem, including noise (duplicates, missing values) and key events like the 'Dates' rollout and user pruning. These were ingested into Google BigQuery, forming staging tables. A robust SSOT view (`ssot_members`) was created, followed by a `features_for_modeling` view for downstream analytics, leveraging SQL techniques like CTEs, window functions, and `SAFE_DIVIDE`.

### 2.2 Behavioral Segmentation
K-Means clustering was applied to key behavioral features (`sessions_30d`, `matches_30d`, `date_suggestions_30d`, `match_rate_30d`, `swipe_to_match_ratio`) to identify distinct user segments. This provides a framework for understanding diverse user engagement patterns and tailoring product interventions.

### 2.3 High-Intent Propensity Modeling
A 'high-intent' target was defined as users who are verified (`verification_passed == 1`), have a `match_rate_30d >= 0.15`, and `sessions_30d >= 2`. Logistic Regression, RandomForest, and XGBoost models were trained to predict this propensity. Feature importance analysis consistently highlighted `verification_passed`, `sessions_30d`, and `matches_30d` as key drivers.

### 2.4 Model Validation & Operationalization
Comprehensive validation included row-level consistency checks, user ID uniqueness, null assertions, cross-validation (Logistic Regression AUC ~0.99), calibration checks, and train/test AUC comparison for tree models (AUC ~1.0 due to synthetic separability). A bias/fairness lens explored predicted high-intent rates across gender and intent levels. A monitoring and retraining plan was outlined for production. SHAP analysis provided detailed interpretability for the XGBoost model, confirming key drivers and their impact on predictions.

## 3. Key Findings & Business Impact

-   **SSOT Foundation:** The BigQuery SSOT provides a single, reliable source for all behavioral data, enabling consistent reporting and analysis.
-   **Identified Behavioral Segments:** Clustering reveals distinct user groups, allowing targeted strategies for engagement and monetization. For example, 'High-Intent Verified' users (Cluster 1) show high engagement and match rates, while 'Low-Engagement Browsers' (Cluster 0) require different activation strategies.
-   **Quantifiable High-Intent Users:** The propensity model accurately identifies users with a high likelihood of being intentional and engaged. Key drivers are `verification_passed`, `sessions_30d`, and `matches_30d`, emphasizing Bumble's 'quality reset' strategy. The model achieved an AUC of ~0.99, demonstrating strong predictive power for this segment.
-   **Causal Measurement Framework:** The project lays the groundwork for robust causal evaluation of product interventions (e.g., Dates UX, Bee AI) using methods like Difference-in-Differences and Synthetic Control, moving beyond simple A/B testing.
-   **Operational Readiness:** A clear plan for monitoring (model performance, data/prediction drift), retraining, and governance ensures the model remains effective and trustworthy in a production environment.

## 4. Conclusion & Next Steps
This project successfully established an end-to-end data science pipeline, from data generation and SSOT creation to advanced modeling, validation, and operational planning. It demonstrates the ability to translate strategic business challenges into actionable data science solutions, aligning directly with the responsibilities of a DRI Data Scientist at Bumble. The next steps include building comprehensive Looker Studio dashboards, further enhancing model interpretability with SHAP, and implementing the outlined causal measurement framework.
