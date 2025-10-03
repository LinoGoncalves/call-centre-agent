# GitHub Copilot Instructions for Call Centre Agent System

## 🎯 Project Overview

This is a sophisticated multi-agent call centre system with **universal AI tool integration**. While you're GitHub Copilot, this project is designed to work seamlessly with Tabnine, Cursor, Codeium, JetBrains AI, and other tools without vendor lock-in.

## 📋 Universal Standards Reference

**IMPORTANT**: Always reference the framework and domain standards in their new locations:

### Framework Location (Universal, Reusable)
- **`agentic-framework/standards/`** - Universal coding guidelines and best practices
- **`agentic-framework/master-agent.md`** - Central orchestration and coordination  
- **`agentic-framework/sub-agents/`** - 22+ specialized agent personas
- **`agentic-framework/agent-roster.json`** - Complete agent mapping and specializations
- **`agentic-framework/templates/`** - Reusable project templates

### Domain Location (Telco-Specific)
- **`telco-domain/project-brief.md`** - Project requirements and scope
- **`telco-domain/project-context.md`** - Session logs and continuity tracking
- **`telco-domain/standards/`** - Telco-specific development standards
- **`telco-domain/business-rules/`** - Telco business logic

### Agent System Architecture
All agent personas are located in **`agentic-framework/sub-agents/`** with enhanced YAML frontmatter metadata for improved context awareness across all AI tools.

## 🤖 Agent Orchestration Patterns

### Master Agent Coordination
When handling complex tasks, **always start with the master agent**:

```bash
@workspace Acting as the master orchestrator from agentic-framework/master-agent.md, coordinate the appropriate specialized agents for this task
```

### Multi-Agent Workflows
For complex features requiring multiple disciplines:

```bash
@workspace Using agentic-framework/master-agent.md orchestration, coordinate these agents:
- agentic-framework/sub-agents/business-analyst-agent.md for requirements
- agentic-framework/sub-agents/solutions-architect-agent.md for system design
- agentic-framework/sub-agents/software-developer-agent.md for implementation
```

### Specialized Agent References
For domain-specific tasks, reference the appropriate specialist:

```bash
@workspace Following agentic-framework/sub-agents/[AGENT-NAME]-agent.md specialization, [TASK DESCRIPTION]
```

## 🛠️ Development Standards Compliance

### Code Generation
Always reference universal standards:
- **Coding Style**: `agentic-framework/standards/coding_styleguide.md`
- **API Design**: `agentic-framework/standards/api_design_patterns.md`  
- **Testing**: `agentic-framework/standards/testing_strategy.md`
- **Security**: `agentic-framework/standards/secure_coding_checklist.md`

### Architecture Decisions
For system design tasks:
- **Architecture Principles**: `agentic-framework/standards/architectural-principles.md`
- **Cloud Standards**: `agentic-framework/standards/iac_standards.md`
- **Network Policies**: `telco-domain/standards/network_security_policy.md`

## 🔧 Tool Integration Awareness

### Multi-Tool Compatibility
Remember that this project supports multiple AI tools:
- **Tabnine** (primary user preference)
- **GitHub Copilot** (you!)
- **Cursor, Codeium, JetBrains AI** (universal support)

### Vendor-Neutral Approach
- Never suggest GitHub-specific solutions that would break other tools
- Always reference the universal `agentic-framework/` structure for reusable components
- Reference `telco-domain/` for project-specific context
- Maintain tool-agnostic recommendations
- Support the established YAML metadata system in agent files

## 📁 Project Structure Awareness

### Core Components
- **`src/models/enhanced_classifier.py`** - Main AI classification engine with Gemini integration
- **`src/ui/streamlit_demo.py`** - Interactive demo interface with HTML sanitization
- **`launch_demo.py`** - Demo launcher script
- **`agentic-framework/`** - Complete agentic AI framework with universal AI tool metadata
- **`telco-domain/`** - Telco-specific project context and business rules

### Configuration Files
- **`.env`** - Environment variables (Google API key)
- **`pyproject.toml`** - Python project configuration
- **`telco-domain/project-context.md`** - Comprehensive project documentation

## 🎨 Code Style and Patterns

### Python Conventions
Follow established patterns in the codebase:
- Use type hints consistently
- Implement comprehensive error handling
- Follow the HTML sanitization patterns established in `src/ui/streamlit_demo.py`
- Maintain the multi-layer defense approach for security

### Agent Integration
When working with agent files:
- Preserve YAML frontmatter metadata structure
- Maintain `agent_type`, `specialization`, `tools_compatible` fields
- Keep `context_scope` and `interaction_patterns` consistent
- Support the universal AI tool integration framework
- Maintain `agent_type`, `specialization`, `tools_compatible` fields
- Keep `context_scope` and `interaction_patterns` consistent
- Support the universal AI tool integration framework

## ⚡ Performance and Quality

### Testing Standards
- Reference `agentic-framework/standards/testing_strategy.md`
- Use appropriate test frameworks for the component type
- Follow established test patterns in existing codebase

### Security Considerations
- Always apply HTML sanitization for user inputs
- Follow `agentic-framework/standards/secure_coding_checklist.md`
- Implement proper input validation and error handling

## 🚀 Project Goals Alignment

### Primary Objectives
1. **Universal AI Tool Support** - Maintain compatibility across all supported tools
2. **Agent Orchestration** - Leverage the multi-agent system for specialized tasks
3. **Quality Standards** - Follow comprehensive development standards
4. **Security First** - Implement robust security practices
5. **Performance** - Optimize for production telecommunications workloads

### Key Success Metrics
- All AI tools can effectively utilize the agent system
- Code follows universal standards accessible to all tools
- Agent orchestration provides specialized expertise
- Security and performance requirements are met

## 🌿 Git Workflow Compliance

### CRITICAL: Before Any Commit

**All AI assistants must validate git workflow before committing code.**

#### Pre-Commit Checklist (MANDATORY)

1. **Check Current Branch**
   ```bash
   git branch --show-current
   ```
   - ❌ If on `main` or `develop`: **STOP** and alert user
   - ✅ If on `feature/*`, `hotfix/*`, `bugfix/*`: Proceed

2. **Reference Branching Strategy**
   - Primary: `telco-domain/BRANCHING_IMPLEMENTATION_GUIDE.md`
   - Universal: `agentic-framework/standards/git_workflow_standards.md`
   - Verify project type (production/internal/toy)

3. **Alert User on Workflow Deviation**
   ```
   ⚠️ WARNING: You are on the 'main' branch (protected).
   
   Documented strategy requires:
   - Create feature branch: git checkout -b feature/descriptive-name
   - Make changes on feature branch
   - Create PR to merge back to develop/main
   
   Is this a toy project? Reply "toy project" to bypass workflow.
   ```

4. **Get Explicit Bypass Permission**
   - For toy/learning projects: User must confirm "this is a toy project"
   - For production projects: Never bypass, enforce workflow strictly

### Workflow for AI Assistants

When user requests "commit", "push", or "upload changes":

**Step 1: Validate Context**
```bash
# Check what branch we're on
git branch --show-current

# Check if uncommitted changes exist
git status
```

**Step 2: Branch Validation Logic**
```
IF current_branch IN ["main", "develop"]:
    ALERT USER:
    "🚨 You're on a protected branch ({current_branch}).
    
    Per {project_branching_guide}, changes should be made on feature branches.
    
    Recommended action:
    1. Create feature branch: git checkout -b feature/your-feature-name
    2. Make your changes
    3. Create PR for review
    
    Is this a toy project where direct commits are acceptable?"
    
    WAIT FOR USER CONFIRMATION before proceeding
ELSE:
    PROCEED with commit
```

**Step 3: Commit Message Validation**
- Follow Conventional Commits format: `<type>(<scope>): <description>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Examples:
  - ✅ `feat(routing): add priority-based queue assignment`
  - ✅ `fix(classifier): handle empty department field`
  - ❌ `updated stuff`
  - ❌ `WIP`

**Step 4: Post-Commit Guidance**
```
✅ Changes committed to {branch_name}

Next steps:
- Push to remote: git push -u origin {branch_name}
- Create Pull Request: {branch_name} → develop
- Request review from team lead

For toy projects, you can push directly to main if confirmed.
```

### Emergency Bypass Protocol

**When User Says "Toy Project"**:
```
Acknowledged: Toy project mode enabled.

Bypassing workflow validation for this session.
Direct commits to main are permitted.

Note: For production projects, always follow the documented branching strategy.

Proceeding with commit...
```

### AI Assistant Education Role

When workflow violations are detected, educate the user:

```
💡 Git Workflow Best Practice

Instead of committing directly to main, consider:

1. **Feature Development**:
   git checkout -b feature/add-new-feature
   # Make changes
   git commit -m "feat(scope): add new feature"
   git push -u origin feature/add-new-feature
   # Create PR on GitHub

2. **Benefits**:
   - Code review before production
   - Easy rollback if issues found
   - Clear feature development history
   - Collaboration with team members

3. **When to Bypass**:
   - Toy/learning projects (like this one)
   - Personal repositories
   - Prototype/experimentation

For this project, you've confirmed it's a toy project, so direct commits are fine.
```

### Workflow Validation Examples

**Example 1: User on Main Branch** ❌
```
User: "Commit these changes to GitHub"

AI Response:
⚠️ Hold on! You're currently on the 'main' branch.

According to telco-domain/BRANCHING_IMPLEMENTATION_GUIDE.md, all changes
should go through feature branches and pull requests.

Options:
1. Create feature branch (recommended):
   git checkout -b feature/your-changes
   
2. If this is a toy project, confirm to bypass:
   Reply with "toy project" to proceed with direct main commit

What would you like to do?
```

**Example 2: User on Feature Branch** ✅
```
User: "Commit these changes"

AI Response:
✅ You're on 'feature/priority-routing' - perfect!

Committing with message:
"feat(routing): implement priority-based queue assignment"

git commit -m "feat(routing): implement priority-based queue assignment"
git push -u origin feature/priority-routing

Next step: Create PR from feature/priority-routing → develop
```

**Example 3: Toy Project Confirmed** ✅
```
User: "This is a toy project, just commit to main"

AI Response:
✅ Toy project mode: Bypassing workflow validation.

Committing directly to main:
git commit -m "feat(classifier): add Gemini integration"
git push origin main

Note: For production projects, always use feature branches + PRs.
```

## 💡 Best Practices

### When to Use Master Agent
Use master agent orchestration for:
- Multi-disciplinary feature development
- Complex architectural decisions  
- Quality assurance coordination
- Cross-functional workflow management

### When to Use Specialized Agents
Reference specific agents for:
- Domain expertise (security, data science, UI/UX)
- Specialized code generation
- Technical domain guidance
- Standards compliance in specific areas

### Universal Compatibility
- Always reference `agentic-framework/` structure for reusable components
- Reference `telco-domain/` for project-specific context
- Support YAML metadata enhancements in agent files
- Maintain tool-agnostic approach
- Preserve vendor independence

---

**Remember**: This project's strength lies in its universal AI tool integration. While optimizing for GitHub Copilot, always maintain compatibility with Tabnine (primary preference), Cursor, Codeium, and JetBrains AI. The `agentic-framework/` structure is the source of truth for all tools.