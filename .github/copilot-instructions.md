# GitHub Copilot Instructions for Call Centre Agent System

## 🎯 Project Overview

This is a sophisticated multi-agent call centre system with **universal AI tool integration**. While you're GitHub Copilot, this project is designed to work seamlessly with Tabnine, Cursor, Codeium, JetBrains AI, and other tools without vendor lock-in.

## 📋 Universal Standards Reference

**IMPORTANT**: Always reference the framework and domain standards in their new locations:

### Framework Location (Universal, Reusable)
- **`framework/standards/`** - Universal coding guidelines and best practices
- **`framework/master-agent.md`** - Central orchestration and coordination  
- **`framework/sub-agents/`** - 22+ specialized agent personas
- **`framework/agent-roster.json`** - Complete agent mapping and specializations
- **`framework/templates/`** - Reusable project templates

### Domain Location (Telco-Specific)
- **`telco-domain/project-brief.md`** - Project requirements and scope
- **`telco-domain/project-context.md`** - Session logs and continuity tracking
- **`telco-domain/standards/`** - Telco-specific development standards
- **`telco-domain/business-rules/`** - Telco business logic

### Agent System Architecture
All agent personas are located in **`framework/sub-agents/`** with enhanced YAML frontmatter metadata for improved context awareness across all AI tools.

## 🤖 Agent Orchestration Patterns

### Master Agent Coordination
When handling complex tasks, **always start with the master agent**:

```bash
@workspace Acting as the master orchestrator from framework/master-agent.md, coordinate the appropriate specialized agents for this task
```

### Multi-Agent Workflows
For complex features requiring multiple disciplines:

```bash
@workspace Using framework/master-agent.md orchestration, coordinate these agents:
- framework/sub-agents/business-analyst-agent.md for requirements
- framework/sub-agents/solutions-architect-agent.md for system design
- framework/sub-agents/software-developer-agent.md for implementation
```

### Specialized Agent References
For domain-specific tasks, reference the appropriate specialist:

```bash
@workspace Following framework/sub-agents/[AGENT-NAME]-agent.md specialization, [TASK DESCRIPTION]
```

## 🛠️ Development Standards Compliance

### Code Generation
Always reference universal standards:
- **Coding Style**: `framework/standards/coding_styleguide.md`
- **API Design**: `framework/standards/api_design_patterns.md`  
- **Testing**: `framework/standards/testing_strategy.md`
- **Security**: `framework/standards/secure_coding_checklist.md`

### Architecture Decisions
For system design tasks:
- **Architecture Principles**: `framework/standards/architectural-principles.md`
- **Cloud Standards**: `framework/standards/iac_standards.md`
- **Network Policies**: `telco-domain/standards/network_security_policy.md`

## 🔧 Tool Integration Awareness

### Multi-Tool Compatibility
Remember that this project supports multiple AI tools:
- **Tabnine** (primary user preference)
- **GitHub Copilot** (you!)
- **Cursor, Codeium, JetBrains AI** (universal support)

### Vendor-Neutral Approach
- Never suggest GitHub-specific solutions that would break other tools
- Always reference the universal `framework/` structure for reusable components
- Reference `telco-domain/` for project-specific context
- Maintain tool-agnostic recommendations
- Support the established YAML metadata system in agent files

## 📁 Project Structure Awareness

### Core Components
- **`src/models/enhanced_classifier.py`** - Main AI classification engine with Gemini integration
- **`src/ui/streamlit_demo.py`** - Interactive demo interface with HTML sanitization
- **`launch_demo.py`** - Demo launcher script
- **`framework/`** - Complete agentic AI framework with universal AI tool metadata
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
- Reference `framework/standards/testing_strategy.md`
- Use appropriate test frameworks for the component type
- Follow established test patterns in existing codebase

### Security Considerations
- Always apply HTML sanitization for user inputs
- Follow `framework/standards/secure_coding_checklist.md`
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
- Always reference `framework/` structure for reusable components
- Reference `telco-domain/` for project-specific context
- Support YAML metadata enhancements in agent files
- Maintain tool-agnostic approach
- Preserve vendor independence

---

**Remember**: This project's strength lies in its universal AI tool integration. While optimizing for GitHub Copilot, always maintain compatibility with Tabnine (primary preference), Cursor, Codeium, and JetBrains AI. The `framework/` structure is the source of truth for all tools.