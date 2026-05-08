# Code Review & Peer Validation Checklist

## 1. Data Integrity & Quality Checks
- [ ] **Data Source:** Is the data being pulled from the correct `features_for_modeling` view (or other specified BigQuery tables)?
- [ ] **Schema Conformance:** Do the columns and their data types match the expected schema (`02_data/00_schema.md`)?
- [ ] **Null Values:** Are missing values handled appropriately? (e.g., `fillna(0)` for `match_rate_30d` and `swipe_to_match_ratio`)
- [ ] **Uniqueness:** Are key identifiers (e.g., `user_id`) unique where expected?
- [ ] **Data Freshness:** Is the data being used up-to-date according to the monitoring plan?
- [ ] **Edge Cases:** Are potential edge cases (e.g., users with zero activity, new users) handled without error?

## 2. Model Development & Evaluation
- [ ] **Target Definition:** Is the target variable (`is_high_intent`) correctly defined and aligned with the business objective?
- [ ] **Feature Engineering:** Are features correctly derived and scaled? Is there any leakage?
- [ ] **Splitting Strategy:** Is the train/test split appropriate (e.g., stratified, temporal if applicable)?
- [ ] **Model Choice:** Is the chosen model (Logistic Regression, RandomForest, XGBoost) justified for the task?
- [ ] **Hyperparameters:** Are hyperparameters tuned, or are reasonable defaults/ranges provided?
- [ ] **Performance Metrics:** Are appropriate evaluation metrics used (e.g., AUC, precision, recall, classification report)?
- [ ] **Overfitting:** Are overfitting checks (e.g., cross-validation, train/test AUC comparison) performed and documented?
- [ ] **Interpretability:** Is feature importance analyzed (e.g., coefficients, SHAP values) and clearly explained?
- [ ] **Calibration:** Is the model's calibration checked, especially if probability estimates are used?

## 3. Code Quality & Reproducibility
- [ ] **Readability:** Is the code clean, well-commented, and easy to understand?
- [ ] **Modularity:** Is the code broken down into logical functions or sections?
- [ ] **Dependencies:** Are all required libraries explicitly imported?
- [ ] **Random Seeds:** Are random seeds set for reproducibility (`RANDOM_SEED`)?
- [ ] **Hardcoding:** Are hardcoded values minimized? Configuration parameters should be externalized.
- [ ] **Version Control:** Is the code checked into the correct repository and branch?
- [ ] **Error Handling:** Are potential errors (e.g., division by zero) handled gracefully (e.g., `SAFE_DIVIDE` in SQL, `fillna` in Python)?

## 4. Business Alignment & Communication
- [ ] **Problem Alignment:** Does the model directly address the business problem outlined in `01_project/01_business_case.md`?
- [ ] **KPI Linkage:** Is the model's impact on key performance indicators (ARPPU, Match→Message, OfflineProgressionEfficiency) clearly articulated?
- [ ] **Stakeholder Readability:** Is the interpretation of model results (e.g., cluster profiles, feature importance, bias analysis) presented in a business-friendly manner?
- [ ] **Limitations:** Are model limitations and assumptions clearly stated (e.g., synthetic data context, lack of fairness mitigation)?
- [ ] **Ethical Considerations:** Are potential biases (e.g., across demographic groups) acknowledged and discussed (`08_reports/04_model_validation_summary.md`)?

## 5. Deployment & Operational Readiness
- [ ] **Monitoring Plan:** Is there a clear plan for monitoring model performance, data drift, and prediction drift (`08_reports/09_phase_vi_monitoring_and_iteration.md`)?
- [ ] **Retraining Strategy:** Is the retraining cadence and trigger logic well-defined?
- [ ] **Documentation:** Are all relevant reports and model cards updated and accessible (`08_reports/`)?
- [ ] **Scalability:** Are the proposed solutions scalable (e.g., BigQuery views, batch scoring)?
- [ ] **Alerting:** Are alerting mechanisms in place for critical deviations?

This checklist serves as a guide for ensuring the robustness, fairness, and business utility of the high-intent propensity model within Bumble's Core Data Science framework.