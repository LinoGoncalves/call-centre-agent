# GitHub Copilot Instructions for Call Centre Agent System

## 🎯 Project Overview

This is a sophisticated multi-agent call centre system with **universal AI tool integration**. While you're GitHub Copilot, this project is designed to work seamlessly with Tabnine, Cursor, Codeium, JetBrains AI, and other tools without vendor lock-in.

## 📋 Universal Standards Reference

**IMPORTANT**: Always reference the main project standards located in the universal structure:

### Primary Standards Location
- **`telco-call-centre/development-standards/`** - All coding guidelines and project standards
- **`telco-call-centre/master-agent.md`** - Central project orchestration and coordination  
- **`telco-call-centre/ai-tool-integration.md`** - Comprehensive multi-tool usage patterns
- **`telco-call-centre/agent-roster.json`** - Complete agent mapping and specializations
- **`telco-call-centre/project-context.json`** - Tool-agnostic project configuration

### Agent System Architecture
All agent personas are located in **`telco-call-centre/sub-agents/`** with enhanced YAML frontmatter metadata for improved context awareness across all AI tools.

## 🤖 Agent Orchestration Patterns

### Master Agent Coordination
When handling complex tasks, **always start with the master agent**:

```bash
@workspace Acting as the master orchestrator from telco-call-centre/master-agent.md, coordinate the appropriate specialized agents for this task
```

### Multi-Agent Workflows
For complex features requiring multiple disciplines:

```bash
@workspace Using telco-call-centre/master-agent.md orchestration, coordinate these agents:
- telco-call-centre/sub-agents/business-analyst-agent.md for requirements
- telco-call-centre/sub-agents/solutions-architect-agent.md for system design
- telco-call-centre/sub-agents/software-developer-agent.md for implementation
```

### Specialized Agent References
For domain-specific tasks, reference the appropriate specialist:

```bash
@workspace Following telco-call-centre/sub-agents/[AGENT-NAME]-agent.md specialization, [TASK DESCRIPTION]
```

## 🛠️ Development Standards Compliance

### Code Generation
Always reference universal standards:
- **Coding Style**: `telco-call-centre/development-standards/coding_styleguide.md`
- **API Design**: `telco-call-centre/development-standards/api_design_patterns.md`  
- **Testing**: `telco-call-centre/development-standards/testing_strategy.md`
- **Security**: `telco-call-centre/development-standards/secure_coding_checklist.md`

### Architecture Decisions
For system design tasks:
- **Architecture Principles**: `telco-call-centre/development-standards/architectural-principles.md`
- **Cloud Standards**: `telco-call-centre/development-standards/iac_standards.md`
- **Network Policies**: `telco-call-centre/development-standards/network_security_policy.md`

## 🔧 Tool Integration Awareness

### Multi-Tool Compatibility
Remember that this project supports multiple AI tools:
- **Tabnine** (primary user preference)
- **GitHub Copilot** (you!)
- **Cursor, Codeium, JetBrains AI** (universal support)

### Vendor-Neutral Approach
- Never suggest GitHub-specific solutions that would break other tools
- Always reference the universal `telco-call-centre/` structure  
- Maintain tool-agnostic recommendations
- Support the established YAML metadata system in agent files

## 📁 Project Structure Awareness

### Core Components
- **`enhanced_classifier.py`** - Main AI classification engine with Gemini integration
- **`streamlit_demo.py`** - Interactive demo interface with HTML sanitization
- **`launch_demo.py`** - Demo launcher script
- **`telco-call-centre/`** - Complete agent system with universal AI tool metadata

### Configuration Files
- **`.env`** - Environment variables (Google API key)
- **`pyproject.toml`** - Python project configuration
- **`project-context.md`** - Comprehensive project documentation

## 🎨 Code Style and Patterns

### Python Conventions
Follow established patterns in the codebase:
- Use type hints consistently
- Implement comprehensive error handling
- Follow the HTML sanitization patterns established in `streamlit_demo.py`
- Maintain the multi-layer defense approach for security

### Agent Integration
When working with agent files:
- Preserve YAML frontmatter metadata structure
- Maintain `agent_type`, `specialization`, `tools_compatible` fields
- Keep `context_scope` and `interaction_patterns` consistent
- Support the universal AI tool integration framework

## ⚡ Performance and Quality

### Testing Standards
- Reference `telco-call-centre/development-standards/testing_strategy.md`
- Use appropriate test frameworks for the component type
- Follow established test patterns in existing codebase

### Security Considerations
- Always apply HTML sanitization for user inputs
- Follow `telco-call-centre/development-standards/secure_coding_checklist.md`
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
- Always reference `telco-call-centre/` structure
- Support YAML metadata enhancements in agent files
- Maintain tool-agnostic approach
- Preserve vendor independence

---

**Remember**: This project's strength lies in its universal AI tool integration. While optimizing for GitHub Copilot, always maintain compatibility with Tabnine (primary preference), Cursor, Codeium, and JetBrains AI. The `telco-call-centre/` structure is the source of truth for all tools.