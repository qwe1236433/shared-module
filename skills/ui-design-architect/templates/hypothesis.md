# Hypothesis · Template (Lean UX / Gothelf)

> For evolutionary or production work, add a measurable hypothesis on top of the purpose statement. Source: Jeff Gothelf's Lean UX writing.

---

## Canonical template

```
We believe that [outcome]
will be achieved if [people]
attain [user outcome]
with [feature].
```

### Components

- **[outcome]** = business / product outcome (measurable). e.g., "increased completion rates by 30%"
- **[people]** = specific user segment. e.g., "first-time visitors", "logged-in editors"
- **[user outcome]** = what the user gets / can do. e.g., "finish setup in under 5 minutes"
- **[feature]** = what we'll build to enable this. e.g., "guided wizard with progress indicator"

---

## Examples

**Example 1 (Gothelf's own, mortgage application):**
> "We believe we will increase mortgage application completion rates by 55% if first-time homebuyers don't have to prepare any documents upfront with a broadly integrated, end-to-end mortgage application process."

**Example 2 (onboarding):**
> "We believe we will reduce time-to-first-action by 50% if new users can complete signup in under 90 seconds with a single-form, no-confirmation-email signup flow."

**Example 3 (feature engagement):**
> "We believe we will double monthly active usage of the report builder if mid-tier customers can save and re-run reports with a saved-reports panel in the sidebar."

---

## Why measurable matters

The whole point of the hypothesis is that you can **invalidate** it. If after building and measuring, the metric didn't move, you've learned the hypothesis was wrong. Without a measurable outcome, you can never invalidate, and the hypothesis is just an opinion.

| Vague (bad) | Measurable (good) |
|---|---|
| "Users will be happier" | "NPS will increase by 5 points" |
| "More users will sign up" | "Trial-to-paid conversion will increase from 4% to 6%" |
| "It will be easier to find features" | "Time-to-find for the 'export' action will drop below 8 seconds (currently 22s)" |
| "The new flow will be better" | "Drop-off in step 3 will decrease from 40% to <25%" |

---

## Build the smallest prototype that can invalidate

After writing the hypothesis, ask: **what's the cheapest artifact that would tell me the hypothesis is wrong?**

- If the signal is qualitative (comprehension, comfort, confusion) → lo-fi or mid-fi + 5-user moderated test
- If the signal is quantitative (% completion, conversion) → hi-fi clickable or coded variant + ≥30 users / A/B

**Don't build hi-fi for a hypothesis whose signal is qualitative.** That's over-investment and the result of skipping this question.

---

## Measure honestly

After the test:

1. Did the measured signal change in the predicted direction?
2. By how much?
3. Was it statistically significant (for quantitative)?
4. What surprised you?

Three possible outcomes:
- **Persevere** — hypothesis confirmed, keep building this direction
- **Pivot** — hypothesis invalidated, change direction
- **Iterate** — hypothesis partially confirmed, refine and re-test

The reason for the loop is *learning*, not validating opinions. If every hypothesis "confirms", you're probably writing them too soft.

---

## When NOT to write a hypothesis

- Purely throwaway exploration (sketches comparing concepts) — purpose statement is enough
- Visual direction calls (taste decisions) — purpose statement is enough
- Pure technical implementation prototypes — hypothesis is about engineering criteria, not user outcome

Reserve the hypothesis template for user-facing experiments where there's a real metric to move.
