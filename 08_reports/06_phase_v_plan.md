# Phase V — Deployment, Dashboards, and Causal Measurement Framework

## 1. Deployment Strategy

### 1.1 Model Packaging
- The high‑intent propensity model (Logistic Regression or XGBoost) is exported as:
  - Serialized model artifact (`.pkl`)
  - Feature schema (`feature_cols.json`)
  - Preprocessing pipeline (scaler, fill‑na logic)
- All transformations are documented in the Phase III notebook and reproducible from BigQuery views.

### 1.2 Batch Scoring Pipeline
Because this is a portfolio project (and BigQuery ML is disabled), the recommended deployment pattern is:

1. **Daily BigQuery extract**  
   ```sql
   SELECT * FROM features_for_modeling;
   ```
2. **Colab / Python batch scoring script**  
   - Loads model artifact  
   - Scores all users  
   - Writes results back to BigQuery as a table:
     ```
     bumble_portfolio.propensity_scores
     ```
3. **Looker Studio connects to the scored table** for visualization.

This mirrors Bumble’s real workflow where batch scoring is common for segmentation and CRM targeting.

### 1.3 Scored Table Schema
```
user_id STRING
propensity_score FLOAT64
cluster INT64
is_high_intent INT64
scored_ts TIMESTAMP
```

### 1.4 Shadow Deployment (Recommended)
Before “promoting” a new model:

- Compare new vs. old model AUC
- Compare distribution of propensity scores
- Compare high‑intent share
- Validate no unexpected shifts in:
  - sessions_30d
  - matches_30d
  - verification_passed

This ensures stability and prevents regressions.

---

## 2. Dashboarding Strategy (Looker Studio)

The goal is to make the model **actionable** for product, CRM, and commercial teams.

Dashboards will be built on:

- `ssot_members`
- `features_for_modeling`
- `propensity_scores`

### 2.1 Dashboard Pages

#### **Page 1 — Executive Overview**
- Total users
- High‑intent share
- Verification rate
- Engagement funnel (sessions → matches → dates)
- Cluster distribution

#### **Page 2 — Behavioral Segmentation**
- Cluster profiles (sessions, matches, match_rate_30d)
- Cluster‑level verification rates
- Cluster‑level high‑intent propensity

#### **Page 3 — High‑Intent Propensity**
- Propensity score distribution
- Top drivers (from SHAP)
- High‑intent users by geography, gender, intent_level

#### **Page 4 — Safety & Verification**
- Verification_passed distribution
- High‑intent vs. unverified comparison
- Sentiment distribution (if added later)

#### **Page 5 — Dates Feature Insights**
- date_suggestions_30d distribution
- High‑intent propensity by date_suggestions_30d
- Cluster 2 (“Dates‑forward users”) deep dive

---

## 3. Causal Measurement Framework

This section outlines how Bumble would evaluate product changes such as:

- Dates UX improvements  
- Bee AI prompts  
- Profile guidance nudges  

### 3.1 Causal Question
**“Did the intervention increase high‑intent behavior?”**

### 3.2 Recommended Methods

#### **A. Difference‑in‑Differences (DiD)**
Use when you have:

- A clear rollout date  
- A control group unaffected by the change  

Example:
```
pre_period: 30 days before rollout
post_period: 30 days after rollout
```

Outcome:
- sessions_30d
- matches_30d
- is_high_intent

#### **B. Synthetic Control**
Use when:

- No natural control group exists  
- Rollout is global  

Construct a synthetic baseline using pre‑rollout trends.

#### **C. Propensity‑Matched Experiments**
Use your high‑intent model to:

- Match users on baseline behavior  
- Compare outcomes between treated vs. untreated groups  

This is especially useful for CRM nudges or profile guidance prompts.

### 3.3 Measurement Framework Outputs
- Uplift in high‑intent share  
- Uplift in match_rate_30d  
- Uplift in date_suggestions_30d  
- Uplift in verification_passed (if intervention targets safety)

---

## 4. Operationalization & Governance

### 4.1 Monitoring
- Weekly AUC  
- Drift in feature distributions  
- Drift in propensity score distribution  
- Drift in cluster composition  

### 4.2 Retraining Triggers
Retrain when:

- AUC drops > 0.05  
- High‑intent share shifts > 20%  
- Major product changes occur (Dates, Bee AI, onboarding flow)

### 4.3 Documentation
- Model card  
- Validation summary  
- Peer review checklist  
- Dashboard spec  
- Causal measurement plan  

This completes Phase V.
