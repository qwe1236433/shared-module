# project-quality-framework

Portable governance framework for AI-assisted software projects. A seed document for any new repository (or any existing repository that needs stronger agent discipline).

The framework defines: quality system, file responsibility boundaries, agent workflow, review gates, report format, synchronization protocol, and adoption checklist. It is project-agnostic — every project-specific value (name, path, command, schema, provider, runtime artifact) is supplied via the **Project Profile Variables** in §0 of the framework.

## What's in this folder

- `PROJECT_QUALITY_FRAMEWORK.md` — the framework itself (676 lines, 19 sections)

## When to use

Adopt this framework when starting a new repo, or when an existing repo needs:

- File responsibility boundaries between design, audit, handoff, and agent execution
- A Requirement Clarification Gate so agents don't silently guess in ambiguous tasks
- A Blueprint Impact Check that routes design-touching changes to the right file
- A Boundary Re-Entry Check that prevents silent cross-boundary edits
- A standard Final Report Format
- A Checkpoint Protocol for cross-agent handoff
- Starter `00_BLUEPRINT.md` and primary agent file skeletons

## How to use

1. Read §0 (Project Profile Variables) and fill in your project's values: `{{PROJECT_NAME}}`, `{{REPO_ROOT}}`, `{{PRIMARY_AGENT_FILE}}`, etc.
2. Choose an adoption profile from §2: Minimal / Expanded / No-Manifest.
3. Copy the relevant section skeletons (§15 starter `00_BLUEPRINT.md` and §16 starter `{{PRIMARY_AGENT_FILE}}`) into your repo, substituting variables.
4. Follow §17 Adoption Checklist to confirm coverage.
5. Use §18 Migration Workflow if applying to an existing repo with prior structure.

## Portability rule

Per the framework's own statement (header):

> Portability rule: every project-specific name, path, command, schema, system, provider, runtime artifact, and workflow state must be supplied by the target repository. Do not copy values from the source project into a new project.

Do not edit this template to bind it to one project. Instead, fill the variables at adoption time in your target repo.

## Version

v1.0.0 (extracted 2026-05-18, source: dome-TV project root)
