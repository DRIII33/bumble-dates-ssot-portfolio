-- 03_sql/02_transform_ssot.sql
-- Build a Single Source of Truth (ssot_members) combining user profile, verification, payments, and aggregated engagement

CREATE OR REPLACE VIEW `driiiportfolio.bumble_portfolio.ssot_members` AS
WITH users AS (
  SELECT
    user_id,
    signup_ts,
    country,
    zip_code,
    gender,
    SAFE_CAST(age AS INT64) AS age,
    intent_level,
    is_paying,
    initial_right_swipe_rate,
    is_pruned
  FROM `driiiportfolio.bumble_portfolio.stg_users`
),

verifications AS (
  SELECT
    user_id,
    verification_attempted,
    verification_passed,
    verification_ts
  FROM `driiiportfolio.bumble_portfolio.stg_verifications`
),

-- Aggregate events to compute engagement metrics
events AS (
  SELECT
    user_id,
    COUNTIF(event_type = 'session_start') AS sessions,
    COUNTIF(event_type = 'swipe') AS swipes,
    COUNTIF(event_type = 'match') AS matches,
    COUNTIF(event_type = 'date_suggestion') AS date_suggestions,
    MIN(event_ts) AS first_event_ts,
    MAX(event_ts) AS last_event_ts
  FROM `driiiportfolio.bumble_portfolio.stg_events`
  GROUP BY user_id
),

payments AS (
  SELECT
    user_id,
    COUNT(*) AS payment_count,
    SUM(amount) AS total_spend,
    MAX(payment_ts) AS last_payment_ts
  FROM `driiiportfolio.bumble_portfolio.stg_payments`
  GROUP BY user_id
),

-- Message-level sentiment aggregation
messages AS (
  SELECT
    m.match_id,
    COUNT(*) AS message_count,
    SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) AS positive_msgs,
    SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_msgs
  FROM `driiiportfolio.bumble_portfolio.stg_messages` m
  GROUP BY m.match_id
),

-- Match-level join to compute per-user offline progression proxies
matches AS (
  SELECT
    match_id,
    user_id,
    partner_id,
    match_ts,
    match_source,
    partner_verified
  FROM `driiiportfolio.bumble_portfolio.stg_matches`
)

-- Final SSOT
SELECT
  u.user_id,
  u.signup_ts,
  u.country,
  u.zip_code,
  u.gender,
  u.age,
  u.intent_level,

  COALESCE(v.verification_passed, 0) AS verification_passed,

  COALESCE(e.sessions, 0) AS sessions,
  COALESCE(e.swipes, 0) AS swipes,
  COALESCE(e.matches, 0) AS matches,
  COALESCE(e.date_suggestions, 0) AS date_suggestions,

  COALESCE(p.payment_count, 0) AS payment_count,
  COALESCE(p.total_spend, 0.0) AS total_spend,

  u.is_paying,
  u.is_pruned,

  -- Derived KPIs
  SAFE_DIVIDE(
    COALESCE(e.matches, 0),
    NULLIF(COALESCE(e.swipes, 0), 0)
  ) AS swipe_to_match_ratio,

  SAFE_DIVIDE(
    COALESCE(p.total_spend, 0),
    NULLIF(COALESCE(p.payment_count, 0), 0)
  ) AS avg_payment_amount,

  -- Recency
  TIMESTAMP_DIFF(
    CURRENT_TIMESTAMP(),
    COALESCE(e.last_event_ts, u.signup_ts),
    DAY
  ) AS days_since_last_event

FROM users u
LEFT JOIN verifications v USING(user_id)
LEFT JOIN events e USING(user_id)
LEFT JOIN payments p USING(user_id);