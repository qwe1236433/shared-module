# Purpose Statement · Templates

> Pick A or B. Write 1-2 sentences. Attach to the artifact (top of file, or in a sibling note). Without this, the build drifts.

---

## Template A · Question-focused (IDEO / Lean UX)

```
This [artifact type] will test whether [user segment] can [goal/task] 
when presented with [interaction/surface], 
to validate that [outcome/hypothesis].
```

### Examples

**Example 1 (validating a flow):**
> "This clickable prototype will test whether first-time users can complete the 3-step onboarding when presented with progressive disclosure of feature explanations, to validate that fewer upfront fields increase completion."

**Example 2 (validating a concept):**
> "This sketch set will test whether power users can understand a tree-vs-graph layout choice for the relations browser, to validate that the visual metaphor matches their existing mental model."

**Example 3 (testing visual direction):**
> "This hi-fi mockup will test whether the user agrees that the 'instrument-not-decoration' visual stance comes across through restrained color, geometric type, and absence of brand chrome, to validate the direction before token-system work begins."

---

## Template B · Axis-focused (Houde & Hill 1997)

```
This is a [Role | Look-and-Feel | Implementation] prototype 
to answer whether [specific question].
```

Recall the axes:
- **Role** = what does this thing do in the user's life?
- **Look-and-Feel** = what's the sensory experience?
- **Implementation** = can it actually work?

### Examples

**Example 1 (Role only):**
> "This is a Role prototype to answer whether the user understands what the system is for, after seeing only the 7-step pipeline diagram (no actual UI)."

**Example 2 (Look-and-Feel primary, Role secondary):**
> "This is a Look-and-Feel + Role prototype to answer whether the dual-gate review interface conveys the 'commitment then redemption' tension, in addition to whether the overall layout makes the user feel they're using an instrument rather than a decoration."

**Example 3 (Implementation only):**
> "This is an Implementation prototype to answer whether the candidate-solver can return top-K results within 3 seconds for a typical 5000-word chapter, using mock data through the real API endpoint."

---

## Multi-axis declaration

For artifacts that legitimately span multiple axes, state the primary axis first, then secondary:

```
Primary: Look-and-Feel — does the visual stance read as "instrument"?
Secondary: Role — does the flow communicate what the system is for?
Explicitly skipped: Implementation — mock data only, real API not wired.
```

**The "explicitly skipped" line is high-value.** It tells future reviewers (and yourself) what NOT to evaluate this artifact against.

---

## What makes a purpose statement bad

| Bad | Why | Fix |
|---|---|---|
| "Design the dashboard" | No question being answered | "This will test whether [user] can [task] when shown [layout]..." |
| "Make it look professional" | Subjective, untestable | "Test whether [audience] perceives [trait] vs [competitor A, B]" |
| "Iterate on v2" | No purpose, just label | "This iteration tests whether [specific change] resolves [specific issue from v1 feedback]" |
| "Build the MVP" | Scope-only, no question | "MVP tests hypothesis: [Gothelf template]" |

A good purpose statement makes "is this artifact done?" answerable. If you can't tell from the statement whether the artifact succeeded, the statement is too vague.

---

## When to write a purpose statement

- **Always at the start of a Phase 1** — non-negotiable for any UI design task
- Updated if scope changes mid-build
- Re-stated at the top of evaluation sessions
- Embedded in the artifact (e.g., as a comment in the HTML, or a header in the Figma file)
