PHASE 0 — Agentic Framework: Master Orchestrator and Sub-Agents

Audience
- Experienced IT professional (15+ years), comfortable with architecture and operations, new to agentic multi-agent orchestration.

Goal
- Explain the agentic-framework used by this project: master orchestrator pattern, sub-agent roles, YAML frontmatter metadata, file layout, extension points, and maintenance best practices. Provide clear examples and a short runbook to onboard new contributors.

Why Phase 0 exists
- We treat the agentic-framework as the foundation: it defines how higher-level tasks are decomposed, how orchestration happens, and how specialized sub-agents contribute. Placing this as Phase 0 helps new contributors understand coordination and ownership before diving into code or models.

Core concepts

Master Orchestrator Pattern
- Single authoritative orchestrator coordinates work across multiple specialized sub-agents.
- Responsibilities:
  - Route tasks to appropriate sub-agents based on their specializations
  - Maintain task state, retries, and error handling policies
  - Aggregate sub-agent outputs and apply business rules or arbitration logic
- Canonical file: `.github/chatmodes/agent-orchestrator.md` (this repository uses that as the single source of truth for orchestration rules)

Sub-Agent Roles and Responsibilities
- Sub-agents are specialized roles that perform disciplined tasks. Common examples in this repo:
  - business-analyst-agent: requirements extraction, acceptance criteria
  - solutions-architect-agent: system and interface design
  - software-developer-agent: implementation guidance and code generation
  - QA-engineer-agent: test plans, QA strategy, test automation
  - security-expert-agent: threat models, secure coding checks
  - data-scientist-agent: model training, evaluation, explainability
  - cloud-engineer-agent: deployment patterns and IaC
- Each sub-agent focuses on a clear domain, producing outputs the master agent can validate and combine.

YAML Frontmatter Metadata
- Each agent file in `agentic-framework/sub-agents/` includes YAML frontmatter describing:
  - agent_type: e.g., `specialist`, `assistant`, `orchestrator`
  - specialization: short phrase (e.g., `data-engineer`)
  - tools_compatible: list of AI tools the agent should support (Tabnine, Copilot, Cursor, etc.)
  - context_scope: e.g., `file-level`, `session-level`, `project-level`
  - interaction_patterns: supported message patterns (e.g., `request-response`, `streaming`, `task-decomposition`)

File Layout and Conventions
- Key directories:
  - `agentic-framework/sub-agents/`: YAML-fronted markdown files for each agent persona
  - `agentic-framework/standards/`: coding, API, testing and security standards the agents reference
  - `.github/chatmodes/agent-orchestrator.md`: canonical orchestrator rules and coordination protocol
  - `telco-domain/`: domain-specific guidelines and business rules
- Naming and metadata conventions:
  - Filenames use `kebab-case` and end with `-agent.md` for persona files
  - Metadata keys are snake_case and consistently present in every agent file

Orchestration examples
- Simple orchestration flow (high level):
  1. Master receives a high-level task (e.g., "Add a new API to classify tickets by department").
  2. Master consults `agent-roster.json` and routes to `solutions-architect-agent` and `software-developer-agent`.
  3. Architect returns a design doc; developer produces a patch.
  4. QA-agent creates tests; security-agent performs a quick threat model.
  5. Master aggregates results and produces a final pull request and checklist.

Example YAML frontmatter (in `agentic-framework/sub-agents/software-developer-agent.md`)

```
---
agent_type: specialist
specialization: software-developer
tools_compatible:
  - tabnine
  - copilot
  - cursor
context_scope: project-level
interaction_patterns:
  - request-response
  - task-decomposition
---
```

Best practices
- Single Source of Truth: Keep orchestration rules in `.github/chatmodes/agent-orchestrator.md` to avoid drift.
- Keep agents narrow: Small, well-described responsibilities reduce ambiguity.
- Metadata-first: Always update YAML frontmatter when changing an agent's scope or capabilities.
- Use human-readable outputs: Agents should produce actionable artifacts (design notes, patch diffs, tests).
- Security: Always apply the `secure_coding_checklist.md` and sanitize outputs before merging.

Onboarding runbook (Quick Start)
1. Read `.github/chatmodes/agent-orchestrator.md` to understand orchestration conventions.
2. Open `agentic-framework/agent-roster.json` to map task types to agents.
3. Inspect `agentic-framework/sub-agents/<relevant-agent>.md` YAML frontmatter for capabilities.
4. If you change an agent's responsibilities, update the YAML frontmatter and add a short note in `agentic-framework/CHANGELOG.md`.
5. When proposing a change that spans agents, create a master-task issue and tag the relevant agent owners.

Extending the framework
- To add a new sub-agent:
  1. Create `agentic-framework/sub-agents/<name>-agent.md` with YAML frontmatter.
  2. Add the new agent to `agentic-framework/agent-roster.json` with routing rules.
  3. Update `agentic-framework/standards/` if the agent introduces new tooling or practices.
  4. Add a short test plan in `agentic-framework/templates/` describing the expected outputs.

Operational notes
- Logs and observability: Master should emit structured logs for task creation, routing, agent responses, and final decisions.
- Retry and backoff: Implement idempotent retries for transient failures, and circuit-breakers for repeated errors.
- Human-in-the-loop (HITL): For high-risk changes (security, infra), require explicit human approval before merging.
- Versioning: When agent behavior changes materially, bump the agent `version` key in YAML frontmatter and note the change in the CHANGELOG.

References
- `agentic-framework/standards/` — coding, security, and testing standards
- `.github/chatmodes/agent-orchestrator.md` — canonical orchestrator definition
- `telco-domain/` — domain-specific business rules used by the agents

Prompt examples and usage recipes
---------------------------------

This section provides actionable prompt templates and short recipes you can use with the master orchestrator and with sub-agents. They are written to be direct and unambiguous for a production environment.

1) Master Orchestrator — high-level task decomposition

Prompt (intent: decompose and route work):

```
Master: You are the Master Orchestrator. A new task was created: "Add a new API endpoint that classifies incoming support tickets into departments and returns routing metadata, confidence scores, and a short reasoning string."

1) Break this task into a minimal set of subtasks (design, implementation, tests, security review, deployment checklist).
2) For each subtask, choose the best sub-agent(s) from the roster and specify the expected artifact (e.g., design doc, patch diff, pytest suite, threat model).
3) Provide priorities, an estimated time-to-complete (hours) and a single checklist item that must be human-approved before merging.

Return a JSON object with keys: `subtasks` (array), `routing` (map agent->subtasks), `artifacts` (map subtask->expected artifact), `hito_required` (boolean), and `human_approval_prompt` (string).
```

Usage notes:
- Use this prompt when creating a cross-cutting change that involves multiple agents.
- The orchestrator should validate that chosen agents exist in `agent-roster.json` and that their `context_scope` permits the requested work.

2) Software Developer sub-agent — generate a patch and small tests

Prompt (intent: produce a focused patch):

```
Agent: You are the `software-developer-agent`. Produce a minimal git patch (unified diff) that implements a new Flask/Starlette/FastAPI endpoint `/classify-ticket` that accepts JSON `{ticket_text: str}` and returns `{department, confidence, reasoning}`. Include a single unit test (pytest) that asserts the response shape for a sample ticket.

Constraints:
- Keep changes limited to `src/api/` and `tests/`.
- Follow the project's coding standards in `agentic-framework/standards/coding_styleguide.md`.
- Do NOT include secrets or real API keys.

Return: `patch` (string), `test` (string), and a short `explanation` (string).
```

3) Data Scientist sub-agent — model tuning suggestion

Prompt (intent: propose model improvements and evaluation plan):

```
Agent: You are the `data-scientist-agent`. Given the current model pipeline (TF-IDF + LogisticRegression ensemble with Gemini fusion), suggest three targeted experiments that could improve departmental routing accuracy by at least 2% on a holdout set. For each experiment provide: reason, metric to track, required data, estimated compute (GPU hours or CPU-hours), and a failing condition that should stop the experiment.

Return a Markdown table with columns: `experiment`, `reason`, `metric`, `data_required`, `compute_estimate`, `failing_condition`.
```

4) Human-in-the-loop (HITL) approval prompt

Prompt (intent: ask for final human approval before merging high-risk changes):

```
Master -> Human: A proposed change touches security-sensitive modules and automated tests have passed. Summary:
- PR title: {title}
- Affected modules: {list}
- Risk summary: {short}
- Required manual checks: {checklist}

Please review the above and explicitly approve or request changes. If approving, reply with `APPROVE: <your name>` and a short rationale.
```

5) Sanitization and safe-output recipe (for any agent that emits HTML or user-visible text)

Prompt (intent: normalize and sanitize text outputs):

```
Agent: Before returning any `reasoning` or `explanation` text that may include user input or free-form model content, perform these steps and return the cleaned text:
1) Strip all HTML tags using a robust parser (e.g., BeautifulSoup `.get_text()`),
2) Remove or normalize any prefix/suffix tokens like `Reasoning:` or `Explanation:` using a case-insensitive regex,
3) Escape remaining special characters for HTML using `html.escape()` before embedding in HTML contexts,
4) Limit output length to 1000 characters and add `...` if truncated.

Return a small JSON: `{clean_text: str, steps_applied: [str]}`.
```

Quick recipe: include this sanitization prompt as a post-processing step in all agents that return human-visible strings.

6) Agent onboarding prompt (create a new sub-agent file)

Prompt (intent: create starter YAML-fronted agent file):

```
Agent: Create a new sub-agent file `agentic-framework/sub-agents/<name>-agent.md` for a `data-privacy-agent`. The YAML frontmatter should include `agent_type`, `specialization`, `tools_compatible` (Tabnine, Copilot), `context_scope`, and `interaction_patterns`. Provide a 3-5 sentence description and a short checklist of responsibilities.

Return the complete markdown file content with YAML frontmatter.
```

Notes and safety
- Keep prompts deterministic when possible: ask for machine-parseable output (JSON, diff, or tables).
- Validate agent outputs against expected schema before taking automated actions.
- Never allow agents to auto-merge high-risk PRs without HITL approval.

End of prompt examples

Quick copy-ready snippets
------------------------

Use these compact prompts and templates when you need a fast, copy-paste starting point.

Master Orchestrator (compact):

```
Master: Decompose task: "Add /classify-ticket API returning {department, confidence, reasoning}". Return JSON: {subtasks, routing, artifacts, hito_required, human_approval_prompt}.
```

Software Developer (compact):

```
Agent (software-developer): Produce a git unified diff implementing `/classify-ticket` and a pytest that verifies response shape. Limit changes to `src/api/` and `tests/`.
```

Data Scientist (compact):

```
Agent (data-scientist): Propose 3 experiments to improve routing accuracy; return a Markdown table: experiment/reason/metric/data_needed/compute/failing_condition.
```

Sanitization/Post-process (compact):

```
Agent: Clean `reasoning` text: 1) strip HTML tags; 2) remove `Reasoning:` prefixes; 3) html.escape(); 4) truncate to 1000 chars. Return JSON {clean_text, steps_applied}.
```

Agent onboarding — YAML template (copy into `agentic-framework/sub-agents/<name>-agent.md`):

```
---
agent_type: specialist
specialization: data-privacy
tools_compatible:
  - tabnine
  - copilot
context_scope: project-level
interaction_patterns:
  - request-response
  - task-decomposition
version: 0.1.0
---

Short description: The data-privacy-agent reviews changes for privacy impact, maintains PII handling patterns, and provides remediation steps.

Responsibilities checklist:
- Review PRs touching data pipelines for PII exposure
- Suggest anonymization or minimization steps
- Provide short remediation steps and test cases
```

Paste these into issues, PR templates, or a developer's scratchpad to speed up routine orchestration tasks.


