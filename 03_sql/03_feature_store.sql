-- 03_sql/03_feature_store.sql
-- Create features for modeling: rolling engagement, propensity to convert, and match quality signals

CREATE OR REPLACE VIEW `driiiportfolio.bumble_portfolio.features_for_modeling` AS

WITH ssot AS (
  SELECT *
  FROM `driiiportfolio.bumble_portfolio.ssot_members`
),

-- Event-level timestamps
event_times AS (
  SELECT
    user_id,
    event_ts,
    event_type
  FROM `driiiportfolio.bumble_portfolio.stg_events`
),

rolling AS (
  SELECT
    user_id,

    COUNTIF(event_type = 'session_start') OVER (
      PARTITION BY user_id
      ORDER BY UNIX_SECONDS(event_ts)
      RANGE BETWEEN 2592000 PRECEDING AND CURRENT ROW
    ) AS sessions_30d,

    COUNTIF(event_type = 'match') OVER (
      PARTITION BY user_id
      ORDER BY UNIX_SECONDS(event_ts)
      RANGE BETWEEN 2592000 PRECEDING AND CURRENT ROW
    ) AS matches_30d,

    COUNTIF(event_type = 'date_suggestion') OVER (
      PARTITION BY user_id
      ORDER BY UNIX_SECONDS(event_ts)
      RANGE BETWEEN 2592000 PRECEDING AND CURRENT ROW
    ) AS date_suggestions_30d,

    MAX(event_ts) OVER (
      PARTITION BY user_id
    ) AS last_event_ts

  FROM event_times
)

SELECT
  s.user_id,
  s.country,
  s.intent_level,
  s.is_paying,
  s.verification_passed,
  s.swipe_to_match_ratio,

  COALESCE(r.sessions_30d, 0) AS sessions_30d,
  COALESCE(r.matches_30d, 0) AS matches_30d,
  COALESCE(r.date_suggestions_30d, 0) AS date_suggestions_30d,

  -- propensity proxy
  SAFE_DIVIDE(
    COALESCE(r.matches_30d, 0),
    NULLIF(COALESCE(r.sessions_30d, 0), 0)
  ) AS match_rate_30d

FROM ssot s

LEFT JOIN (
  SELECT
    user_id,
    MAX(sessions_30d) AS sessions_30d,
    MAX(matches_30d) AS matches_30d,
    MAX(date_suggestions_30d) AS date_suggestions_30d
  FROM rolling
  GROUP BY user_id
) r
USING(user_id);