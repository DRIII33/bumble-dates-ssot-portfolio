# Looker Studio Dashboard Specification — High‑Intent Propensity & Behavioral Segmentation

## 1. Data Sources
- `bumble_portfolio.ssot_members`
- `bumble_portfolio.features_for_modeling`
- `bumble_portfolio.propensity_scores`

All tables are refreshed daily.

---

## 2. Dashboard Pages & Components

### Page 1 — Executive Overview
**KPIs**
- Total Users  
- High‑Intent Share  
- Verification Rate  
- Avg Sessions (30d)  
- Avg Matches (30d)  

**Visuals**
- Engagement Funnel (sessions → matches → dates)
- Cluster Distribution (pie or bar)
- High‑Intent Trend Over Time (line chart)

---

### Page 2 — Behavioral Segmentation
**Visuals**
- Cluster Profiles (bar chart)
  - sessions_30d  
  - matches_30d  
  - match_rate_30d  
- Cluster‑Level Verification Rate  
- Cluster‑Level High‑Intent Share  
- Cluster‑Level Propensity Score Distribution  

**Tables**
- Top 10% users by propensity score within each cluster

---

### Page 3 — High‑Intent Propensity
**Visuals**
- Propensity Score Histogram  
- Propensity Score by Gender  
- Propensity Score by Intent Level  
- SHAP Summary Plot (imported as image)  

**KPIs**
- High‑Intent Users (count)  
- Avg Propensity Score  

---

### Page 4 — Safety & Verification
**Visuals**
- Verification_passed Distribution  
- High‑Intent vs. Unverified Comparison  
- Sessions_30d by Verification Status  
- Matches_30d by Verification Status  

---

### Page 5 — Dates Feature Insights
**Visuals**
- date_suggestions_30d Distribution  
- High‑Intent Propensity vs. Date Suggestions  
- Cluster 2 (“Dates‑Forward Users”) Deep Dive  
- Sessions → Matches → Dates Funnel for Cluster 2  

---

## 3. Filters
- Gender  
- Intent Level  
- Country  
- Verification Status  
- Cluster  
- Propensity Score Range  

---

## 4. Dashboard Refresh
- Daily refresh  
- Propensity scores updated via batch scoring pipeline  

---

## 5. Stakeholder Usage
- **Product:** Identify segments needing UX improvements  
- **CRM:** Target high‑propensity users for nudges  
- **Safety:** Monitor verification and sentiment patterns  
- **Commercial:** Understand monetization potential of high‑intent users  
