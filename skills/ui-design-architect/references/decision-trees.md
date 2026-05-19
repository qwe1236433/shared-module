# Decision Trees & Cheat Sheets · Reference

> Compact lookup for moments when the SKILL.md tree isn't enough. Use for branching fidelity decisions, IA artifact decisions, and throwaway-vs-evolutionary disambiguation.

---

## 1. Master decision tree (full version)

```
START — user asks for UI work
   ↓
PHASE 0 — Project-Fit Diagnosis
   ├─ Run the 7-question worksheet (see templates/project-fit-diagnosis.md)
   ├─ Surface contradictions if any (e.g., hi-fi requested but concept unclear)
   └─ Confirm reading with user
   ↓
PHASE 1 — Purpose Declaration
   ├─ Pick Template A (question-focused) or B (axis-focused)
   ├─ For evolutionary/production work, ALSO write Gothelf hypothesis
   └─ Write 1-2 sentences, attach to artifact
   ↓
PHASE 2 — Fidelity Choice
   │
   ├─ Q1: Is primary Houde-Hill axis Role or Look-and-Feel?
   │     ├─ NO (it's Implementation) → Build vertical code slice. EXIT.
   │     └─ YES ↓
   │
   ├─ Q2: Is the purpose to EXPLORE alternatives?
   │     ├─ YES → Paper sketches, ≥5 alternatives, ≤1 day each. EXIT to Phase 4.
   │     └─ NO ↓
   │
   ├─ Q3: Is the purpose to TEST with real users?
   │     ├─ YES ↓
   │     │     ├─ Time ≤ 1 week + need quick feedback?
   │     │     │     ├─ YES → Day-4 façade (5-7 frames, 1 day). EXIT to Phase 4 (5-user test).
   │     │     │     └─ NO → Mid-fi wireframe + cognitive walkthrough. EXIT to Phase 4.
   │     └─ NO ↓
   │
   ├─ Q4: Is the purpose to DECIDE visual direction (with stakeholder)?
   │     ├─ YES → Mid-fi → hi-fi static, single direction, "direction proposal". EXIT to Phase 4 (heuristic review).
   │     └─ NO ↓
   │
   ├─ Q5: Is the purpose to PRODUCE ship-ready spec?
   │     ├─ YES → Go to Phase 3 (full execution standards).
   │     └─ NO → STOP. Purpose unclear, return to Phase 1.
   ↓
PHASE 3 — Execution (if ship-ready or hi-fi)
   ├─ Token system (3 layers)
   ├─ Type scale (fixed set)
   ├─ Spacing tokens (4dp grid)
   ├─ State matrices per interactive component
   ├─ Motion tokens + prefers-reduced-motion
   └─ WCAG 2.2 AA pass
   ↓
PHASE 4 — Evaluation
   ├─ Match method to fidelity:
   │     - Sketch/lo-fi → critique + 1-3 paper tests
   │     - Mid-fi/clickable → cognitive walkthrough + 5-user
   │     - Hi-fi → heuristic eval (3-5 reviewers) + stakeholder review
   │     - Production → all above + a11y audit + visual regression
   └─ Synthesize, decide next experiment
```

---

## 2. Cheat sheet — "what's the right fidelity for my question?"

| If the question is... | Right fidelity | Right evaluation |
|---|---|---|
| "Does this concept make sense?" | Paper sketch | Team critique |
| "Which of these 3 approaches works best?" | Lo-fi sketches × 3 | Stakeholder + paper test |
| "Can users find / understand X?" | Lo-fi or mid-fi clickable | 5-user moderated test |
| "Does this look right?" | Hi-fi static | Heuristic eval (3-5 reviewers) |
| "Does the flow feel natural?" | Mid-fi clickable | Cognitive walkthrough + 5-user test |
| "Can we actually build this?" | Code prototype (vertical slice) | Engineering review |
| "Should we A/B test these?" | Hi-fi or coded variants | Quantitative A/B with N≥30 per arm |
| "Is this production-ready?" | Production design + tokens | a11y audit + visual regression + heuristic eval |

---

## 3. IA artifact decision tree

```
START — about to draw screens
   ↓
Q1: Is task logic, branching, or navigation undecided?
   ├─ YES → Draw user flow FIRST (5-7 nodes, entry/success/failure)
   └─ NO ↓
Q2: Are there multiple distinct user journeys?
   ├─ YES → Draw site map + user flows for each
   └─ NO ↓
Q3: Are there modals, branching dialogs, or progressive disclosure?
   ├─ YES → Draw state machine for the complex interaction(s)
   └─ NO ↓
Q4: Is the interaction linear and primarily visual?
   ├─ YES → Skip IA artifacts, go straight to screens
   └─ NO → Default: light user flow before screens (5-7 nodes)
```

---

## 4. Throwaway vs Evolutionary disambiguation

```
START — building a prototype
   ↓
Q1: Will any of this code or artifact ship as production?
   ├─ NO → THROWAWAY. Tag explicitly. Use fast tools (Figma, HTML mockup).
   └─ YES ↓
Q2: Are the core requirements stable for the components being prototyped?
   ├─ NO → STOP — still in throwaway territory until requirements settle.
   └─ YES ↓
Q3: Is the team committed to refactor + quality-gate before merging to production?
   ├─ NO → STAY throwaway. The risk of "prototype quality in production" is too high.
   └─ YES ↓
Q4: Can the system be decomposed into vertical slices?
   ├─ YES → INCREMENTAL (slice by slice, each with its own quality gate)
   └─ NO → EVOLUTIONARY (whole prototype evolves; require explicit refactor checkpoints)
```

**Key rule**: defaulting to throwaway is almost always safer when in doubt. Migration cost is far lower than the cost of accidentally shipping prototype quality.

---

## 5. Evaluation method picker

```
Artifact at hand:
   ↓
SKETCH or LO-FI
   → 15-min team critique
   → Optional: 1-3 paper tests same day

MID-FI WIREFRAME
   → Cognitive walkthrough (NN/g 4 questions per step)
   → Optional: 5 moderated tests if time

HI-FI STATIC (no interaction)
   → Heuristic evaluation (3-5 reviewers, Nielsen 10)
   → Stakeholder review for visual sign-off
   → SKIP user testing (static can't be tested for interaction)

HI-FI CLICKABLE (façade or Figma prototype)
   → 5 moderated user tests with think-aloud (45-60 min each)
   → Cognitive walkthrough by team beforehand
   → Heuristic review by 1-2 reviewers beforehand

CODE PROTOTYPE
   → Engineering validation (perf, integration, edge cases)
   → Light user test (3-5 users) for end-to-end flow
   → a11y automated check (axe / Pa11y)

PRODUCTION DESIGN
   → All of the above
   → Quantitative metrics tracking (need N≥30 for stat sig)
   → Visual regression suite
   → a11y CI gate
```

---

## 6. Quick "is my work good?" self-check

Before declaring any UI work done, run through:

| ✓ | Check |
|---|---|
| ☐ | Did Phase 0 produce a project-fit reading? |
| ☐ | Is the purpose statement attached (1-2 sentences)? |
| ☐ | Does the chosen fidelity match the primary Houde-Hill axis? |
| ☐ | If hi-fi or above: are tokens (not hex) the source of values? |
| ☐ | If interactive component: are min 5 states defined? |
| ☐ | If motion present: is `prefers-reduced-motion` handled? |
| ☐ | Does the artifact pass WCAG 2.2 AA on contrast / focus / target size? |
| ☐ | Is the evaluation method picked and queued? |
| ☐ | Is the output annotated with what's NOT included (skipped axes, deferred concerns)? |

If any unchecked: don't declare done yet.

---

## 7. Common project-fit patterns (with right move)

| Pattern | Likely right move |
|---|---|
| "User asks for hi-fi mockup, project still pre-MVP" | Push back: propose lo-fi sketches first, ≥5 alternatives |
| "User asks for token system, current product has 0 designs" | Push back: too early for tokens; start with sketches → mid-fi |
| "User asks for production design system, audience is 1 person" | Push back: audience doesn't justify the cost; suggest minimal token system instead |
| "User asks for new feature mockup, design system exists" | Inherit from design system; don't build from scratch |
| "User has hi-fi mockup, wants 'a real prototype'" | Add interactivity layer (Figma prototype) + test plan; don't redo visuals |
| "User says 'make it prettier'" | Phase 0 ask: prettier for whom? Drives whether to invest tokens or to do a quick visual pass |
| "User wants 7 screens designed in 2 hours" | Constraints force lo-fi or façade; flag the time/quality tradeoff explicitly |
| "User wants the design 'production-ready' but it's never been user-tested" | Hi-fi for sign-off OK, but flag: no user validation = not actually production-ready |
