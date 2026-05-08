# SHAP Interpretability — High‑Intent Propensity Model

## 1. Purpose
SHAP (SHapley Additive exPlanations) provides local and global interpretability for the XGBoost model.  
It explains **how each feature contributes to each individual prediction** and **which features matter most overall**.

---

## 2. SHAP Setup (Python)

```python
import shap

# Initialize SHAP explainer for XGBoost
explainer = shap.TreeExplainer(xgb)
shap_values = explainer.shap_values(X_test)

# Summary plot (global importance)
shap.summary_plot(shap_values, X_test, feature_names=feature_cols)
```

This produces a global importance plot showing:

- sessions_30d  
- matches_30d  
- match_rate_30d  
- verification_passed  
- date_suggestions_30d  
- swipe_to_match_ratio  

ranked by contribution to predictions.

---

## 3. Interpretation of SHAP Summary Plot

### 3.1 Global Insights
- **sessions_30d** is the strongest driver of high‑intent predictions.  
- **matches_30d** and **match_rate_30d** also contribute significantly.  
- **verification_passed** has a strong positive effect when present.  
- **date_suggestions_30d** and **swipe_to_match_ratio** have weaker contributions.

These findings align with:

- Logistic regression coefficients  
- RandomForest feature importance  
- XGBoost feature importance  

This triangulation increases trust in the model.

---

## 4. Local Interpretability (Individual Users)

Example:

```python
# Force plot for a single user
shap.force_plot(
    explainer.expected_value,
    shap_values[0,:],
    X_test.iloc[0,:],
    matplotlib=True
)
```

This shows:

- Which features pushed the prediction **toward** high‑intent  
- Which features pushed it **away** from high‑intent  

Useful for:

- CRM targeting  
- Product debugging  
- Understanding edge cases  

---

## 5. Business Interpretation

### 5.1 What SHAP Confirms
- High‑intent users are characterized by **consistent engagement** (sessions_30d).  
- **Match success** (matches_30d, match_rate_30d) is a strong indicator of intent.  
- **Verification** is a key safety and intent signal.  

### 5.2 How Stakeholders Use This
- **Product:** Improve onboarding for low‑engagement users.  
- **CRM:** Target users with high sessions but low matches (Cluster 3).  
- **Safety:** Reinforce verification nudges.  
- **Commercial:** Identify high‑propensity segments for premium features.  

---

## 6. Limitations of SHAP in This Context
- Synthetic data may exaggerate feature separability.  
- SHAP values reflect the model’s learned patterns, not causal relationships.  
- Ratio features may show unstable SHAP values due to multicollinearity.  

---

**Conclusion:**  
SHAP provides a transparent, stakeholder‑friendly explanation of the XGBoost model’s behavior. Combined with clustering, logistic regression, and feature importance, it completes a robust interpretability package for the high‑intent propensity model.
