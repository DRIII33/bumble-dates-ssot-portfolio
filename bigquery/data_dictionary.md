# Data Dictionary — Bumble Portfolio BigQuery Dataset

## Dataset: `driiiportfolio.bumble_portfolio`

---

## 1. Staging Tables

### 1.1 `stg_users`
- `user_id` (STRING) — Unique user identifier  
- `signup_ts` (TIMESTAMP) — Signup timestamp  
- `country` (STRING) — Country code  
- `zip_code` (INT64) — Zip/postal code  
- `gender` (STRING) — Gender  
- `age` (FLOAT64) — Age  
- `intent_level` (STRING) — Stated intent (casual, friendship, intentional)  
- `is_paying` (INT64) — 1 if paying user, else 0  
- `initial_right_swipe_rate` (FLOAT64) — Initial swipe behavior  
- `is_pruned` (INT64) — 1 if pruned in quality reset, else 0  

### 1.2 `stg_events`
- `event_id` (STRING)  
- `user_id` (STRING)  
- `event_type` (STRING) — e.g., session_start, swipe, match  
- `event_ts` (TIMESTAMP)  
- `device` (STRING)  
- `app_version` (STRING)  

### 1.3 `stg_matches`
- `match_id` (STRING)  
- `user_id` (STRING)  
- `partner_id` (STRING)  
- `match_ts` (TIMESTAMP)  
- `match_source` (STRING)  
- `partner_verified` (INT64)  

### 1.4 `stg_messages`
- `message_id` (STRING)  
- `match_id` (STRING)  
- `sender_id` (STRING)  
- `text` (STRING)  
- `sentiment` (STRING)  
- `message_ts` (TIMESTAMP)  

### 1.5 `stg_payments`
- `payment_id` (STRING)  
- `user_id` (STRING)  
- `amount` (FLOAT64)  
- `currency` (STRING)  
- `payment_ts` (TIMESTAMP)  
- `payment_method` (STRING)  

### 1.6 `stg_verifications`
- `user_id` (STRING)  
- `verification_attempted` (INT64)  
- `verification_passed` (INT64)  
- `verification_ts` (TIMESTAMP)  

---

## 2. Core Views

### 2.1 `ssot_members`
Member‑level Single Source of Truth (SSOT). Typical fields:

- `user_id` (STRING)  
- `signup_ts` (TIMESTAMP)  
- `country` (STRING)  
- `gender` (STRING)  
- `intent_level` (STRING)  
- `is_paying` (INT64)  
- `is_pruned` (INT64)  
- `verification_passed` (INT64)  
- `sessions_30d` (FLOAT64) — Sessions in last 30 days  
- `matches_30d` (FLOAT64) — Matches in last 30 days  
- `date_suggestions_30d` (FLOAT64) — Date suggestions in last 30 days  
- `match_rate_30d` (FLOAT64) — Matches per session (SAFE_DIVIDE)  
- `swipe_to_match_ratio` (FLOAT64) — Matches per swipe (SAFE_DIVIDE)  

### 2.2 `features_for_modeling`
Feature store for clustering and propensity modeling. Typical fields:

- `user_id` (STRING)  
- `gender` (STRING)  
- `country` (STRING)  
- `intent_level` (STRING)  
- `verification_passed` (INT64)  
- `sessions_30d` (FLOAT64)  
- `matches_30d` (FLOAT64)  
- `date_suggestions_30d` (FLOAT64)  
- `match_rate_30d` (FLOAT64)  
- `swipe_to_match_ratio` (FLOAT64)  
- `cluster` (INT64) — Assigned in modeling pipeline (may be written back)  

---

## 3. Scoring Table & Views

### 3.1 `propensity_scores_raw` (TABLE)
- `user_id` (STRING)  
- `propensity_score` (FLOAT64) — Model‑predicted probability of high‑intent  
- `cluster` (INT64) — Behavioral cluster assignment  
- `is_high_intent` (INT64) — 1 if high‑intent (per target definition), else 0  
- `scored_ts` (TIMESTAMP) — Scoring timestamp  

### 3.2 `propensity_scores` (VIEW)
- Same fields as `propensity_scores_raw`, exposed as a view for Looker Studio.

---

## 4. Reporting Views

### 4.1 `cluster_profiles`
- `cluster` (INT64)  
- `avg_sessions_30d` (FLOAT64)  
- `avg_matches_30d` (FLOAT64)  
- `avg_date_suggestions_30d` (FLOAT64)  
- `avg_match_rate_30d` (FLOAT64)  
- `avg_swipe_to_match_ratio` (FLOAT64)  
- `verification_rate` (FLOAT64) — Avg of `verification_passed`  

### 4.2 `high_intent_summary`
- `is_high_intent` (INT64)  
- `user_count` (INT64)  
- `avg_sessions_30d` (FLOAT64)  
- `avg_matches_30d` (FLOAT64)  
- `avg_match_rate_30d` (FLOAT64)  
- `verification_rate` (FLOAT64)  

### 4.3 `dates_feature_insights`
- `user_id` (STRING)  
- `date_suggestions_30d` (FLOAT64)  
- `sessions_30d` (FLOAT64)  
- `matches_30d` (FLOAT64)  
- `match_rate_30d` (FLOAT64)  
- `swipe_to_match_ratio` (FLOAT64)  
- `cluster` (INT64)  
- `propensity_score` (FLOAT64)  
- `is_high_intent` (INT64)  

### 4.4 `safety_verification_summary`
- `verification_passed` (INT64)  
- `user_count` (INT64)  
- `avg_sessions_30d` (FLOAT64)  
- `avg_matches_30d` (FLOAT64)  
- `avg_match_rate_30d` (FLOAT64)  
- `avg_propensity_score` (FLOAT64)  
- `high_intent_rate` (FLOAT64)  

---

This data dictionary reflects the structures you’ve actually used and described throughout the project—no invented fields, no extra tables.
