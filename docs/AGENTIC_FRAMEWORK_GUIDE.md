# Agentic Framework Guide

**Purpose**: Complete guide to the universal AI agent orchestration framework  
**Audience**: Developers, AI tool users, project managers  
**Compatibility**: GitHub Copilot, Tabnine, Cursor, Codeium, JetBrains AI, and all major AI coding assistants

---

## Overview

The **Agentic Framework** is a universal, tool-agnostic system for orchestrating specialized AI agents to handle complex, multi-disciplinary software projects. Instead of asking a single AI to be an expert in everything, the framework coordinates 32+ specialized agents, each with deep expertise in specific domains.

###What Makes This Framework Universal?

**Tool-Agnostic Design:**
- Works with **any** AI coding assistant (not locked to GitHub Copilot)
- YAML metadata in agent files provides context for all tools
- Markdown-based personas are human-readable and AI-parseable
- No vendor-specific APIs or extensions required

**Key Innovation**: Master-Agent Orchestration Pattern
- **Master Agent** coordinates complex tasks
- **Sub-Agents** provide specialized expertise
- **Human-in-the-Loop (HITL)** at critical decision points

---

## Framework Architecture

### Directory Structure

```
agentic-framework/
├── master-agent.md                   # Orchestration controller (315 lines)
├── agent-roster.json                 # Complete agent mapping
├── sub-agents/                       # 32+ specialized agents
│   ├── __init__.py
│   ├── business-analyst-agent.md
│   ├── solutions-architect-agent.md
│   ├── software-developer-agent.md
│   ├── data-scientist-agent.md
│   ├── devops-engineer-agent.md
│   ├── security-expert-agent.md
│   ├── QA-engineer-agent.md
│   └── ... (25 more agents)
├── standards/                        # Universal development standards
│   ├── coding_styleguide.md
│   ├── api_design_patterns.md
│   ├── testing_strategy.md
│   ├── secure_coding_checklist.md
│   └── ... (15 standards documents)
└── templates/                        # Reusable project templates
    ├── project-brief-template.md
    ├── quality-gates.md
    └── workflow-state-management.md
```

---

## Master Agent: The Orchestrator

**File**: `agentic-framework/master-agent.md` (315 lines)

### Core Responsibilities

1. **Understand complex, multi-faceted goals**
2. **Identify required specialized agents**
3. **Coordinate agent workflows**
4. **Maintain project context across interactions**
5. **Manage human approval gates (HITL)**
6. **Track project state and continuity**

### YAML Metadata (Universal AI Tool Context)

**Lines 2-10**:
```yaml
---
agent_type: "master_orchestrator"
specialization: ["project_management", "team_coordination", "workflow_orchestration"]
tools_compatible: ["tabnine", "github_copilot", "cursor", "codeium", "jetbrains_ai"]
context_scope: "project_wide"
interaction_patterns: ["planning", "delegation", "coordination", "review"]
model_suggestions: ["claude_sonnet", "gpt4", "gemini_pro"]
updated: "2025-09-29"
---
```

**Why YAML Metadata?**

Different AI tools have different context mechanisms:
- **Tabnine**: Uses metadata for project-wide understanding
- **GitHub Copilot**: Recognizes `tools_compatible` for persona loading
- **Cursor**: Parses `context_scope` for relevance scoring
- **Universal**: All tools can parse YAML frontmatter

**Key Fields:**
- `agent_type`: Role classification (orchestrator, specialist, reviewer)
- `specialization`: Domain expertise areas
- `tools_compatible`: Which AI assistants support this agent
- `context_scope`: How much project context needed (file, module, project_wide)
- `interaction_patterns`: Expected usage patterns
- `model_suggestions`: Recommended LLM models for best results

### Usage Pattern

**Basic Invocation:**
```
@workspace Using #file:agentic-framework/master-agent.md, create a comprehensive tutorial for this project
```

**Multi-Agent Coordination:**
```
@workspace Acting as the master orchestrator from agentic-framework/master-agent.md, 
coordinate these agents for the task:
- business-analyst-agent for requirements analysis
- solutions-architect-agent for system design
- software-developer-agent for implementation
- QA-engineer-agent for validation checkpoints
```

**Why This Works:**
- `@workspace`: Provides full project context to AI tool
- `#file:` reference: Loads agent persona explicitly
- Clear delegation: Specifies which agents to engage
- HITL checkpoints: Human review between agent hand-offs

---

## Specialized Sub-Agents

### Agent Categories

**Core Team** (6 agents):
- Product Owner, Business Analyst, Solutions Architect
- Software Developer, UI Designer, QA Engineer

**Infrastructure Team** (4 agents):
- Cloud Engineer, Networks Engineer, Database Engineer, DevOps Engineer

**Data Science & ML Team** (3 agents):
- Data Engineer, Data Scientist, ML Engineer

**Governance & Management** (5 agents):
- Security Expert, Project Manager, Test Manager, Test Automation Expert, Scrum Master

**Additional Specialists** (6 agents):
- Technical Writer, SRE, UX Researcher, Principal Engineer, Blueprint Executor, Critical Analyst

**Total**: 32+ specialized agents (extensible)

---

### Agent Persona Structure

**Example**: `agentic-framework/sub-agents/solutions-architect-agent.md`

```markdown
---
agent_type: "specialist"
specialization: ["system_architecture", "design_patterns", "scalability"]
tools_compatible: ["tabnine", "github_copilot", "cursor", "codeium", "jetbrains_ai"]
context_scope: "project_wide"
interaction_patterns: ["design", "review", "documentation"]
model_suggestions: ["claude_sonnet", "gpt4"]
updated: "2025-09-29"
---

# Persona: Solutions Architect Agent 🏛️

You are a **Senior Solutions Architect** with 15+ years of experience...

## Core Responsibilities
- Design scalable system architectures
- Make technology stack decisions
- Create technical design documents
- Review and approve architectural changes
- Ensure alignment with industry best practices

## Standards Reference
Always follow:
- `agentic-framework/standards/architectural-principles.md`
- `agentic-framework/standards/api_design_patterns.md`
- `agentic-framework/standards/security_policies.md`

## Output Format
- Architecture Decision Records (ADRs)
- System diagrams (C4 model)
- Technology evaluation matrices
- Capacity planning documents

## Interaction Pattern
1. Understand requirements from Business Analyst
2. Design system architecture
3. Document architectural decisions
4. Present to stakeholders for approval
5. Hand off to Software Developer for implementation
```

**Key Sections:**
1. **YAML Metadata**: Tool compatibility and context
2. **Persona Definition**: Role and expertise level
3. **Core Responsibilities**: What this agent does
4. **Standards Reference**: Which guidelines to follow
5. **Output Format**: Expected deliverables
6. **Interaction Pattern**: Workflow integration

---

## Human-in-the-Loop (HITL) Workflows

### Oversight Modes

The framework supports **4 oversight levels**:

#### 1. **Full Automation** (No HITL)
- AI handles entire workflow without pauses
- **Use Case**: Repetitive, low-risk tasks (code formatting, documentation)
- **Example**: "Format all Python files per style guide"

#### 2. **Checkpoint Mode** (Phase-Level HITL)
- AI completes each phase, waits for human approval
- **Use Case**: Standard feature development
- **Example**: 
  1. BA Agent creates requirements → **Human Review**
  2. Architect Agent designs system → **Human Review**
  3. Developer Agent implements → **Human Review**
  4. QA Agent validates → **Human Review**

#### 3. **Interactive Mode** (Sub-Task HITL)
- AI pauses for approval at every sub-task
- **Use Case**: High-risk changes, complex features
- **Example**: Database schema migration (review each table change)

#### 4. **Advisory Mode** (Human Leads, AI Assists)
- AI provides suggestions, human makes all decisions
- **Use Case**: Learning mode, critical system changes
- **Example**: Production deployment (AI suggests steps, human executes)

### Checkpoint Configuration

**In Master Agent Invocation:**
```
@workspace Using #file:agentic-framework/master-agent.md with CHECKPOINT mode,
create authentication system:
- Business Analyst: requirements → WAIT FOR APPROVAL
- Solutions Architect: design → WAIT FOR APPROVAL
- Software Developer: implement → WAIT FOR APPROVAL
- QA Engineer: test plan → WAIT FOR APPROVAL
```

---

## Standards Integration

### Universal Development Standards

**Purpose**: Consistent quality across all agents

**Available Standards** (`agentic-framework/standards/`):

**Code Quality:**
- `coding_styleguide.md`: Python, JavaScript, TypeScript conventions
- `api_design_patterns.md`: RESTful API best practices
- `secure_coding_checklist.md`: Security patterns (OWASP)

**Architecture:**
- `architectural-principles.md`: SOLID, Clean Architecture, Domain-Driven Design
- `iac_standards.md`: Infrastructure as Code (Terraform, Kubernetes)

**Testing:**
- `testing_strategy.md`: Unit, integration, E2E testing patterns
- `test_automation_expert-agent.md`: CI/CD integration

**Data & ML:**
- `data_pipeline_patterns.md`: ETL/ELT best practices
- `mlops_pipeline_standards.md`: ML lifecycle management

**Operations:**
- `sre_handbook.md`: Site Reliability Engineering practices
- `network_security_policy.md`: Network segmentation, firewalls

**Documentation:**
- `documentation_styleguide.md`: Technical writing standards
- `api_reference_template.md`: API documentation format

### Standards Enforcement

**Every agent references standards:**
```markdown
## Standards Reference
Always follow:
- `agentic-framework/standards/coding_styleguide.md`
- `agentic-framework/standards/testing_strategy.md`
```

**In prompts:**
```
@workspace Using #file:agentic-framework/sub-agents/software-developer-agent.md,
implement authentication following:
- agentic-framework/standards/coding_styleguide.md
- agentic-framework/standards/secure_coding_checklist.md
```

---

## Real-World Usage Examples

### Example 1: Feature Development

**Goal**: Add user authentication to web application

**Workflow:**

**Step 1: Master Agent Planning**
```
@workspace Using #file:agentic-framework/master-agent.md, plan implementation of 
OAuth2 authentication with the following agents:
- business-analyst-agent: user stories and acceptance criteria
- solutions-architect-agent: authentication architecture design
- security-expert-agent: security review and threat modeling
- software-developer-agent: implementation
- QA-engineer-agent: test cases and validation
```

**Step 2: Requirements (Business Analyst)**
```
@workspace Using #file:agentic-framework/sub-agents/business-analyst-agent.md,
create user stories for OAuth2 authentication:
- Login with Google/GitHub/Microsoft
- Token refresh mechanism
- Logout and session management
- Authorization scopes
```

**Step 3: Architecture (Solutions Architect)**
```
@workspace Using #file:agentic-framework/sub-agents/solutions-architect-agent.md,
design OAuth2 authentication system following:
- agentic-framework/standards/api_design_patterns.md
- agentic-framework/standards/security_policies.md
Include: architecture diagram, API endpoints, database schema
```

**Step 4: Security Review (Security Expert)**
```
@workspace Using #file:agentic-framework/sub-agents/security-expert-agent.md,
review OAuth2 design for vulnerabilities:
- Token storage security
- CSRF protection
- XSS prevention
- Rate limiting
Reference: agentic-framework/standards/secure_coding_checklist.md
```

**Step 5: Implementation (Software Developer)**
```
@workspace Using #file:agentic-framework/sub-agents/software-developer-agent.md,
implement OAuth2 authentication based on approved architecture.
Follow: agentic-framework/standards/coding_styleguide.md
```

**Step 6: Validation (QA Engineer)**
```
@workspace Using #file:agentic-framework/sub-agents/QA-engineer-agent.md,
create test suite for OAuth2:
- Unit tests for token validation
- Integration tests for auth flows
- Security tests (invalid tokens, expired sessions)
Reference: agentic-framework/standards/testing_strategy.md
```

**Result**: Feature developed with multi-disciplinary expertise, consistent quality, and documented decisions.

---

### Example 2: Bug Investigation

**Goal**: Debug production performance issue

**Workflow:**

**Step 1: Triage (Master Agent)**
```
@workspace Using #file:agentic-framework/master-agent.md, investigate slow API responses:
Engage: site-reliability-engineer-agent for diagnostics
```

**Step 2: Diagnostics (SRE)**
```
@workspace Using #file:agentic-framework/sub-agents/site-reliability-engineer-agent.md,
analyze performance metrics:
- Response time percentiles (p50, p95, p99)
- Database query performance
- API endpoint latency breakdown
- Resource utilization (CPU, memory, network)
```

**Step 3: Root Cause (Data Scientist if ML-related, or Software Developer)**
```
@workspace Using #file:agentic-framework/sub-agents/software-developer-agent.md,
identify performance bottleneck in [specific endpoint]
```

**Step 4: Solution Design (Solutions Architect)**
```
@workspace Using #file:agentic-framework/sub-agents/solutions-architect-agent.md,
design optimization strategy:
- Caching layer (Redis)
- Database indexing
- Query optimization
- Horizontal scaling
```

**Step 5: Implementation & Validation**
(Software Developer → QA Engineer → SRE for production monitoring)

---

### Example 3: ML Model Development

**Goal**: Build and deploy ML classification model

**Workflow:**

**Master Agent Coordination:**
```
@workspace Using #file:agentic-framework/master-agent.md, coordinate ML model development:
- data-engineer-agent: data pipeline
- data-scientist-agent: model training
- ML-engineer-agent: model deployment
- devops-engineer-agent: infrastructure
- QA-engineer-agent: validation
```

**Data Pipeline (Data Engineer):**
```
@workspace Using #file:agentic-framework/sub-agents/data-engineer-agent.md,
build data pipeline following:
- agentic-framework/standards/data_pipeline_patterns.md
Include: ETL scripts, data validation, schema management
```

**Model Training (Data Scientist):**
```
@workspace Using #file:agentic-framework/sub-agents/data-scientist-agent.md,
train classification model:
- Feature engineering
- Model selection (Random Forest, XGBoost, Neural Network)
- Hyperparameter tuning
- Cross-validation
Reference: agentic-framework/standards/mlops_pipeline_standards.md
```

**Model Deployment (ML Engineer):**
```
@workspace Using #file:agentic-framework/sub-agents/ML-engineer-agent.md,
deploy model to production:
- Containerization (Docker)
- API endpoint (FastAPI)
- Model versioning
- A/B testing setup
Follow: agentic-framework/standards/iac_standards.md
```

**Infrastructure (DevOps Engineer):**
```
@workspace Using #file:agentic-framework/sub-agents/devops-engineer-agent.md,
setup ML infrastructure:
- Kubernetes deployment
- Auto-scaling (HPA)
- Monitoring (Prometheus)
- Logging (ELK stack)
```

---

## Framework Extension

### Adding New Agents

**Step 1: Create Agent File**

**File**: `agentic-framework/sub-agents/my-new-agent.md`

```markdown
---
agent_type: "specialist"
specialization: ["domain1", "domain2"]
tools_compatible: ["tabnine", "github_copilot", "cursor", "codeium", "jetbrains_ai"]
context_scope: "project_wide"
interaction_patterns: ["analysis", "implementation"]
model_suggestions: ["gpt4", "claude_sonnet"]
updated: "2025-10-02"
---

# Persona: My New Agent 🚀

You are a **[Role Title]** with expertise in...

## Core Responsibilities
- Responsibility 1
- Responsibility 2

## Standards Reference
- `agentic-framework/standards/relevant-standard.md`

## Output Format
- Deliverable format 1
- Deliverable format 2

## Interaction Pattern
1. Step 1
2. Step 2
```

**Step 2: Register in Agent Roster**

**File**: `agentic-framework/agent-roster.json`

```json
{
  "agents": [
    {
      "name": "my-new-agent",
      "file": "sub-agents/my-new-agent.md",
      "category": "specialist",
      "specializations": ["domain1", "domain2"],
      "tools_compatible": ["all"]
    }
  ]
}
```

**Step 3: Use in Master Agent**

```
@workspace Using #file:agentic-framework/master-agent.md, engage my-new-agent for [task]
```

---

### Adding New Standards

**Step 1: Create Standard Document**

**File**: `agentic-framework/standards/my-standard.md`

```markdown
# My Standard Document

## Purpose
Define standards for [domain]

## Guidelines
1. Guideline 1
2. Guideline 2

## Examples
[Code examples demonstrating standard]

## Validation Checklist
- [ ] Checklist item 1
- [ ] Checklist item 2
```

**Step 2: Reference in Agents**

Update relevant agent personas:
```markdown
## Standards Reference
- `agentic-framework/standards/my-standard.md`
```

---

## Best Practices

### 1. Always Start with Master Agent

❌ **Don't**:
```
@workspace Create authentication system
```
(Lacks structure, misses specialized expertise)

✅ **Do**:
```
@workspace Using #file:agentic-framework/master-agent.md, plan and implement 
authentication system with appropriate specialized agents
```

### 2. Specify HITL Mode Explicitly

❌ **Don't**:
```
@workspace Build payment integration
```
(Unclear when human should review)

✅ **Do**:
```
@workspace Using master-agent.md with CHECKPOINT mode, build payment integration.
Pause for approval after: requirements, architecture, implementation, testing
```

### 3. Reference Standards Explicitly

❌ **Don't**:
```
@workspace Write secure authentication code
```
(Vague, no concrete standards)

✅ **Do**:
```
@workspace Using software-developer-agent.md, implement authentication following:
- agentic-framework/standards/secure_coding_checklist.md
- agentic-framework/standards/api_design_patterns.md
```

### 4. Use Appropriate Agent Granularity

**Simple Task** (single agent):
```
@workspace Using technical-writer-agent.md, document this API endpoint
```

**Complex Task** (multi-agent via master):
```
@workspace Using master-agent.md, coordinate agents for complete feature development
```

### 5. Maintain Context Files

**Track project state in domain-specific context files:**
- `telco-domain/project-context.md`: Session logs, decisions, continuity
- `telco-domain/project-brief.md`: Requirements, scope, stakeholders

**Update after major changes:**
```
@workspace Update telco-domain/project-context.md with:
- Authentication system implemented (OAuth2)
- Architectural decisions logged
- Security review passed
```

---

## Troubleshooting

### Issue: Agent Not Following Standards

**Problem**: Generated code doesn't match coding style guide

**Solution**: Explicitly reference standard in prompt
```
@workspace Using software-developer-agent.md, refactor this code to match:
agentic-framework/standards/coding_styleguide.md
Show before/after comparison
```

### Issue: Master Agent Skips Agents

**Problem**: Master agent doesn't engage all necessary specialists

**Solution**: Explicitly list required agents
```
@workspace Using master-agent.md, implement feature X with these agents:
1. business-analyst-agent (requirements)
2. solutions-architect-agent (design)
3. security-expert-agent (security review)
4. software-developer-agent (implementation)
5. QA-engineer-agent (testing)
Do NOT skip any agent.
```

### Issue: Context Loss Between Agent Hand-offs

**Problem**: Later agents don't have context from earlier agents

**Solution**: Use `@workspace` scope and reference output files
```
@workspace Using software-developer-agent.md, implement authentication based on:
- docs/architecture/auth-design.md (from architect agent)
- docs/requirements/auth-user-stories.md (from BA agent)
```

---

## Key Takeaways

1. **Master Agent** orchestrates complex, multi-disciplinary tasks
2. **32+ Specialized Agents** provide deep domain expertise
3. **YAML Metadata** ensures universal AI tool compatibility
4. **HITL Workflows** balance automation with human oversight
5. **Standards Integration** maintains consistent quality
6. **Tool-Agnostic Design** works with all major AI assistants
7. **Extensible Framework** easily add new agents and standards
8. **Context Management** maintains continuity across interactions
9. **Explicit References** (#file:) load agent personas reliably
10. **Structured Workflows** (BA → Architect → Developer → QA) ensure quality

The Agentic Framework transforms AI from a single-agent assistant into an orchestrated team of specialists, each expert in their domain, working together under unified standards to deliver production-quality software.

**Ready to Use**: Reference any agent with `#file:agentic-framework/sub-agents/[agent-name].md` and let the framework handle the complexity!
