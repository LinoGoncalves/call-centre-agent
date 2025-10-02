# Agentic AI Framework

**Universal Multi-Agent Orchestration System for Enterprise Software Development**

## 🎯 Overview

This directory contains a **reusable, tool-agnostic agentic AI framework** designed for human-AI collaboration across the full software development lifecycle (SDLC). The framework is completely independent of any specific project domain and can be extracted for use in ANY software project.

## 🚀 Key Features

- **Universal AI Tool Compatibility**: Works seamlessly with Tabnine, GitHub Copilot, Cursor, Codeium, JetBrains AI, and other AI coding assistants
- **Master Agent Orchestration**: Central coordinator that delegates to 22+ specialized agents
- **Rich Metadata Schema**: YAML frontmatter in all agent files for enhanced AI context awareness
- **Comprehensive Standards**: 20+ universal development standards covering API design, security, testing, documentation, and more
- **Human-in-the-Loop (HITL)**: Dynamic oversight modes (stepwise, autonomous, hybrid, standard)
- **Cognitive Enhancement**: Built-in meta-cognitive triggers for complex problem-solving

## 📁 Framework Structure

```
framework/
├── master-agent.md              # 🎯 Master orchestrator (START HERE)
│
├── sub-agents/                  # 22+ specialized agent personas
│   ├── business-analyst-agent.md
│   ├── solutions-architect-agent.md
│   ├── software-developer-agent.md
│   ├── security-expert-agent.md
│   ├── ML-engineer-agent.md
│   ├── data-scientist-agent.md
│   ├── QA-engineer-agent.md
│   ├── devops-engineer-agent.md
│   └── ... (and 14 more)
│
├── standards/                   # Universal development standards
│   ├── api_design_patterns.md
│   ├── architectural-principles.md
│   ├── coding_styleguide.md
│   ├── testing_strategy.md
│   ├── secure_coding_checklist.md
│   ├── security_policies.md
│   ├── database_schema_standards.md
│   ├── iac_standards.md
│   ├── sre_handbook.md
│   └── ... (and 11 more)
│
├── scripts/                     # Framework CLI tools
│   └── cli.py                  # Command-line interface
│
├── templates/                   # Project scaffolding templates
│   ├── framework-management-guide.md
│   ├── project-brief-template.md
│   ├── quality-gates.md
│   └── workflow-state-management.md
│
└── agent-roster.json           # Agent registry and metadata
```

## 🤖 Agent Specializations

The framework includes specialized agents across all SDLC disciplines:

### **Business & Requirements**
- Product Owner Agent
- Business Analyst Agent
- UX Research Agent

### **Architecture & Design**
- Solutions Architect Agent
- Principal Engineer Agent
- UI Designer Agent

### **Development**
- Software Developer Agent
- ML Engineer Agent
- Data Engineer Agent
- Database Engineer Agent

### **Quality Assurance**
- QA Engineer Agent
- Test Manager Agent
- Test Automation Expert Agent

### **Security & Compliance**
- Security Expert Agent
- Network Engineer Agent

### **Operations & Infrastructure**
- DevOps Engineer Agent
- Site Reliability Engineer (SRE) Agent
- Cloud Engineer Agent

### **Process & Governance**
- Project Manager Agent
- Scrum Master Agent
- Technical Writer Agent

### **Advanced Capabilities**
- Critical Analyst Agent (assumption validation, evidence-based decision making)
- Blueprint Executor Agent (systematic implementation, debugging)

## 🚀 Quick Start

### For AI Tools (Tabnine, Copilot, Cursor, etc.)

```bash
# In your AI tool's chat interface
@workspace Load framework/master-agent.md to orchestrate specialized agents
```

### For Human Developers

1. **Start with the Master Agent**: Read `master-agent.md` to understand the orchestration patterns
2. **Explore Specialized Agents**: Browse `sub-agents/` for domain-specific expertise
3. **Review Standards**: Reference `standards/` for best practices
4. **Use Templates**: Apply `templates/` for consistent project structure

### For CLI Workflow

```bash
# Start agentic workflow
python framework/scripts/cli.py start
```

## 📚 Universal Development Standards

The framework includes comprehensive, tool-agnostic standards:

- **API Design**: RESTful patterns, GraphQL, gRPC, versioning
- **Architecture**: Microservices, event-driven, CQRS, clean architecture
- **Coding Style**: Language-agnostic best practices, formatting, naming
- **Testing**: Unit, integration, E2E, TDD, BDD strategies
- **Security**: OWASP Top 10, zero trust, encryption, access control
- **Database**: Schema design, migrations, indexing, normalization
- **Infrastructure as Code**: Terraform, CloudFormation, Bicep patterns
- **SRE**: Observability, incident response, SLOs, capacity planning
- **Documentation**: API docs, architecture diagrams, user guides
- **Agile Ceremonies**: Sprints, retrospectives, planning, standups

## 🔧 How to Use This Framework

### Option 1: Reference in Place

Keep the framework in your project and reference it:

```bash
# Your project structure
your-project/
├── framework/              # This directory
├── your-domain/            # Your domain-specific content
├── src/                    # Your application code
└── ...
```

### Option 2: Extract and Reuse

Copy the entire `framework/` directory to a new project:

```bash
# Copy to new project
cp -r framework/ ../new-project/framework/

# Update references in new project
# Use framework/master-agent.md as the orchestration entry point
```

### Option 3: Package as Dependency

Publish the framework as a separate repository and reference it:

```bash
# Clone framework separately
git clone https://github.com/your-org/agentic-framework.git

# Reference from multiple projects
```

## 🎯 Human Oversight Modes

The framework supports dynamic control over AI autonomy:

- **STEPWISE**: AI proposes each step, human reviews/approves
- **AUTONOMOUS**: AI executes full workflow, pauses at milestones
- **HYBRID**: AI asks for review at key decision points
- **STANDARD**: Default HITL workflow (AI drafts, human approves)

Change modes anytime with: `MODE: [STEPWISE | AUTONOMOUS | HYBRID | STANDARD]`

## 🧠 Cognitive Enhancement

Built-in meta-cognitive triggers automatically engage advanced reasoning:

- **Beast Mode**: For deadline-critical tasks and production issues
- **Quantum Thinking**: For strategic decisions and multi-stakeholder scenarios
- **Critical Analysis**: For assumption validation and risk assessment

## 🔗 Integration with Your Project

### 1. Load the Master Agent

Point your AI tool to `framework/master-agent.md` as the orchestration entry point.

### 2. Define Your Domain Context

Create a separate directory (e.g., `your-domain/`) with:
- Project brief and requirements
- Domain-specific standards
- Business rules and logic
- Project context files

### 3. Build Your Application

Keep application code in `src/`, tests in `tests/`, etc.

### 4. Leverage Framework Standards

Reference `framework/standards/` for universal best practices.

## 📖 Documentation

- **`master-agent.md`**: Complete orchestration guide and workflow patterns
- **`sub-agents/*.md`**: Individual agent capabilities and prompts
- **`standards/*.md`**: Detailed development standards and guidelines
- **`templates/*.md`**: Reusable project templates

## 🤝 Contributing

To add new agents or standards to the framework:

1. Follow the YAML metadata schema in existing agent files
2. Ensure tool-agnostic approach (works with all AI coding assistants)
3. Document cognitive triggers and interaction patterns
4. Add to `agent-roster.json` registry

## 📜 License

This framework is designed to be reusable and shareable. Check the project root for license details.

## 🎉 Framework Philosophy

**"AI Drafts, Human Approves"**

The core principle is collaboration, not replacement. Every specialized agent produces a first draft that humans review, refine, and approve. The framework enhances human capabilities without removing human judgment from the critical path.

---

**Ready to orchestrate?** Start with `framework/master-agent.md` 🚀
