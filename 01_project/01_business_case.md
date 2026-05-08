### Project Framing & Business Scenario

**Data Scientist:** Daniel Rodriguez III

**Top challenges (extracted):**  
- **Quality reset trade-off (Pruning vs. Scale):** balancing a deliberate 21.1% reduction in paying users with network-effect risks.   
- **Modeling intent beyond swipes:** moving from binary swipe signals to richer “Dates” and intent/storytelling signals.   
- **Causal measurement & incrementality:** product changes (removing swipe → Dates) require causal frameworks beyond short A/B tests.   
- **AI orchestration & safety:** integrating the front-facing “Bee” assistant while preserving authenticity and refining safety models (Private Detector).   
- **Marketplace dynamics & multi-sided trade-offs:** ensuring balanced discovery across gender, intent, and geography.

**Business Problem (DRI scenario):**  
You are the **Directly Responsible Individual (DRI)** Data Scientist in Bumble’s Austin Core Data Science team. Your mission is to **design, implement, and operationalize an end-to-end measurement and modeling pipeline** that (1) creates a Single Source of Truth (SSOT) for member behavior across the new “Dates” experience, (2) produces behavioral segmentations and propensity models that optimize offline progression and ARPPU, and (3) delivers causal evidence on the Dates rollout and AI “Bee” interventions while preserving safety and marketplace balance.

> **Two sentences from the research document:** “The Data Scientist is responsible for uncovering the drivers of member behavior and performance, providing the insights that inform the 2026 product overhaul.” “The company has deliberately pruned its user base to prioritize intentional, engaged members, resulting in a 21.1% decrease in paying users to 3.2 million.”
