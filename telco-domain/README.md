# Telco Call Centre - Domain Context

**Telecommunications Call Centre AI Agent System - Domain-Specific Knowledge Base**

## 🎯 Overview

This directory contains all **telecommunications call centre domain-specific** content, including project requirements, business rules, and telco-focused development standards. This content is separate from the universal agentic framework to enable clear separation of concerns.

## 📁 Domain Structure

```
telco-domain/
├── project-brief.md                    # Project vision, scope, and requirements
├── project-context.md                  # Continuity tracking and session logs
├── project-context.json                # Machine-readable project metadata
├── BRANCHING_IMPLEMENTATION_GUIDE.md   # Git workflow for this project
│
├── business-rules/                     # Telco-specific business logic
│   └── Business Rules/                 # Captured business rules
│
├── standards/                          # Telco-specific development standards
│   ├── mlops_pipeline_standards.md    # MLOps with telco LLM context
│   ├── network_standards.md           # Telco network requirements
│   ├── network_security_policy.md     # Telco compliance and security
│   └── approved_libraries.json        # Project-specific dependencies
│
└── LEGACY_README.md                   # Historical README (reference only)
```

## 🚀 Project Overview

### Call Centre AI Agent System

An advanced AI-powered ticket classification and routing system designed for telecommunications customer support operations.

**Key Features:**
- **99.5%+ Accuracy**: Hybrid ensemble (Traditional ML + Google Gemini LLM)
- **6 Categories**: BILLING, TECHNICAL, SALES, COMPLAINTS, NETWORK, ACCOUNT
- **AI Reasoning**: Detailed explanations for every classification
- **Sentiment Analysis**: Critical, negative, neutral, positive detection
- **Departmental Routing**: Intelligent agent assignment with skill matching
- **Priority Levels**: P1_HIGH, P2_MEDIUM, P3_LOW based on urgency and sentiment

**Technology Stack:**
- **ML/AI**: Google Gemini LLM, scikit-learn, transformers
- **Backend**: Python 3.13, FastAPI
- **Frontend**: Streamlit (interactive demo)
- **Data**: Pandas, NumPy
- **Infrastructure**: Docker, Azure (planned)

## 📋 Domain-Specific Standards

### MLOps Pipeline Standards
- Optimized for telco LLM workflows
- Includes ticket classification pipeline patterns
- Addresses telco-specific compliance (POPIA, GDPR)
- Model versioning and A/B testing strategies

### Network Standards
- Telecommunications network requirements
- Call centre infrastructure considerations
- Agent routing and load balancing
- Real-time processing constraints

### Network Security Policy
- Telco compliance frameworks (POPIA, GDPR)
- Customer data protection
- PII handling and masking
- Audit logging requirements

### Approved Libraries
- Project-specific Python dependencies
- Version constraints for stability
- Security-vetted packages only

## 🎯 Business Rules

The `business-rules/` directory contains captured business logic specific to telecommunications call centre operations:

- Ticket categorization rules
- Priority escalation thresholds
- Departmental routing logic
- SLA requirements
- Customer sentiment scoring
- Agent skill mapping

## 📖 Project Documentation

### project-brief.md
Complete project vision, scope, deliverables, and technical requirements. **Start here** for project context.

### project-context.md
Session logs and continuity tracking for AI agent handoffs. Enables seamless work resumption across sessions.

### project-context.json
Machine-readable project metadata for tooling and automation.

### BRANCHING_IMPLEMENTATION_GUIDE.md
Git workflow strategy for the project (Git Flow with feature branches).

## 🔗 Integration with Framework

This domain content integrates with the universal agentic framework located in `../framework/`:

```
call-centre-agent/
├── framework/                  # Universal agentic AI framework
│   ├── master-agent.md        # Orchestrator
│   ├── sub-agents/            # 22+ specialized agents
│   └── standards/             # Universal dev standards
│
├── telco-domain/              # THIS DIRECTORY
│   ├── project-brief.md       # Telco project requirements
│   ├── business-rules/        # Telco business logic
│   └── standards/             # Telco-specific standards
│
├── src/                       # Application code
│   ├── models/                # ML models & classifiers
│   └── ui/                    # Streamlit demo
│
└── ... rest of application
```

## 🤖 Using with AI Tools

When working with AI coding assistants (Tabnine, GitHub Copilot, Cursor, etc.):

1. **Load Framework First**: Point to `../framework/master-agent.md`
2. **Provide Domain Context**: Reference this directory for project-specific requirements
3. **Apply Standards**: Combine universal framework standards with telco-specific standards

Example prompt:
```
@workspace Using framework/master-agent.md orchestration and telco-domain/project-brief.md 
requirements, implement [feature] following both universal and telco-specific standards.
```

## 📊 Project Status (October 2025)

### ✅ Completed
- Hybrid ML/LLM classification system (99.5%+ accuracy)
- Google Gemini LLM integration with reasoning
- Sentiment analysis and priority detection
- Departmental routing with skill matching
- Interactive Streamlit demo
- Comprehensive test suite
- Docker containerization
- Complete development standards
- Universal agentic framework integration

### 🔄 In Progress
- Python file reorganization (completed)
- Framework/domain separation (in progress)
- Documentation updates

### 📋 Roadmap
- MLOps pipeline with monitoring
- Production deployment to Azure
- A/B testing framework
- Advanced analytics dashboard
- Multi-language support

## 🎓 Learning from This Project

This project demonstrates:
- **Framework Reusability**: Clear separation enables framework extraction
- **Domain Clarity**: Business logic isolated from universal patterns
- **Standard Organization**: Universal vs domain-specific standards properly split
- **AI Collaboration**: Human-AI collaboration patterns across SDLC

## 💡 Best Practices

1. **Keep Framework Independent**: Never put domain logic in `../framework/`
2. **Document Domain Assumptions**: Capture telco-specific assumptions in business rules
3. **Maintain Standard Hygiene**: Update telco standards as requirements evolve
4. **Track Context**: Use `project-context.md` for session continuity

## 📞 Stakeholders

- **Product Owner**: Defines requirements and priorities
- **Development Team**: Implements features per standards
- **Data Science Team**: Optimizes ML/LLM models
- **Security Team**: Ensures compliance and data protection
- **Operations Team**: Deploys and monitors production systems

## 🔒 Compliance & Security

This project handles sensitive customer data and must comply with:
- **POPIA** (Protection of Personal Information Act - South Africa)
- **GDPR** (General Data Protection Regulation - EU)
- **Telco Industry Standards**: Call centre data handling requirements
- **PII Protection**: Customer information masking and encryption

All standards are documented in `standards/network_security_policy.md`.

---

**For Framework Documentation**: See `../framework/README.md`  
**For Application Code**: See `../src/`  
**For Project Requirements**: Start with `project-brief.md`

🚀 **Let's build intelligent call centre automation!**
