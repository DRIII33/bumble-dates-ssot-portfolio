# Phase VI — Monitoring & Iteration Plan

## 1. Continuous Monitoring

### 1.1 Model Performance Monitoring
- **Metrics:** Track AUC, precision, recall, and F1-score for the high-intent class on a weekly basis.
- **Thresholds:** Set alerts for significant drops (e.g., > 0.05 absolute change) in AUC or large shifts in precision/recall for the high-intent segment.
- **Tooling:** Utilize Looker Studio dashboards for visualizing performance trends and BigQuery scheduled queries for alert triggers.

### 1.2 Data Drift Monitoring
- **Features:** Monitor distributions of key features: `sessions_30d`, `matches_30d`, `match_rate_30d`, and `verification_passed`.
- **Methodology:** Compare current distributions to baseline distributions (e.g., previous month or training data) using statistical tests (e.g., Kolmogorov-Smirnov) or divergence metrics (e.g., Jensen-Shannon divergence).
- **Alerts:** Trigger alerts if significant drift is detected (e.g., p-value < 0.01 for statistical tests) in critical features.
- **Tooling:** Implement data drift checks via BigQuery scheduled queries or a dedicated Python script run in Colab/GCP. 

### 1.3 Prediction Drift Monitoring
- **Propensity Score Distribution:** Track the overall distribution of predicted high-intent propensity scores and the proportion of users classified as high-intent (e.g., p > 0.7).
- **Cluster Composition:** Monitor changes in the size and characteristics of the identified behavioral clusters.
- **Alerts:** Set alerts for changes greater than 10-15% week-over-week in high-intent share or significant shifts in cluster population distribution.

## 2. Retraining Cadence & Strategy

### 2.1 Scheduled Retraining
- **Frequency:** Retrain the model monthly by default.
- **Process:** Automate the re-execution of the Phase III notebook (EDA → clustering → propensity modeling → validation) to generate an updated model.

### 2.2 Event-Driven Retraining
- **Triggers:** Initiate immediate retraining if:
  - Model performance metrics (AUC, precision/recall) drop significantly below established thresholds.
  - Major data drift is detected in critical features.
  - Significant shifts in business metrics or user behavior that the current model cannot explain.
  - Major product changes are rolled out (e.g., Dates UX updates, new Bee AI features, changes in onboarding flow).

### 2.3 Shadow Deployment & A/B Testing
- **Comparison:** Before deploying a newly trained model, run it in shadow mode alongside the production model.
- **Validation:** Compare key metrics (AUC, propensity score distributions, high-intent share) between the new and old models to ensure improvement and stability.
- **A/B Testing:** For significant model changes, consider A/B testing in a controlled environment to measure the causal impact on business outcomes (e.g., Match→Message rate, OfflineProgressionEfficiency) before full rollout.

## 3. Iterative Improvement & Feedback Loop

### 3.1 Model Enhancements
- **Feature Engineering:** Continuously explore new features from evolving user interactions or external data sources.
- **Algorithm Exploration:** Evaluate more advanced modeling techniques (e.g., deep learning) if justified by business impact and resource availability.
- **Target Refinement:** Periodically review and refine the definition of ‘high-intent’ in collaboration with product and business stakeholders.

### 3.2 Stakeholder Feedback Integration
- **Regular Reviews:** Conduct monthly review meetings with product, CRM, and safety teams to gather feedback on model performance and insights.
- **Actionable Insights:** Translate model outputs and monitoring findings into actionable recommendations for product development and marketing campaigns.

## 4. Documentation & Governance

### 4.1 Model Card & Validation Summary Updates
- **Version Control:** Maintain versioned model cards (`08_reports/02_model_card_high_intent.md`) and validation summaries (`08_reports/04_model_validation_summary.md`) for each deployed model iteration.
- **Change Log:** Document all model changes, retraining events, and performance impacts in a central change log.

### 4.2 Peer Review & Audit
- **Code Review:** All changes to the modeling pipeline (Phase III notebook, scoring scripts) will undergo peer review.
- **Audit Trails:** Ensure all BigQuery queries and data transformations are auditable and reproducible.

## 5. Alignment with Bumble's Vision
This Phase VI plan ensures that the high-intent propensity model remains a dynamic and reliable asset, continuously adapting to user behavior and platform evolution, thereby supporting Bumble's quality reset strategy and commitment to intentional connections.
