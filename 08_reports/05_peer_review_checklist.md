# Peer Review Checklist

## 1. Data
- [ ] **Keys Unique:** Are all primary keys (e.g., `user_id`, `event_id`) unique where expected?
- [ ] **Nulls Understood:** Are null values handled appropriately in all data pipelines (SQL and Python)?
- [ ] **Distributions Stable:** Are feature distributions reasonable and stable compared to prior runs or expectations?
- [ ] **Schema Adherence:** Does the data adhere to the defined schema (`02_data/00_schema.md`)?

## 2. Model
- [ ] **Train/Test Split:** Is the data split correctly for training and testing, avoiding data leakage?
- [ ] **Cross-Validation:** Is cross-validation used to assess model robustness and prevent overfitting?
- [ ] **Metrics:** Are appropriate evaluation metrics chosen and reported (e.g., AUC, precision, recall, F1-score)?
- [ ] **Feature Importance:** Is feature importance clearly analyzed and explained (e.g., logistic regression coefficients, SHAP values for tree models)?
- [ ] **Calibration:** Is model calibration assessed, especially if probability scores are used for decision-making?
- [ ] **Overfitting Checks:** Are specific steps taken to check for and mitigate overfitting (e.g., comparing train/test AUC, regularization)?

## 3. Code
- [ ] **Reproducible:** Is the code reproducible from end-to-end (e.g., random seeds set, dependencies clear)?
- [ ] **Parameterized:** Are configurable parameters externalized rather than hard-coded?
- [ ] **Cleanliness:** Is the code well-structured, readable, and commented where necessary?
- [ ] **Error Handling:** Are potential errors handled gracefully?

## 4. Business
- [ ] **Target Alignment:** Is the model's target variable (`is_high_intent`) still aligned with the current business strategy and objectives?
- [ ] **Actionable Insights:** Does the model provide actionable insights for product or commercial teams?
- [ ] **Limitations & Assumptions:** Are model limitations, assumptions, and potential biases clearly documented and communicated?
- [ ] **Safety/Ethical Considerations:** Are fairness aspects (e.g., across demographic groups) considered and documented?

This checklist ensures that models are robust, transparent, and aligned with Bumble's business goals and safety standards, fostering a culture of peer learning and accountability.