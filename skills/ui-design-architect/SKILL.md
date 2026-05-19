---
name: ui-design-architect
description: Use this skill whenever the user asks for any UI design work — mockups, prototypes, wireframes, screens, components, visual redesign, page layouts, dashboards, console interfaces, design systems, or vague requests like "make this prettier", "design a screen for X", "let's do a UI for Y", or "redo this page". The skill encodes the architectural logic of professional UI design (both prototype-stage purpose/fidelity/Houde-Hill axes AND production-stage tokens/components/a11y) and forces an explicit project-fit diagnosis BEFORE any CSS or markup is written. Make sure to invoke this whenever the user mentions UI, design, mockup, prototype, screen, layout, component, visual, dashboard, or asks Claude to produce or revise anything visual — even if the user does not explicitly ask for design rigor. Without this skill, Claude tends to skip the architecture and jump straight to writing CSS by gut feel, producing styled markup that isn't real UI design.
---

# UI Design Architect

## Core principle

**Don't jump to CSS.** Real UI design is a sequence of architectural decisions before any pixel is placed. Skipping those decisions produces "styled markup" — code that runs but encodes no design reasoning. This skill enforces the sequence.

The sequence is **five phases**:

```
Phase 0 — Project-Fit Diagnosis    (figure out what this project actually needs right now)
Phase 1 — Purpose Declaration      (state what this artifact is testing/producing/answering)
Phase 2 — Fidelity Choice          (match the artifact to the question)
Phase 3 — Execution Standards      (build it with tokens/states/a11y, not hex/single-state/untested)
Phase 4 — Evaluation               (heuristic eval / cognitive walkthrough / N-user test)
```

Skip Phase 0 and you'll produce the wrong artifact for the project's state.  
Skip Phase 1-2 and you'll over-invest in fidelity that doesn't answer the question.  
Skip Phase 3 and you'll produce styled markup, not design.  
Skip Phase 4 and you'll never know if it works.

---

## Phase 0 — Project-Fit Diagnosis

**Always run this first.** Before producing any UI artifact, fill out this 7-question worksheet from project context and explicit user statements. If any answer is unclear, ASK the user — don't guess.

| # | Question | Why it matters |
|---|---|---|
| 1 | **Audience**: who will see this? (just the user / small team / external users / millions) | Determines whether a11y and polish thresholds matter, and how rigorous the design must be |
| 2 | **Lifecycle stage**: pre-MVP / MVP / iterating / shipping / production / maintenance | Decides whether sketches+exploration are still cheap, or whether token/state rigor is now required |
| 3 | **Immediate ask**: what's this UI artifact testing or producing? (concept / flow / visual direction / interaction detail / production-readiness / accessibility / token system) | Maps directly to Houde-Hill axis and fidelity (Phase 2) |
| 4 | **Disposability**: throwaway / evolves into code / production-bound | Determines whether to invest in maintainable architecture or to deliberately stay throwaway |
| 5 | **Existing artifacts**: none / sketches / mockups / design system / production design | Determines whether to build from scratch or inherit/extend |
| 6 | **Time budget**: hours / days / weeks | Hard constraint on fidelity choice |
| 7 | **Role split**: Claude designs + decides / Claude designs, user decides / Claude advises only / someone else designs | Decides whether Claude should propose, ask, or just execute |

**Output of Phase 0**: a brief paragraph (3-5 sentences) summarizing the project's state, written back to the user for confirmation. Example:

> "Project-fit reading: this is a personal-use tool (audience=1), in pre-MVP iterating stage. Immediate ask is visual-direction exploration. Artifact is throwaway (will be re-implemented by someone else). Existing assets: a 7-file mockup set in `tools/console/cv3design/`. Time budget: days. Role split: I propose, you decide. Sound right? If yes, proceeding to Phase 1."

**If Phase 0 reveals a contradiction** (e.g., user asks for hi-fi mockup but project is pre-MVP with unclear concept), surface the contradiction — that's more valuable than complying.

→ Full worksheet template: `templates/project-fit-diagnosis.md`

---

## Phase 1 — Purpose Declaration

Every prototype answers a question. Declaring the question first prevents over-investment.

**Two templates** (pick one):

**Template A · question-focused** (IDEO + Lean UX):
> "This artifact will test whether [user segment] can [goal/task] when presented with [interaction/surface], to validate that [hypothesis]."

**Template B · axis-focused** (Houde & Hill 1997):
> "This is a [Role | Look-and-Feel | Implementation] prototype to answer whether [specific question]."

**For evolutionary or production work**, add a **Lean UX hypothesis** (Gothelf):
> "We believe that [outcome] will be achieved if [people] attain [user outcome] with [feature]."

Write the purpose in 1-2 sentences. If the project is throwaway exploration and the question is "what does this look like?", that's a valid purpose — but state it. The act of writing it prevents drift.

→ Templates: `templates/purpose-statement.md`, `templates/hypothesis.md`

---

## Phase 2 — Fidelity Choice (Houde-Hill axis → fidelity)

### The Houde & Hill three axes

| Axis | What it asks | Right fidelity |
|---|---|---|
| **Role** | What does this artifact do for the user's life? | Sketch / paper / storyboard / Day-4 façade |
| **Look-and-Feel** | What's the sensory experience? | Sketch (for exploration) / mid-fi (for direction) / hi-fi (for sign-off) |
| **Implementation** | Can it actually work? | Code prototype (vertical slice) |

### The fidelity ladder (matched to questions)

| Fidelity | Tools | Answers well | Fails at | Time |
|---|---|---|---|---|
| **1. Paper sketch** | pen/paper, whiteboard | Concept exploration, ≥5 alternatives | Visual quality, micro-interaction | Minutes per variant |
| **2. Lo-fi wireframe** | Balsamiq (deliberately ugly), digital whiteboard | Layout, hierarchy, navigation | Animation, brand | Hours - 1 day |
| **3. Mid-fi (grayscale)** | Axure, Figma grayscale | Structural interaction, task flow | Visual sign-off | 1-2 days |
| **4. Hi-fi static** | Figma full-color | Visual design, typography, branding | Interaction (it's static!) | Days |
| **5. Clickable prototype** | Figma prototype, Keynote stitched | Flow logic, user comprehension of sequences | Performance, real data | 1 day (Sprint Day 4 façade) |
| **6. Code prototype** | Real code with mocks | Technical feasibility, integration, performance | Quick divergent exploration | Days - weeks |

### Decision tree (use this; don't guess)

```
1. Is primary axis Role or Look-and-Feel?
   ├─ Yes → 2
   └─ No (Implementation) → Build vertical code slice. EXIT.

2. Is purpose to EXPLORE multiple directions?
   ├─ Yes → Paper sketches, ≥5 alternatives, NN/g paper-prototype rules. EXIT.
   └─ No → 3

3. Is purpose to TEST one direction with users?
   ├─ Yes → 4
   └─ No → 5

4. Time ≤ 1 week + need quick user feedback?
   ├─ Yes → Day-4 façade (5-7 storyboard frames, clickable, 5-user test next day). EXIT.
   └─ No → Mid-fi wireframe + cognitive walkthrough. EXIT.

5. Is purpose to DECIDE visual direction (no user test yet)?
   ├─ Yes → Mid-fi → hi-fi static. Single direction. Annotate as "direction proposal". EXIT.
   └─ No → 6

6. Is purpose to PRODUCE ship-ready spec?
   ├─ Yes → Hi-fi + design tokens + state matrix + a11y audit. Go to Phase 3 execution standards.
   └─ No → STOP. Purpose unclear, return to Phase 1.
```

### Buxton's hard rule

Before committing to any one direction at mid-fi or higher: **≥5 sketch alternatives** of the key design decisions must exist. If they don't, go back to paper sketch first. This rule applies even for "small" decisions like "what's the visual metaphor for our candidate review?"

→ Full decision trees + cheat sheets: `references/decision-trees.md`

---

## Phase 3 — Execution Standards

Only run Phase 3 if Phase 2 landed on hi-fi static, clickable prototype, or production. For sketches and lo-fi, skip Phase 3 entirely — those phases are *supposed* to be rough.

### Hard requirements for hi-fi and above

1. **Tokens, not hex.** Every color must come from a 3-layer token system:
   - Primitive tokens (raw values): `--ref-palette-purple-90: #E8DEF8`
   - Semantic tokens (roles): `--color-surface`, `--color-on-surface`, `--color-accent`, `--color-accent-hover`
   - Component tokens (overrides): `--btn-primary-bg` (defaults to `--color-accent`)
   
2. **On-color pairing.** Every surface color has a paired `on-X` text color guaranteed to meet contrast ratio.

3. **State matrix per interactive component.** Each interactive component must have its full state set defined:
   ```
   default | hover | focused | active | disabled | loading | error | selected
   ```
   At minimum the first 5. Missing states = incomplete design.

4. **Type scale and spacing as named tokens.** Not "I'll use 14px here and 13px there". Pick a fixed set (Material 3's 15-token scale, or Refactoring UI's 7-size set, or Tailwind's defaults). Spacing follows a 4dp grid with named tokens (`--spacing-1` through `--spacing-10`).

5. **Motion tokens.** Duration in 3-5 tiers (`--motion-fast` ~150ms, `--motion-normal` ~250ms, `--motion-slow` ~400ms, `--motion-emphasized` ~500ms). Named easing curves. **Always include `@media (prefers-reduced-motion: reduce)` overrides.**

6. **WCAG 2.2 AA minimum:**
   - Text contrast ≥ 4.5:1 (normal text) or 3:1 (≥18pt or 14pt bold)
   - Non-text contrast ≥ 3:1 (UI components, graphical objects)
   - Touch target ≥ 24 × 24 CSS px
   - Visible focus indicator
   - All functionality keyboard-operable
   - Motion disable-able via OS setting

If any of these can't be met inside the time budget, **reduce the fidelity** rather than ship a hi-fi that violates them. Half-done hi-fi is worse than honest mid-fi.

→ Detailed token taxonomy, type scales, motion tokens, WCAG checklist: `references/design-foundations.md`

---

## Phase 4 — Evaluation

Don't ship without evaluating. Match the method to the artifact:

| Artifact | Evaluation |
|---|---|
| Sketch / lo-fi | Team critique (15-30 min), paper test with 1-3 users same day |
| Mid-fi / clickable | Cognitive walkthrough (NN/g 4 questions per step) + 5-user moderated test (Nielsen) |
| Hi-fi static | Heuristic evaluation (Nielsen's 10 heuristics, 3-5 evaluators) + stakeholder review |
| Production | All of the above + a11y audit (axe / Pa11y) + visual regression |

### Nielsen's 5-user law (the "why 5")

Formula: `N(1 - (1 - L)^n)`, where L ≈ 0.31, n = 5 yields ≈ 85% qualitative problem detection. Only valid for qualitative discovery; quantitative metrics need 30+. Don't claim "validated by users" with N < 5 moderated sessions.

→ Evaluation methods + templates: `references/prototype-foundations.md` (section on Evaluation)

---

## Anti-Pattern Self-Check

Run through this list after Phase 3. If you check any, fix before declaring done.

| # | Anti-pattern | Sign | Fix |
|---|---|---|---|
| 1 | Polished too early (visual investment before purpose validated) | Hex everywhere; spent hours on pixel alignment; unwilling to change direction | Strip to lo-fi; restate purpose; reduce timebox |
| 2 | Skipped sketch phase | Single direction explored; can't articulate "why not approach X" | Go back and produce ≥5 sketch alternatives for key decisions; even rough |
| 3 | Used real data/images too early | Reviewers comment on copy/content instead of structure | Replace with placeholder content |
| 4 | Treated mockup as spec | Handed static mockup to engineers; missing states/edge cases | Attach state matrix, edge case notes, acceptance criteria, OR generate proper design system handoff |
| 5 | Prototype code drifting to production | Throwaway code being merged without refactor | Tag as prototype; require quality gate (tests + a11y + perf) before any production merge |

---

## Project-Fit Quick Diagnosis Table

This is the operational core. Read across one row to see the "right move" for a project state.

| Audience | Stage | Existing assets | Time | → Right artifact |
|---|---|---|---|---|
| 1 (self) | Pre-MVP, exploring concept | None | Hours | Paper sketches, ≥5 alternatives |
| 1 (self) | Pre-MVP, picked direction | Sketches | 1-3 days | Mid-fi clickable, no token system yet |
| 1 (self) | Iterating, visual decisions ahead | Mid-fi | Days | Hi-fi static for the visual decisions only, throwaway |
| Small team | MVP testing | Mid-fi or hi-fi | 1-2 weeks | Hi-fi clickable + 5-user test |
| External users | Shipping | Hi-fi or production | Weeks | Token system + state matrices + a11y audit + handoff spec |
| Millions | Production | Full design system | Ongoing | Full DTCG token pipeline, multi-theme, component library, a11y CI, motion tokens, design QA before every release |
| Anyone | Maintenance / fix | Production | Hours-days | Diagnose against existing token system; do not add new tokens; minimal patch |

**If the requested artifact doesn't match the row, surface that mismatch.** E.g., "user asks hi-fi but is in pre-MVP exploring — recommend stepping back to sketches" is high-value feedback.

---

## When to read reference files

- **`references/design-foundations.md`** — Read when in Phase 3 and need to look up: token taxonomies, full type scales (Material 3 / Carbon / Tailwind), spacing grids, color systems (semantic + on-color), motion durations + easings, WCAG 2.2 specifics, design QA checklist. Also read when auditing existing UI.
- **`references/prototype-foundations.md`** — Read when in Phase 1-2 and need to look up: Houde-Hill axes details, Buxton's sketch-prototype distinction, Design Sprint 5-day methodology, Lean UX hypothesis canvas, evaluation methods (cognitive walkthrough steps, Nielsen 5-user formula derivation).
- **`references/decision-trees.md`** — Read when the SKILL.md decision tree above isn't enough and you need: branching fidelity decisions, IA artifact decisions (when to draw user flow vs. screens), throwaway-vs-evolutionary decision logic.

---

## Output discipline

When this skill is in play, every UI output Claude produces includes:

1. **Phase 0 reading**: 3-5 sentence project-fit diagnosis paragraph (or "previously diagnosed as: ..." if Phase 0 ran in an earlier turn)
2. **Purpose statement**: 1-2 sentences using Template A or B
3. **Fidelity declaration**: which step of the ladder, and why (mapped to Houde-Hill axis)
4. **Artifact**: the actual mockup/sketch/spec, executed to the standards of the declared fidelity
5. **What's NOT in this artifact**: explicit list of axes/aspects deferred (e.g., "Implementation axis not addressed — this is a Look-and-Feel artifact only")
6. **Evaluation recommendation**: what should be done with it next (heuristic eval / cognitive walkthrough / 5-user test / hand to engineering)

Steps 1-3 and 5-6 can be 1-2 sentences each; the artifact itself (step 4) is the bulk of the output. The framing is short and forces clarity.

---

## When NOT to use this skill

- User explicitly says "just make the change, skip the design framework" — comply
- Trivial CSS fix (e.g., "this button color is wrong, change it to #FF0000") — skip Phases 0-2, jump to execute, but check Phase 3 token compliance
- Code-only task (e.g., "make this React component memoized") with no visual change — irrelevant
- Documentation-only work — irrelevant

For anything else involving UI surface, use the skill.
