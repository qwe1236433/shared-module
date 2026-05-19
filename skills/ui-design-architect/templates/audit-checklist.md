# UI Audit Checklist · 8-Layer Self-Audit

> Run this against any existing UI work to surface where it's "styled markup" vs. real UI design. Each layer has a binary "compliant" check and a "fix path" if not.

---

## Layer 0 — Design principles

| ✓ | Check | If failing |
|---|---|---|
| ☐ | Project has 3-5 written design principles | Write them. Examples: "instrument over chrome", "reveal reasoning", "restraint over decoration" |
| ☐ | Each visible UI decision can be justified by ≥1 principle | If not, either the principle is missing or the decision is arbitrary |

---

## Layer 1 — Design tokens (3 layers)

| ✓ | Check | If failing |
|---|---|---|
| ☐ | Primitive tokens defined (raw color values, etc.) | Create `tokens/primitive.json` or equivalent |
| ☐ | Semantic tokens defined (surface, on-surface, accent, etc.) | Create semantic mapping referencing primitives |
| ☐ | On-color pairs exist (every surface has paired text color) | Add `on-X` for each `X` surface |
| ☐ | Component tokens defined (per-component overrides) | Add for each component variant |
| ☐ | No hex codes in component CSS (everything is `var(--token)`) | `grep -r "#[0-9A-Fa-f]\{6\}"` in component files; replace each |

---

## Layer 2 — Typography

| ✓ | Check | If failing |
|---|---|---|
| ☐ | Type scale is a fixed set of ≤15 named tokens | Audit all `font-size:` usages; collapse to nearest scale value |
| ☐ | Body text is ≥16px on mobile | Increase or document the exception |
| ☐ | Line heights are derived (heading ratio, body ratio) | Apply Refactoring UI: 1.0-1.25 heading, 1.5-1.75 body |
| ☐ | Weights are limited (4-5 max: 300, 400, 500, 600, 700) | Remove unused weights, reduce font payload |
| ☐ | Font families are limited (≤3) | Remove or consolidate |
| ☐ | No `em` units for type sizing (px or rem only) | Find/replace |

---

## Layer 3 — Spacing & layout

| ✓ | Check | If failing |
|---|---|---|
| ☐ | Spacing follows 4dp (or 8pt) grid | Audit all `margin/padding/gap`; round to nearest grid value |
| ☐ | Spacing values are named tokens (`--space-1` through `--space-10`) | Replace raw values with tokens |
| ☐ | Breakpoints are explicit and named | Define `--bp-sm/md/lg/xl` and use consistently |
| ☐ | Container max-width defined per breakpoint | Add or document why uncapped |

---

## Layer 4 — Color states

| ✓ | Check | If failing |
|---|---|---|
| ☐ | Every interactive component has hover state defined | Add `:hover` rules |
| ☐ | Every interactive component has focus state visible | Add `:focus-visible` rules (NOT `outline: none` without replacement) |
| ☐ | Every interactive component has active state | Add `:active` rules |
| ☐ | Every interactive component has disabled state | Add `:disabled` or `[aria-disabled="true"]` rules |
| ☐ | Forms have error / validation states | Add `[aria-invalid="true"]` rules |
| ☐ | Async components have loading state | Add `[aria-busy="true"]` rules |
| ☐ | State colors come from state tokens, not hex | `--color-state-success`, `--color-state-warning`, `--color-state-danger`, `--color-state-info` |

---

## Layer 5 — Components

| ✓ | Check | If failing |
|---|---|---|
| ☐ | Repeated patterns extracted into reusable components | Identify duplicates; extract |
| ☐ | Each component has a documented anatomy (named parts) | Document in MDX or comment |
| ☐ | Each component lists its variants | E.g., Button: filled / outlined / text / ghost |
| ☐ | Each component lists its states (5 min) | Default/hover/focused/active/disabled |
| ☐ | Components compose; don't hard-code children | E.g., `<Card>` accepts arbitrary children, doesn't bake structure |

---

## Layer 6 — Motion

| ✓ | Check | If failing |
|---|---|---|
| ☐ | Duration values are tokens (3-5 tiers) | `--motion-fast/normal/medium/slow` |
| ☐ | Easing curves are named tokens | `--ease-standard/decelerate/accelerate` |
| ☐ | No `transition: all` (specific properties only) | Replace `all` with explicit property list |
| ☐ | `@media (prefers-reduced-motion: reduce)` is implemented | Add the media query; zero out durations or set to `transition: none` |
| ☐ | Motion is purposeful (not on every interaction) | Review; remove decorative-only animations |
| ☐ | Entering animations longer than exiting (200ms out, 400ms in pattern) | Adjust if reversed |

---

## Layer 7 — Accessibility (WCAG 2.2 AA)

| ✓ | Check | Threshold | If failing |
|---|---|---|---|
| ☐ | Text contrast | ≥4.5:1 normal, ≥3:1 large | Test with axe / WebAIM contrast checker; adjust |
| ☐ | UI component contrast | ≥3:1 | Audit borders, icons, focus rings |
| ☐ | Touch target size | ≥24×24 CSS px | Increase via padding |
| ☐ | Focus visible on every interactive element | Visible at 3:1 contrast against unfocused | Add `:focus-visible` rules |
| ☐ | Keyboard reaches every action | Tab through entire UI | Add `tabindex` only where necessary |
| ☐ | Screen reader semantics correct | `<button>` not `<div onClick>`; ARIA where needed | Refactor; add ARIA |
| ☐ | Zoom to 200% holds layout | No horizontal scroll, no overlap | Fix responsive bugs |
| ☐ | All motion has reduce-motion fallback | (Layer 6) | (See Layer 6) |

---

## Layer 8 — Design QA & handoff

| ✓ | Check | If failing |
|---|---|---|
| ☐ | Purpose statement attached to artifact | Write it (templates/purpose-statement.md) |
| ☐ | Houde-Hill axis declared | Add: "This is a [axis] artifact" |
| ☐ | Throwaway / evolutionary / production declared | Add explicit tag |
| ☐ | Evaluation method ran (heuristic / walkthrough / N-user test) | Run one; document findings |
| ☐ | Anti-patterns checked (see prototype-foundations.md §10) | Self-check; fix any |
| ☐ | If handoff to engineering: state matrix + edge cases + acceptance criteria attached | Write or generate |

---

## How to use this checklist

1. **Initial audit**: walk the 8 layers, mark each check ✓ or ☐
2. **Tally**: count ☐ per layer
3. **Prioritize fixes**:
   - Layer 7 (a11y) failures = ship-blockers if audience is external
   - Layer 1 (tokens) failures = scalability blockers; fix before scaling
   - Layer 5 (components) failures = maintenance debt; fix during scale-up
   - Layer 6 (motion) failures = polish + a11y
   - Layer 0, 8 failures = documentation debt; fix when handoff is near
4. **Re-audit after fixes**

## Output format

When reporting an audit, use this structure:

```markdown
# UI Audit — [project name] — [date]

## Summary
- Layers compliant: 3 / 8
- Layers partial: 4 / 8  
- Layers non-compliant: 1 / 8
- Ship blockers: [list of items]

## Per-layer findings
[For each layer, list checks failed with concrete examples and fix paths]

## Recommended next moves
[Ranked list, top 5]
```
