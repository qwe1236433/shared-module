# Prototype Foundations · Reference

> Detailed reference for Phases 1-2 (Purpose Declaration + Fidelity Choice) and Phase 4 (Evaluation). Read when deciding what kind of prototype to build, or when planning to evaluate one.
>
> **Contents**: Houde & Hill three-axis model, Buxton's sketch-vs-prototype, fidelity ladder details, throwaway-vs-evolutionary, Google Design Sprint, Lean UX hypothesis, IA artifacts, evaluation methods, anti-patterns.

---

## 1. Purpose declaration — why it matters

Houde & Hill 1997 ([PDF](https://hci.stanford.edu/courses/cs247/2012/readings/WhatDoPrototypesPrototype.pdf)) frame the discipline:

> "the art of identifying the most important open design questions, and building only what is needed to answer them"

Without a purpose statement attached to the artifact, the prototype drifts. The build becomes about "what looks cool" instead of "what answers the question." Reviewers comment on irrelevant aspects. Hours are wasted.

### Two templates

**Template A · question-focused (IDEO + Lean UX style):**
> "This prototype will test whether [user segment] can [goal/task] when presented with [interaction/surface], to validate that [outcome]."

Example:
> "This prototype will test whether first-time buyers can complete a 3-step pre-qualification flow on mobile when shown a simplified progress indicator, to validate that fewer fields increase completion."

**Template B · axis-focused (Houde & Hill):**
> "This is a [Role | Look-and-Feel | Implementation] prototype to answer whether [specific question]."

Example:
> "This is a Role + Look-and-Feel prototype to answer whether the onboarding narrative makes the user understand the product's purpose."

### Lean UX hypothesis (Gothelf, used in build-measure-learn)

Verbatim template from Jeff Gothelf:
> "We believe that [outcome] will be achieved if [people] attain [user outcome] with [feature]."

Example:
> "We believe we will increase mortgage application completion by 55% if first-time homebuyers don't have to prepare documents upfront with an integrated end-to-end process."

The hypothesis is testable. It says what success looks like in measurable terms.

---

## 2. Houde & Hill — the three axes (canonical theory)

| Axis | Verbatim definition | Right fidelity |
|---|---|---|
| **Role** | "the purpose or function an artifact serves in a user's life" | Sketch / paper / storyboard / Day-4 façade |
| **Look-and-Feel** | "the concrete sensory experience of using a design before the final solution exists" | Sketch (exploration) / mid-fi (direction) / hi-fi (sign-off) |
| **Implementation** | "the artifact's ability to perform its intended functions" | Code prototype (vertical slice) |

### Classic examples

- **Role + Look-and-Feel maximum**: Apple's 1987 *Knowledge Navigator* concept video. Looked like a real product, did nothing. Communicated "what is this thing."
- **Implementation maximum**: a code vertical slice. Looks crude, but proves "it can run end-to-end."

### Mapping method (5 steps)

1. Write purpose statement (Template A or B above)
2. Map the question to one or more axes; mark primary
3. Pick fidelity matching primary axis:
   - Role / Look-and-Feel → paper, façade, storyboard
   - Implementation → vertical code slice
4. Scope minimally — build only what exercises the axis
5. Choose evaluation method accordingly (see §8 below)

### Common misuse

Producing hi-fi visuals when the primary question is "does this concept make sense?" — that's a Role question, answered better by paper sketches at 1/100 the cost. The hi-fi visuals lock in irreversible commitments before the concept is validated.

---

## 3. Buxton — sketch vs prototype distinction

Bill Buxton ([Sketches vs Prototypes PDF](https://cs.cmu.edu/~bam/uicourse/Buxton-SketchesPrototypes.pdf)):

> "Sketches are disposable, unfinished, and ask questions. Prototypes answer questions and suggest concrete designs."

### Generate-then-test loop

```
Diverge (sketch many)
   ↓
Converge (critique + vote → pick 1-2)
   ↓
Prototype (refine the chosen direction)
   ↓
Test (real users)
   ↓
Loop back to sketch if new directions emerge
```

### Hard rule: ≥5 sketch alternatives before prototyping

Before committing to hi-fi for any key design decision, ≥5 distinct conceptual sketches must exist. This forces exploration of the design space rather than crystallizing the first idea.

"Key design decisions" include:
- Core visual metaphor (e.g., "how do we represent N candidates?")
- Major interaction pattern (e.g., "how does user move between steps?")
- Information hierarchy (e.g., "what goes top, what goes side?")

Not every micro-detail needs 5 sketches — but the load-bearing decisions do.

### Exit criteria for sketch phase

- ≥5 distinct alternatives drawn
- Primary learning objective written and mapped to Houde-Hill axis
- Team / stakeholder agreement on evaluation plan

### Entry criteria for prototype phase

- Purpose statement attached
- Fidelity chosen, timebox set
- Evaluation method chosen

---

## 4. Fidelity ladder · detailed

| Fidelity | Best questions | Worst questions | Tools | Typical time |
|---|---|---|---|---|
| **1. Paper sketch** | Concept, flow, hierarchy, 5+ alternatives | Visual quality, task time, animation, brand | Pen, paper, whiteboard, Sharpie | Minutes per variant |
| **2. Lo-fi wireframe** | Layout, hierarchy, navigation, content grouping | Animation, brand, emotion | Balsamiq (deliberately ugly), digital whiteboard | Hours to 1 day |
| **3. Mid-fi grayscale** | Structural interactions, task flows, element placement | Brand validation, micro-interaction polish | Axure, Figma grayscale | 1-2 days |
| **4. Hi-fi static** | Visual design, typography, brand sign-off | Interaction logic (static can't be tested) | Figma full-color | Days per key screen |
| **5. Interactive prototype** | Flow logic, basic interactivity, sequence comprehension | Performance, real data, edge cases | Figma prototype, Keynote stitched, ProtoPie | 1 day for façade (Sprint Day 4 model) |
| **6. Code prototype** | Technical feasibility, integration, performance | Quick divergent exploration | Real code with mocks | Days to weeks |

### Empirical finding (MeasuringU)

Lo-fi and hi-fi prototypes find **similar qualitative usability problems**, but lo-fi underestimates task times and aesthetic reactions. Translation: if your question is "can users figure this out", don't waste time on hi-fi yet.

### Scope guidance

Hi-fi interactive prototypes: **5-15 screens** is the typical target. More than that wastes investment; fewer than that doesn't cover the flow.

---

## 5. Throwaway vs Evolutionary vs Incremental

Source: Ian Sommerville's software engineering text.

| Type | Intent | Risk |
|---|---|---|
| **Throwaway** | Build fast to learn requirements / usability, then discard | Very low IF discard is enforced; high if it secretly migrates to production |
| **Evolutionary** | Start with a working core, iterate features, becomes production | Tech debt; prototype-quality code in production |
| **Incremental** | Decompose into vertical slices, prototype each independently, then integrate | Integration risk between slices |

### Vertical vs Horizontal

- **Vertical**: a few components built to full functionality (deep, narrow)
- **Horizontal**: many components built to surface only (wide, shallow)

**Trap**: horizontal prototypes give the team a false sense of completion. Validating technical feasibility requires vertical slices.

### Decision criteria

Choose **throwaway** when:
- Main risk is "requirements / usability still fuzzy"
- Need to compare multiple concepts fast
- Tools chosen for speed, not production

Choose **evolutionary** when:
- Requirements stable for the core
- Team accepts maintaining + extending into production (with explicit refactor plan)
- Quality gates defined (tests, a11y, security, refactor) before prototype code merges to prod

Choose **incremental** when:
- System decomposable, risk localized to specific components

### The migration trap

If evolutionary prototype code drifts to production without a refactor, you've shipped prototype quality. Mitigation: **tag prototype code explicitly**, gate any production merge behind tests + a11y + perf + security review.

---

## 6. Google Design Sprint (1-week structure)

Source: [GV Sprint](https://gv.com/sprint/), [Jake Knapp's book *Sprint*](https://thesprintbook.com)

| Day | Phase | Output |
|---|---|---|
| Monday | Understand / Map | Expert interviews + problem map |
| Tuesday | Sketch | Each person produces multiple solution sketches |
| Wednesday | Decide | Vote, pick storyboard |
| Thursday | Prototype | **Realistic façade** built in 1 day |
| Friday | Test | 5 user moderated sessions |

### The Day-4 façade

Key properties:
- Looks real, doesn't need to function
- "Goldilocks" fidelity — not too rough, not too polished
- 5-7 storyboard frames (max ~15)
- Tools: Figma, Keynote, Illustrator, paper, whatever
- Team roles: maker, stitcher, content owner
- Time: 1 day total

### Day-5 test (the "5 users" rule)

Tests the Day-4 prototype with 5 target users, 45-60 minutes each, moderated, with think-aloud protocol. Immediate synthesis afterward.

### Sprint 2.0 variant

Knapp later compressed to 4 days (combining Mon+Tue). Use if time-pressed.

---

## 7. Lean UX (Gothelf) · hypothesis-driven prototyping

Source: [Lean UX Canvas v4](https://jeffgothelf.com/wp-content/uploads/2016/12/LeanUX_canvas_v4.pdf), [Jeff Gothelf](https://jeffgothelf.com)

### Build-Measure-Learn (Think-Make-Check) loop

```
Hypothesis (Gothelf template)
   ↓
Build (smallest prototype that can invalidate the hypothesis)
   ↓
Measure (defined metric, qualitative or quantitative)
   ↓
Learn (pivot / persevere / iterate)
   ↓
Back to hypothesis
```

### Process checklist (5 steps per hypothesis)

1. Write hypothesis using Gothelf template; attach measurable metric
2. Map to Houde-Hill axis; choose fidelity
3. Build the minimum that can invalidate (MVP / minimal prototype) in timebox
4. Measure — qualitative (5 users) or quantitative (30+, telemetry)
5. Learn — decide pivot / persevere / iterate

### Pragmatic application

If signal is qualitative (comprehension, flow), use lo/mid-fi + 5-user test.  
If signal is quantitative (conversion %), use higher fidelity or code prototype + larger sample.

Don't use hi-fi for a hypothesis whose signal is qualitative — wastes investment.

---

## 8. IA / user flow artifacts — precede the visual prototype

### Artifact types

| Artifact | Use | When |
|---|---|---|
| **Information Architecture (IA)** | Content organization, naming | Project start |
| **Sitemap** | Top-level hierarchy | After IA |
| **User flow / task flow** | User's path through tasks with decision points | Before lo-fi screens |
| **State machine / screen graph** | Branching interaction logic | When modals / disclosure / branches exist |

### Decision rule: user flow vs. screens first

**Draw user flow first when:**
- Task logic, branching, or navigation undecided
- Multiple journeys exist
- Risk of rework on screens is high

**Draw screens first when:**
- Interaction is linear
- Primary question is visual, not navigational
- (Map this via Houde-Hill axis)

### Minimum artifacts for a Sprint-scale exercise

- 1-page sitemap covering only the prototype's scope
- 5-7 node user flow with entry / success / failure states annotated

---

## 9. Prototype evaluation methods

### Cognitive Walkthrough (Wharton, Rieman, Lewis, Polson)

Per step, ask the 4 core questions:
1. Will the user try to do this step? (matches goal)
2. Will the user notice the action is available? (visibility)
3. Will the user connect the action to the goal? (label / affordance)
4. After acting, will the user feel progress toward goal? (feedback)

**Steps to run:**
1. Pick target task
2. Prepare persona + context
3. Team walks each step, asks the 4 questions
4. Log problems + severity

### Heuristic Evaluation (Nielsen's 10 heuristics)

Method: 3-5 evaluators independently review the artifact against a set of heuristics. Compile findings, rate severity, prioritize fixes.

The canonical 10 are Jakob Nielsen's. They're widely cited; refer to [NN/g — 10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/) for the authoritative list.

Run time: 30-60 min per evaluator. Synthesis: another 30-60 min.

### Usability Testing — Nielsen's 5-user rule

Formula: **N(1 - (1 - L)^n)** where:
- N = total problems to be found
- L = probability one user finds one problem (empirically ≈ 0.31)
- n = number of users

For n=5, ≈ 85% problem detection. This is the basis for Sprint Day-5's 5-user test.

**Important caveats** (MeasuringU's reflection):
- 5 users is for *qualitative* problem discovery only
- Low-incidence problems (affecting 10% of users) need many more participants
- Quantitative metrics (conversion, time-on-task) need 30+ users for statistical reliability

**Don't claim "validated by users" with N<5 moderated sessions.**

### Combined evaluation plan (typical single-prototype experiment)

| Step | Activity | Time |
|---|---|---|
| 1 | Heuristic review, 1-3 evaluators | 30-60 min each |
| 2 | Cognitive walkthrough, team workshop | 1-2 hours |
| 3 | Moderated usability test, 5 users, 45-60 min each, think-aloud | 5-6 hours total |
| 4 | Synthesis, decide next experiment | Half day |

---

## 10. Anti-patterns

| # | Anti-pattern | Diagnosis signs | Remediation |
|---|---|---|---|
| 1 | **Polishing too early** | Slow builds; reluctance to change direction; reviewers focus on polish | Revert to lo-fi; require purpose statement before visual investment |
| 2 | **Skipping sketch phase** | Single direction only; can't articulate alternatives | Buxton rule: ≥5 sketch variants before prototype |
| 3 | **Real data / images too early** | Reviewers comment on copy/content, not flow | Use placeholder content; annotate assumptions |
| 4 | **Treating mockup as spec** | Missing states; missing edge cases; engineering tickets just reference images | Attach state matrix + acceptance criteria; or generate proper design system handoff |
| 5 | **Prototype code into production** | Prototype branches merged without refactor; no tests, no a11y, no security review | Explicitly tag prototype code; require quality gate before any production merge |

---

## 11. Foundational readings

| Work | Why |
|---|---|
| Houde & Hill — *What do prototypes prototype?* (1997) | The canonical Role/Look-and-Feel/Implementation axes; foundation of prototype purpose declaration |
| Bill Buxton — *Sketching User Experiences* | Sketch-vs-prototype distinction, generate-then-test loop, ≥5 alternatives rule |
| Jake Knapp — *Sprint* (GV book) | 5-day structured prototype-and-test, Day-4 façade, Day-5 5-user test |
| Jeff Gothelf — *Lean UX* | Hypothesis-driven prototyping, canvas, build-measure-learn loop |
| Ian Sommerville — *Software Engineering* (Ch.10) | Throwaway vs evolutionary definitions and engineering tradeoffs |
| Steve Krug — *Don't Make Me Think* | Practical usability testing, the 3-second test |
| Alan Cooper — *About Face* | Goal-directed design, persona-driven prototyping |
| Jakob Nielsen — *Why You Only Need to Test with 5 Users* (NN/g article) | The mathematical basis for small qualitative tests |

---

## References (URLs)

- [Houde & Hill 1997 PDF](https://hci.stanford.edu/courses/cs247/2012/readings/WhatDoPrototypesPrototype.pdf)
- [Buxton — Sketches vs Prototypes PDF](https://cs.cmu.edu/~bam/uicourse/Buxton-SketchesPrototypes.pdf)
- [GV Sprint](https://gv.com/sprint/)
- [NN/g — Prototype Specifications](https://nngroup.com/articles/prototype-specifications/)
- [NN/g — Cognitive Walkthrough Workshop](https://nngroup.com/articles/cognitive-walkthrough-workshop/)
- [NN/g — Why 5 Users](https://nngroup.com/articles/why-you-only-need-to-test-with-5-users/)
- [NN/g — 10 Usability Heuristics](https://nngroup.com/articles/ten-usability-heuristics/)
- [Sommerville Ch.10 PDF](https://shms-prod.s3.amazonaws.com/media/editor/146581/Se10.pdf)
- [Jeff Gothelf hypothesis template](https://jeffgothelf.com/blog/how-i-break-down-hypotheses-to-make-them-easier-to-test/)
- [IDEO Design Kit](https://ideo.com/journal/design-kit-the-human-centered-design-toolkit)
- [Atlassian Design Sprint](https://atlassian.com/agile/design/design-sprint)
- [MeasuringU — Prototype Fidelity](https://measuringu.com/prototype-fidelity/)
- [UsabilityBOK — Cognitive Walkthrough](https://usabilitybok.org/cognitive-walkthrough)
