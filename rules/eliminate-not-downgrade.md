# eliminate-not-downgrade

When a framework, system, module, decision, or artifact is retired, **delete the source files and produce a single salvage document** capturing what transfers forward. Do not "downgrade" the eliminated content by leaving it marked as "historical evidence retained" with broken cross-references.

> 淘汰的东西就要清理, 不要降级。

## Rule

If something is decided to be eliminated:

1. **Extract the salvageable components** into one new salvage document. List each transferable component, why it survives, and how it adapts to the new framework.
2. **Delete the original source files.**
3. **Clean cross-references.** Any document linking to the eliminated files must be updated (link removed or redirected to the salvage document).
4. **Record the decision** in the project's decisions log with explicit "eliminated" status (not "superseded as future method", not "retained as historical evidence").
5. **Forbid re-introduction.** The salvage document explicitly lists what was NOT salvaged and why.

## What this rule rejects

The "降级" pattern looks like:

- `STATUS: COMPLETED AS HISTORICAL EVIDENCE / SUPERSEDED AS FUTURE METHOD`
- Roadmap row that keeps the eliminated item as an active step, just marked "historical"
- Decision record that records the supersession but doesn't delete the source files
- Cross-references kept as "for historical reference"
- README that still links to deleted file names

These leave the project in a confused state: the agent or reviewer cannot tell whether the eliminated item is operative, partially operative, or fully retired. Dead links accumulate. Future agents waste cycles re-evaluating the dead idea.

## Anti-example (do not do this)

```text
## P0 | OLD_FRAMEWORK_X experiment
Status: COMPLETED AS HISTORICAL EVIDENCE / SUPERSEDED AS FUTURE METHOD
Useful as runtime-pipeline baseline and output-diagnosis evidence,
but not the next methodology.

[link to docs/research/OLD_FRAMEWORK_X_plan.md]    ← link still active
[link to OLD_FRAMEWORK_X_aesthetic_manual.md]     ← link still active
```

After this rule, the entry becomes:

```text
## DEC-NNN: OLD_FRAMEWORK_X eliminated
6 transferable components captured in OLD_FRAMEWORK_X_salvage.md.
Source files removed. Re-introduction blocked.
```

And the original files are deleted.

## What "salvage" means

A salvage document:

- Lists why the original was eliminated (the errors / paradigm mismatches)
- Lists what was preserved and how it adapts to the current framework
- Lists what was NOT preserved and why (kill list)
- Lists all files removed in the cleanup
- Is the single source of truth — readers do not consult the deleted files

A salvage document is NOT:

- A copy of the original files with "historical" markers
- A summary of the original framework
- A bridge document allowing the original to still be referenced

## Why this rule exists

Half-retired frameworks pollute project momentum. Agents read the cross-references and re-evaluate whether the framework is operative. Decisions get re-litigated. New work accidentally builds on top of "historical" assumptions that nobody owns.

A clean elimination produces clarity: there is one current framework, one salvage document for what came before, and no dangling references. Agents and reviewers can trust the project state.

## How to install

- User-global: copy into `~/.claude/rules/eliminate-not-downgrade.md`
- Project-local: paste into project `CLAUDE.md` / `AGENTS.md` cleanup or refactor sections
