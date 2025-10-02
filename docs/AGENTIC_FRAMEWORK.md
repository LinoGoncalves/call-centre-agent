# Agentic Framework Guide

**Purpose**: Explain the master orchestrator pattern, sub-agent roles, YAML metadata conventions, and how to extend the `agentic-framework/` for new workflows.

---

## Overview

The `agentic-framework/` contains the orchestrator and a roster of specialized agents designed to collaborate on complex tasks. It is intentionally vendor-neutral and optimized for multi-agent coordination in engineering workflows.

Key components:
- `master-agent.md`: Orchestration patterns and coordination strategies
- `sub-agents/`: 32+ specialized agents (software-dev, data-science, QA, DevOps, etc.)
- `templates/`: Reusable YAML and documentation templates

---

## Agent Types and Responsibilities

Each agent file in `agentic-framework/sub-agents/` contains YAML frontmatter specifying:
- `agent_type` (master|specialist)
- `specialization` (e.g., 'data-engineer')
- `tools_compatible` (which AI tools or libraries it supports)
- `interaction_patterns` (how it expects to be invoked)

Example YAML frontmatter:
```yaml
---
agent_type: specialist
specialization: data-engineer
tools_compatible:
  - pandas
  - scikit-learn
context_scope: dataset preparation, ETL
interaction_patterns: |
  - Provide schema validation
  - Offer data-sampling strategies
---
```

---

## Master Agent Orchestration (Canonical Reference)

This repository centralizes orchestration guidance in a single canonical document: the agent orchestrator specification located at `.github/chatmodes/agent-orchestrator.md`.

Rather than duplicating orchestration rules in multiple places, refer to that canonical file for decision patterns, coordination flows, and invocation examples. In short:

- The master agent produces a scoped plan with explicit todos and acceptance criteria.
- Exactly one todo is marked in-progress at a time to avoid conflicting state changes.
- Human-in-the-loop (HITL) tasks are flagged and routed to reviewers.
- The master composes sub-agent outputs into final artifacts (docs, code, tests).

For full orchestration rules and example workflows, read: `.github/chatmodes/agent-orchestrator.md` (Master Orchestrator Chat Mode).
---

## How to Add a New Sub-Agent

1. Create a new markdown file in `agentic-framework/sub-agents/` with YAML frontmatter
2. Include `agent_type`, `specialization`, `tools_compatible`, `context_scope`, and `interaction_patterns`
3. Add example invocation snippets and expected outputs
4. Register agent in `agentic-framework/agent-roster.json` with metadata

---

## Example Workflow: Create New Feature

1. Master agent defines feature scope and break into tasks
2. Master assigns tasks to specialized sub-agents (solutions-architect, data-engineer, developer)
3. Sub-agents return artifacts (design doc, code snippets, tests)
4. Master composes final PR and creates validation checklist

---

## Best Practices


--3. **HITL (Human-in-the-loop)**: For full guidance on HITL workflows (modes, checkpoints, and examples), see `docs/AGENTIC_FRAMEWORK_GUIDE.md` -> "Human-in-the-Loop (HITL) Workflows".

## Security and Governance
- Sub-agents that access external APIs must document required environment variables and permissions

---

## Extending the Framework

- Add tooling metadata to `agent-roster.json`
- Provide CI checks for new agents (linting YAML, validating frontmatter)
- Integrate with documentation generators to produce an agent catalog

---

This guide makes it straightforward for engineers to understand, use, and extend the agentic orchestration in this repository.