# Project-Fit Diagnosis · Worksheet Template

> Fill this out at the start of any UI design task. Take answers from the project's existing context (CLAUDE.md, docs, recent conversation) where possible. Ask the user for anything that's unclear. **Do not skip questions.**

---

## The 7 questions

### 1. Audience

Who will see this UI?

- [ ] Just the user themselves (personal tool)
- [ ] Small internal team (≤10)
- [ ] Small external users (10-1000)
- [ ] Large external users (1k-1M)
- [ ] Millions
- [ ] Unknown

**Why it matters**: Determines rigor floor for a11y, polish, internationalization, and the cost-benefit of a full token system.

### 2. Lifecycle stage

Where is the product right now?

- [ ] Pre-MVP, concept exploration
- [ ] Pre-MVP, direction picked
- [ ] MVP, gathering feedback
- [ ] MVP → product, iterating
- [ ] Production, shipping
- [ ] Production, maintenance / bug-fix

**Why it matters**: Decides whether sketches+exploration are still cheap (early) or whether token rigor + state matrices are now required (late).

### 3. Immediate ask

What is this specific UI artifact for? (pick the most accurate)

- [ ] **Explore** — generate multiple direction candidates
- [ ] **Decide** — pick one direction from candidates
- [ ] **Validate flow** — does the user task complete?
- [ ] **Validate visual** — does the look match intent?
- [ ] **Validate interaction** — do micro-interactions feel right?
- [ ] **Produce** — ship-ready design for engineering
- [ ] **Fix** — solve a specific reported problem
- [ ] **Audit** — assess existing UI work

**Why it matters**: Maps directly to Houde-Hill axis and fidelity choice.

### 4. Disposability

What happens to this artifact after the immediate ask is done?

- [ ] **Throwaway** — discarded; serves only as reference
- [ ] **Evolves** — same code/files extended into production
- [ ] **Production** — goes live as-is or near-as-is

**Why it matters**: Throwaway permits speed and rough edges. Evolutionary demands quality gates. Production demands full token + state + a11y rigor.

### 5. Existing artifacts

What's already been built or designed?

- [ ] None — greenfield
- [ ] Some sketches / notes
- [ ] Lo-fi or mid-fi mockups
- [ ] Hi-fi mockups
- [ ] Partial design system (some tokens, some components)
- [ ] Full design system in active use
- [ ] Existing production design

**Why it matters**: Determines whether to extend / inherit / replace. Inheriting from existing is almost always right when a system exists.

### 6. Time budget

How much time is available before next milestone?

- [ ] Minutes — 1 quick fix
- [ ] Hours — a session of work
- [ ] 1-2 days
- [ ] A week
- [ ] Multiple weeks
- [ ] Open-ended

**Why it matters**: Hard ceiling on fidelity. Even if fidelity is "right" for the question, if it doesn't fit the budget, drop down a level rather than ship half-baked hi-fi.

### 7. Role split

Who decides what?

- [ ] Claude designs + decides (full agency)
- [ ] Claude designs, user decides (Claude proposes, user picks)
- [ ] Claude advises, user / someone else designs
- [ ] Claude executes (user gives explicit spec, Claude implements)

**Why it matters**: Determines whether Claude should propose alternatives, ask questions, or just execute. Affects the entire interaction style.

---

## Output

After answering all 7, write 3-5 sentences summarizing the reading and confirm with the user. Example:

> "Project-fit reading: this is a personal-use tool (audience=1), in iterating stage (MVP, gathering own feedback). Immediate ask is to validate visual direction. Artifact will be throwaway (you mentioned this is for visual reference, will be re-implemented separately). Existing assets: 7-file hi-fi mockup set in `tools/console/cv3design/`. Time budget: a few days. Role split: I propose, you decide. Does this match your reading? If yes, I'll move to Phase 1 (purpose declaration)."

---

## What to do with the reading

| If reading suggests... | Action |
|---|---|
| Pre-MVP + asking for hi-fi | Push back. Recommend stepping down to sketches first. |
| Production + audience>1k + no token system | Push back. Token system precedes production design. |
| Throwaway + asking for full design system | Push back. ROI doesn't justify. Minimal token set instead. |
| Inherits from existing design system | Good. Use existing tokens; don't fork. |
| Time budget incompatible with fidelity ask | Surface the tradeoff. Propose dropping fidelity OR extending time. |
| Role split = "Claude executes from spec" | Skip Phase 1-2 proposals; go straight to execute against the spec. |
| Anything contradictory | Surface contradiction explicitly. Ask user to resolve before proceeding. |
