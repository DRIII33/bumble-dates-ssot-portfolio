# Causal Strategy: Synthetic Control, Difference-in-Differences

## 1. Objective
To rigorously evaluate the causal impact of product changes, such as the 'Dates' rollout and AI 'Bee' interventions, on key member behaviors and business outcomes (e.g., long-term retention, offline progression, ARPPU).

## 2. Challenges & Considerations
- **Quality Reset Trade-off:** Evaluating the impact of a deliberate user base reduction (pruning) requires careful baseline considerations.
- **Network Effects:** Changes can have ripple effects across the ecosystem, complicating direct measurement.
- **Confounding Factors:** External events or simultaneous product changes can obscure the true causal impact.
- **Long-term vs. Short-term Effects:** Short A/B tests may not capture the full, sustained impact of behavioral shifts.

## 3. Recommended Causal Frameworks

### 3.1 Difference-in-Differences (DiD)
**When to use:** Ideal for interventions with a clear start date and an identifiable control group that is similar to the treated group but not exposed to the intervention.

**Application to Bumble:**
- **Dates Rollout Evaluation:** If the 'Dates' feature is rolled out regionally or to specific user cohorts, DiD can compare the change in outcomes (e.g., `date_suggestions_30d`, `match_rate_30d`, `is_high_intent`) for the treated group before and after the rollout, against the change for an unexposed control group over the same period.
- **AI 'Bee' Interventions:** Similar application if the AI nudges are introduced to specific user segments or geographies.

**Key Metrics to Measure (Post-Intervention Uplift):**
- `sessions_30d`
- `matches_30d`
- `date_suggestions_30d`
- `match_rate_30d`
- `verification_passed`
- `is_high_intent`

**Methodology:**
1. **Identify Treated & Control Groups:** Select a group exposed to the intervention and a comparable group not exposed.
2. **Define Pre & Post Periods:** Establish a time window before and after the intervention.
3. **Calculate Change in Outcome:** Measure the difference in average outcome for both groups between the pre and post periods.
4. **Estimate Causal Effect:** The DiD estimate is the difference between the change in the treated group and the change in the control group.

### 3.2 Synthetic Control Method (SCM)
**When to use:** When a natural, comparable control group is not available, especially for interventions rolled out at a macro level (e.g., national launch, global policy change).

**Application to Bumble:**
- **Dates Rollout (Global/Large Scale):** If the 'Dates' feature is rolled out across a large portion of the user base without a clear, unexposed control group.
- **Algorithmic Pruning Impact (from research context):** To assess the long-term impact of the 21.1% user base reduction on overall platform health, ARPPU, or marketplace balance, by constructing a counterfactual 'Bumble' that didn't prune.

**Methodology:**
1. **Select Control Units:** Identify similar (non-treated) units (e.g., other regions not receiving the feature, or historical data from Bumble itself before the change). In a synthetic data context, this would involve carefully constructed user groups.
2. **Construct Synthetic Control:** Create a weighted combination of control units that best resembles the treated unit's pre-intervention trends for key outcome variables.
3. **Compare Trends:** Observe the difference in outcome trends between the treated unit and its synthetic control in the post-intervention period.

### 3.3 Propensity Score Matching (PSM)
**When to use:** To balance covariates between treatment and control groups in observational studies, or to select comparable control units for A/B tests to ensure validity.

**Application to Bumble:**
- **Targeted AI Nudges:** When testing the impact of AI 'Bee' prompts on user behavior, use the high-intent propensity model to match users with similar propensities, ensuring treatment and control groups are balanced on relevant covariates.
- **User Segmentation for Experimentation:** Create balanced comparison groups for experiments focusing on specific behavioral segments.

**Methodology:**
1. **Estimate Propensity Scores:** Use a logistic regression model (like the high-intent propensity model) to predict the probability of receiving treatment (e.g., being exposed to a new feature) based on pre-treatment characteristics.
2. **Match Units:** Pair treated and control units with similar propensity scores.
3. **Estimate Treatment Effect:** Compare outcomes between matched pairs.

## 4. Measurement & Incrementality
- **Long-Window Metrics:** Focus on longer-term outcomes (e.g., 90-day retention, 60-day conversion to paying) to capture sustained behavioral shifts beyond immediate engagement spikes.
- **ARPPU & Offline Progression:** Directly measure the impact on key business metrics outlined in the success metrics document (`01_project/02_success_metrics.md`).
- **Guardrail Metrics:** Continuously monitor safety incidents, swipe-to-match ratio, and message sentiment to ensure product changes do not negatively impact platform health or user experience.
