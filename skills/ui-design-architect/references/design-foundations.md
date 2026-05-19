# Design Foundations · Reference

> Detailed reference for Phase 3 (Execution Standards). Read when producing hi-fi mockups, design tokens, component libraries, or production design specs.
>
> **Contents**: token architecture, type scales, spacing grids, color systems, component anatomy + state matrices, motion tokens, WCAG 2.2 specifics, design QA checklist.

---

## 1. The three-layer token architecture

W3C Design Tokens Community Group (DTCG) format is production-ready. Format: JSON, file extension `.tokens.json`, references via `{token.path}` syntax.

### Layer 1 — Primitive (reference) tokens

Raw values. Don't change with context.

Material naming: `md.ref.palette.secondary90 = #E8DEF8`  
Tailwind-style: `gray-500`, `blue-600`

### Layer 2 — Semantic (system) tokens

Role-based. These are what components reference.

Material naming: `--md-sys-color-primary`, `--md-sys-color-on-primary`  
Carbon naming: `$interactive-01`, `$text-04`, `$hover-primary`, `$active-primary`, `$focus`, `$disabled-02`, `$danger-01`

**Critical pattern — on-color pairing:** every surface color has a paired text color guaranteed to meet contrast.
- `surface` ↔ `on-surface`
- `primary` ↔ `on-primary`
- `accent` ↔ `on-accent`

### Layer 3 — Component tokens

Per-component overrides. Default to semantic tokens.

Material: `--md-filled-button-container-color` (defaults to `--md-sys-color-primary`)

### Real token tree fragment

```json
{
  "color": {
    "ref": { "palette": { "purple90": { "value": "#E8DEF8" } } },
    "sys": {
      "primary":    { "value": "{color.ref.palette.purple40}" },
      "on-primary": { "value": "{color.ref.palette.white}" }
    },
    "comp": {
      "btn-primary": {
        "bg":   { "value": "{color.sys.primary}" },
        "text": { "value": "{color.sys.on-primary}" }
      }
    }
  }
}
```

### Two strategies for state derivation

| Strategy | Used by | Pros | Cons |
|---|---|---|---|
| Overlay-based | Material | Few tokens, less maintenance | Less precise control |
| Explicit state tokens | Carbon | Precise per-state control | More tokens to maintain |

---

## 2. Type scales (numeric, verbatim from primary sources)

### Material 3 (15 tokens, full table)

Sources: m3.material.io typography, developer.android.com Compose docs

| Token | Size (sp/px) | Line height | Weight |
|---|---|---|---|
| Display Large | 57 | 64 | Regular |
| Display Medium | 45 | 52 | Regular |
| Display Small | 36 | 44 | Regular |
| Headline Large | 32 | 40 | Regular |
| Headline Medium | 28 | 36 | Regular |
| Headline Small | 24 | 32 | Regular |
| Title Large | 22 | 28 | Regular |
| Title Medium | 16 | 24 | Medium |
| Title Small | 14 | 20 | Medium |
| Body Large | 16 | 24 | Regular |
| Body Medium | 14 | 20 | Regular |
| Body Small | 12 | 16 | Regular |
| Label Large | 14 | 20 | Medium |
| Label Medium | 12 | 16 | Medium |
| Label Small | 11 | 16 | Medium |

Note: Material distinguishes 5 categories (display / headline / title / body / label), each with 3 sizes (large / medium / small). The naming is semantic, not just size-based.

### Tailwind defaults (12 utilities)

Source: tailwindcss.com font-size docs

| Utility | Size (rem / px) | Line height |
|---|---|---|
| text-xs | 0.75 / 12 | 16 |
| text-sm | 0.875 / 14 | 20 |
| text-base | 1.0 / 16 | 24 |
| text-lg | 1.125 / 18 | 28 |
| text-xl | 1.25 / 20 | 28 |
| text-2xl | 1.5 / 24 | 32 |
| text-3xl | 1.875 / 30 | 36 |
| text-4xl | 2.25 / 36 | 40 |
| text-5xl | 3.0 / 48 | (unitless 1.0) |

### Carbon (selected, "short" vs "long" distinction)

Source: carbondesignsystem.com type-sets

| Token | Size (px / rem) | Line height | Letter spacing |
|---|---|---|---|
| code-01 | 12 / 0.75 | 16 | 0.32 |
| caption-01 | 12 / 0.75 | 16 | 0.32 |
| label-02 | 14 / 0.875 | 18 | 0.16 |
| body-short-01 | 14 / 0.875 | 18 | 0.16 |
| body-long-01 | 14 / 0.875 | 20 | 0.16 |
| body-short-02 | 16 / 1.0 | 22 | 0 |
| body-long-02 | 16 / 1.0 | 24 | 0 |

**Carbon's insight:** distinguish short (UI labels) from long (body paragraphs) at same font size, with different line heights. Most teams miss this.

### Refactoring UI minimal set (7 sizes, UI-focused)

Source: refactoringui.com guidance (via summaries)

Recommended UI scale (base 16px, ratio 1.25): `12, 14, 16, 20, 24, 30, 36`

Additional principles from Refactoring UI:
- Line height: 1.0-1.25 headings, 1.5-1.75 body
- Weight: 400-500 body, 600-700 emphasis (don't rely solely on size for hierarchy)
- Limit to 2-3 font families
- Use px or rem, NOT em (em compounds and creates surprise)

### Modular scale ratios

Common ratios: 1.125, 1.2, **1.25** (most common for UI), 1.333, 1.414, 1.5, 1.618 (golden)

UI tends toward tighter ratios (1.2-1.333) so adjacent sizes are distinguishable but not jarring. Editorial uses wider ratios (1.414-1.618) for dramatic display.

---

## 3. Spacing grids (numeric)

### Material 3 (4dp grid, 16 tokens)

`0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 80` (all dp, multiples of 4)

### Carbon (10 tokens, rem-based)

| Token | rem | px |
|---|---|---|
| spacing-01 | 0.125 | 2 |
| spacing-02 | 0.25 | 4 |
| spacing-03 | 0.5 | 8 |
| spacing-04 | 0.75 | 12 |
| spacing-05 | 1.0 | 16 |
| spacing-06 | 1.5 | 24 |
| spacing-07 | 2.0 | 32 |
| spacing-08 | 2.5 | 40 |
| spacing-09 | 3.0 | 48 |
| spacing-10 | 4.0 | 64 |

### Refactoring UI minimal

`4, 8, 16, 24, 32, 48, 64` (7 tokens, geometric-ish growth)

### 4pt vs 8pt grid — when to use what

| System | Choice | Why |
|---|---|---|
| Google / Material | 4dp primary, 8dp secondary | Precise; aligns with baselines |
| Old 8pt schools | 8pt primary | Historical; visual differences clearer; fewer tokens to manage |
| UCLA hybrid | 8pt soft grid + 4pt for small components | Balanced |

**Pragmatic recommendation:** base on 4, but **converge common values to multiples of 8** (4, 8, 12, 16, 24, 32, 48, 64). Use 4 or 12 only when necessary.

### Breakpoints

**Material 3 (dp):**  
- `< 600` Compact (mobile)
- `600-839` Medium (small tablet)  
- `840-1199` Expanded (tablet / small desktop)
- `1200-1599` Large (desktop)
- `≥ 1600` Extra-large (wide desktop)

**Tailwind (px, min-width):** sm 640, md 768, lg 1024, xl 1280, 2xl 1536

**Bootstrap 5 (px, min-width):** sm 576, md 768, lg 992, xl 1200, xxl 1400

---

## 4. Color systems

### Semantic naming pattern (consolidated best practice)

```
--color-surface              (page background)
--color-surface-raised       (cards above page)
--color-surface-overlay      (modals, popups)
--color-on-surface           (text on surface)
--color-on-surface-muted     (secondary text)
--color-border               (subtle dividers)
--color-border-strong        (emphasized dividers)
--color-accent               (primary action)
--color-on-accent            (text on accent)
--color-accent-hover
--color-accent-active
--color-state-success
--color-state-warning
--color-state-danger
--color-state-info
```

### Dark / light mode structure

Two strategies:

1. **Toggle root variables** (Material approach): same component CSS, swap `--md-sys-color-*` values at `:root` for `[data-theme="dark"]`
2. **Theme files** (Carbon approach): role tokens stay constant, multiple theme files map roles to different hex values

### Carbon's role + theme separation

Carbon defines 4 default themes:
- White (light)
- Gray 10 (light)
- Gray 90 (dark)
- Gray 100 (dark)

Each maps the same role tokens (`$interactive-01`, etc.) to theme-appropriate hex.

---

## 5. Component architecture

### Anatomy (button as example)

```
┌──────────────────────────────────┐
│  ◉  Label text             ─→    │  ← container (bg + shape + border)
│  │                               │
│  └ icon (optional)               │
└──────────────────────────────────┘
  ↑                                ↑
  named parts                      focus ring (separate part)
```

Named parts (token-able):
- container — bg, shape, border
- label — text style + color
- icon — color
- outline — for outlined variants
- focus ring — separate token

### Full state matrix (interactive component)

| State | Trigger | Visual change |
|---|---|---|
| **Default** | Idle | Base appearance |
| **Hover** | Mouse over | Background lift, slight color shift |
| **Focused** | Keyboard focus | Visible focus ring (WCAG required) |
| **Active** | Pressed | Background darken / scale 0.98 |
| **Disabled** | `disabled` attr | Reduced opacity / muted colors, no pointer events |
| **Loading** | Async in progress | Spinner / progress, pointer-events off |
| **Error** | Validation failure | Danger color + error icon |
| **Selected** | In multi-select / toggle | aria-pressed + visual distinction |

**Minimum for shipping:** default, hover, focused, active, disabled.  
Loading and error are mandatory for forms.

### Variant axis × state axis

- **Variant axis**: filled / outlined / elevated / tonal / text — different "look", same component
- **State axis**: as above, applies within each variant
- **Product**: 5 variants × 8 states = 40 visual specs. **Only manageable with tokens.**

### Atomic Design (Brad Frost) — when it works, when it doesn't

```
Atoms      → buttons, inputs, labels (smallest, no children)
Molecules  → search bar (label + input + button)
Organisms  → header (logo + nav + search + user menu)
Templates  → page-level skeleton
Pages      → templates with real content
```

**Modern critique** (Sparkbox 2020+): flat hierarchy "may not be practical for modern applications, can cause pain points." Boundary between molecule and organism is fuzzy in practice. Modern teams often use feature-driven / vertical-slice organization instead.

**Pragmatic stance:** use Atomic Design as a thinking aid (helpful for spotting "this primitive should be reusable"), don't enforce it as a strict folder structure.

---

## 6. Motion

### Material 3 duration + easing tokens

Source: m3.material.io/styles/motion/easing-and-duration

| Easing | Duration | Use |
|---|---|---|
| Emphasized | 500ms | Screen-level start/end transitions (recommended default) |
| Emphasized decelerate | 400ms | Element entering screen |
| Emphasized accelerate | 200ms | Element exiting screen |
| Standard | 300ms | Fallback for Web/iOS |
| Standard decelerate | 250ms | Entering (Web/iOS) |
| Standard accelerate | 200ms | Exiting (Web/iOS) |

**Core rules:**
- Entering animations are longer than exiting (e.g., 400ms in / 200ms out) — gives weight on arrival
- On Web, use Standard set (Emphasized requires native platforms)
- Web cubic-bezier control points are not in primary M3 sources; common Web defaults: `cubic-bezier(.4, 0, .2, 1)` (standard), `cubic-bezier(0, 0, .2, 1)` (decelerate), `cubic-bezier(.4, 0, 1, 1)` (accelerate)

### Recommended motion token set

```css
:root {
  --motion-fast: 150ms;        /* hover, micro */
  --motion-normal: 250ms;      /* state change */
  --motion-medium: 400ms;      /* element enter */
  --motion-slow: 700ms;        /* screen transition / camera moves */

  --ease-standard:   cubic-bezier(.4, 0, .2, 1);
  --ease-decelerate: cubic-bezier(0, 0, .2, 1);
  --ease-accelerate: cubic-bezier(.4, 0, 1, 1);
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --motion-fast: 0ms;
    --motion-normal: 0ms;
    --motion-medium: 0ms;
    --motion-slow: 0ms;
  }
}
```

### prefers-reduced-motion (REQUIRED for a11y)

WCAG 2.3.3 (AAA): motion triggered by interaction must be disable-able. The standard pattern:

```css
@media screen and (prefers-reduced-motion: no-preference) {
  /* default animations */
  .card { transition: transform 400ms cubic-bezier(.4, 0, .2, 1); }
}

@media screen and (prefers-reduced-motion: reduce) {
  .card { transition: none; }
}
```

Or use the token approach above (motion tokens zero out at reduce).

### When NOT to animate

- Pure decoration on every interaction (animation fatigue)
- High-frequency events (scroll, mouse-move)
- Critical-path interactions where speed matters more than feedback
- Anything during user reading flow

---

## 7. Accessibility · WCAG 2.2 numeric checklist

| SC | Name | Threshold | Source |
|---|---|---|---|
| 1.4.3 | Contrast Minimum (AA) | 4.5:1 text, 3:1 large text (≥18pt or 14pt bold) | [W3C](https://w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) |
| 1.4.11 | Non-text Contrast (AA) | ≥3:1 for UI components, graphical objects | [W3C](https://w3c.github.io/wcag21/understanding/non-text-contrast.html) |
| 2.5.8 | Target Size Min (AA, new in 2.2) | ≥24×24 CSS px (5 exceptions: spacing/equivalent/essential/user-agent/inline) | [W3C](https://w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) |
| 2.4.11 | Focus Not Obscured (AA, new in 2.2) | Focus indicator not fully hidden by author content | [W3C](https://w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) |
| 2.4.11 | Focus Appearance | ≥1 CSS px perimeter or 4 CSS px shortest side + 3:1 contrast | (third-party summary) |
| 2.1.1 | Keyboard (A) | All functionality keyboard-operable, no time-dependent input | [W3C](https://w3.org/WAI/WCAG21/Understanding/keyboard.html) |
| 2.3.3 | Animation from Interactions (AAA) | Motion disable-able via system setting or site option | (plain-English summary) |

### Practical a11y audit (run before shipping hi-fi)

1. **Contrast check** every text/background pair using a tool (axe DevTools, WebAIM contrast checker, Stark)
2. **Keyboard nav** the entire flow (Tab, Shift+Tab, Enter, Esc) — every action reachable?
3. **Focus indicator** visible on every interactive element?
4. **Screen reader** smoke test (VoiceOver / NVDA) — does the structure make sense?
5. **Touch targets** measured — anything < 24×24?
6. **Reduced motion** — does the UI degrade gracefully when motion is reduced?
7. **Zoom** to 200% — does layout hold?

---

## 8. Design QA / handoff checklist

Run before declaring a hi-fi or production design "done":

| # | Check | Artifact |
|---|---|---|
| 1 | All colors come from tokens (no hex in component CSS) | grep for `#` in CSS |
| 2 | Every interactive component has min 5 states (default/hover/focused/active/disabled) | Storybook stories per state |
| 3 | a11y automated check (axe / Pa11y) clean or known-issue annotated | CI report JSON |
| 4 | Responsive: validated at min 3 breakpoints (mobile / tablet / desktop) | Screenshots per breakpoint |
| 5 | Copy review (typos, voice, length) | PR description note |
| 6 | Motion has `prefers-reduced-motion` override | grep for `prefers-reduced-motion` |
| 7 | Release phase tagged (Early Access / Beta / GA / Production) | Issue label |
| 8 | Tokens documented (which semantic tokens does this component consume?) | Component MDX or spec doc |

---

## References (further reading)

- [Material Design 3 — Design tokens](https://m3.material.io/foundations/design-tokens)
- [Material Design 3 — Motion](https://m3.material.io/styles/motion/easing-and-duration)
- [Carbon Design System](https://carbondesignsystem.com/elements/spacing/overview/)
- [W3C Design Tokens Format](https://designtokens.org/tr/drafts/format/)
- [WCAG 2.2 Overview](https://w3.org/WAI/WCAG22/quickref/)
- [Refactoring UI by Adam Wathan & Steve Schoger](https://refactoringui.com)
- [Atomic Design by Brad Frost](https://atomicdesign.bradfrost.com/)
- [Sparkbox critique of Atomic Design](https://sparkbox.com/foundry/iterating_on_atomic_design)
