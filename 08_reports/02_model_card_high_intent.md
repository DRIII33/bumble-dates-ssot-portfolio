# Model Card — High‑Intent Propensity Model

## 1. Model Overview

- **Objective:** Estimate the probability that a member is **high‑intent**, defined as:
  - Verified (`verification_passed == 1`)
  - `match_rate_30d >= 0.15`
  - `sessions_30d >= 2`
- **Model Type:** Logistic Regression (binary classification)
- **Data Source:** `features_for_modeling` view in `driiiportfolio.bumble_portfolio`
- **Population:** Synthetic Bumble‑like users over a 30‑day window

## 2. Input Features

- `sessions_30d` — number of sessions in last 30 days  
- `matches_30d` — number of matches in last 30 days  
- `date_suggestions_30d` — number of date suggestions in last 30 days  
- `match_rate_30d` — matches_30d / sessions_30d  
- `swipe_to_match_ratio` — matches / swipes  
- `verification_passed` — 1 if selfie verification passed, else 0  

## 3. Performance

- **Metric:** ROC AUC on held‑out test set  
- **AUC:** ~0.75–0.85 (expected range; exact value from notebook)  
- **Class Balance:**  
  - Positive (high‑intent): ~X%  
  - Negative: ~100 − X%

## 4. Key Drivers (Feature Importance)

From logistic regression coefficients:

- **Strong Positive Drivers:**
  - `verification_passed` — verified users are substantially more likely to be high‑intent.
  - `match_rate_30d` — efficient conversion from sessions to matches is a strong signal of intent.

- **Moderate Positive Drivers:**
  - `sessions_30d` — more sessions generally increase the probability of high‑intent, up to a point.
  - `date_suggestions_30d` — members who move toward dates more often are more likely to be high‑intent.

- **Potential Negative / Weak Drivers:**
  - Very low `swipe_to_match_ratio` may indicate low quality or misaligned behavior.

## 5. Intended Use

- **Product:** Prioritize high‑intent members for:
  - AI‑guided profile improvements
  - “Dates” experience enhancements
  - Safety and verification nudges
- **Commercial:** Support pricing and premium feature experiments by identifying cohorts with high propensity to engage deeply.

## 6. Limitations

- Synthetic data; not calibrated to real Bumble distributions.
- Target definition is a proxy for “high‑intent” and may not capture all nuances.
- No fairness or bias analysis included (would be required in production).

## 7. Alignment with Role Expectations

- Demonstrates ability to:
  - Build behavioral segmentations and propensity models.
  - Connect model outputs to commercial and product strategy.
  - Communicate drivers and trade‑offs clearly to stakeholders.
