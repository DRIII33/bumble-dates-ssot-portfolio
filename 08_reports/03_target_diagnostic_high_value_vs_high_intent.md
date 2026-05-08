# Target Diagnostic — From “High‑Value” to “High‑Intent”

## 1. Initial Target: `is_high_value`

**Definition (initial):**

```python
is_high_value = (match_rate_30d >= 0.3) & (sessions_30d >= 5)
```

When evaluated:

- Positive rate ≈ **0.002%** (0.00002 as a fraction)
- This means only a tiny handful of users were labeled high‑value.

### 1.1 Why This Was a Problem

- **Extreme class imbalance:** With only 0.002% positives, the model would:
  - Struggle to learn meaningful patterns.
  - Be highly unstable and sensitive to noise.
  - Likely default to predicting the negative class.
- **Synthetic data constraints:** The synthetic generation process did not produce enough users with both very high match_rate and high sessions simultaneously.

In practice, Bumble would either:
- Relax the definition, or
- Use a different outcome that better reflects the business question.

---

## 2. Revised Target: `is_high_intent`

To create a more usable and business‑aligned target, we defined:

```python
is_high_intent = (
    (verification_passed == 1) &
    (match_rate_30d >= 0.15) &
    (sessions_30d >= 2)
)
```

### 2.1 Why This Works Better

- **Positive rate:** In a more reasonable range (e.g., 3–15%), enabling:
  - Stable training
  - Meaningful AUC
  - Sensible calibration
- **Business alignment:**
  - Incorporates **verification**, which is central to Bumble’s safety strategy.
  - Uses **match_rate_30d** and **sessions_30d** to capture both quality and engagement.
  - Reflects Bumble’s 2026 “quality reset” focus on intentional, verified members.

---

## 3. Lessons (What This Shows About the Candidate)

- Recognizes when a target is **statistically unusable** (extreme imbalance).
- Can **re‑frame the problem** to align with:
  - Data realities
  - Business strategy
  - Modeling best practices
- Demonstrates the kind of **diagnostic thinking** expected in a Core Data Science role.

In a real Bumble setting, this same reasoning would be applied to:
- Funnel conversion targets
- Retention outcomes
- Safety incident reduction metrics
- Monetization and ARPPU uplift definitions
