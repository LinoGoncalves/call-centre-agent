# Call Centre Agent - AI Assistant Project Context Guide

> **Universal AI Tool Compatibility**: This project is designed to work seamlessly with GitHub Copilot, Tabnine, Cursor, Codeium, JetBrains AI, and other AI coding assistants without vendor lock-in.

## 🎯 Project Overview

**Call Centre Agent System** is a sophisticated multi-agent telecommunications call centre with universal AI tool integration, featuring advanced ticket classification, routing intelligence, and multi-provider LLM support.

### Core Mission
- **Multi-Agent Architecture**: 22+ specialized AI agent personas for different domains
- **Universal Compatibility**: Works with any AI coding assistant (Tabnine, Copilot, Cursor, etc.)
- **Production Ready**: Telecommunications-grade system with security, performance, and scalability
- **Intelligent Routing**: Rules Engine → Vector DB → LLM pipeline for optimal performance/cost

---

## 📁 Project Structure Guide

### **🏗️ Framework Layer (Universal, Reusable)**
```
agentic-framework/
├── master-agent.md           # 🧠 Central orchestration and coordination
├── sub-agents/              # 🤖 22+ specialized agent personas
│   ├── business-analyst-agent.md
│   ├── solutions-architect-agent.md
│   ├── software-developer-agent.md
│   ├── security-specialist-agent.md
│   └── [18+ more specialized agents]
├── agent-roster.json        # 📋 Complete agent mapping and specializations
├── standards/               # 📖 Universal coding guidelines and best practices
│   ├── coding_styleguide.md
│   ├── api_design_patterns.md
│   ├── testing_strategy.md
│   └── secure_coding_checklist.md
└── templates/               # 🎨 Reusable project templates
```

### **🏢 Domain Layer (Telco-Specific)**
```
telco-domain/
├── project-brief.md         # 📋 Project requirements and scope
├── project-context.md       # 📝 Session logs and continuity tracking
├── standards/               # 📖 Telco-specific development standards
└── business-rules/          # 💼 Telco business logic and regulations
```

### **💻 Core Application**
```
src/
├── models/                  # 🤖 AI Classification & Routing
│   ├── enhanced_classifier.py      # Main Gemini LLM integration
│   ├── multi_provider_manager.py   # Multi-LLM orchestration (Gemini + Ollama)
│   ├── opensource_llm.py           # Ollama local LLM integration
│   ├── rules_engine.py             # High-speed pattern matching
│   └── config_manager.py           # Configuration management
├── ui/                      # 🎨 Streamlit Demo Interface
│   ├── streamlit_demo.py           # Main demo application
│   └── pipeline_visualization.py   # Step-by-step routing visualization
├── vector_db/               # 🗃️ Vector Database Integration
│   ├── pinecone_client.py          # Cloud vector search
│   └── chromadb_client.py          # Local vector storage
└── utils/                   # 🛠️ Utilities and helpers
```

---

## 🤖 Agent Orchestration System

### **Master Agent Coordination**
All complex tasks should start with the master agent for proper coordination:

```bash
@workspace Acting as the master orchestrator from agentic-framework/master-agent.md, coordinate the appropriate specialized agents for this task
```

### **Specialized Agent Usage**
For domain-specific work, reference the appropriate specialist:

```bash
@workspace Following agentic-framework/sub-agents/[AGENT-NAME]-agent.md specialization, [TASK DESCRIPTION]
```

### **Multi-Agent Workflows**
For complex features requiring multiple disciplines:

```bash
@workspace Using agentic-framework/master-agent.md orchestration, coordinate these agents:
- agentic-framework/sub-agents/business-analyst-agent.md for requirements
- agentic-framework/sub-agents/solutions-architect-agent.md for system design  
- agentic-framework/sub-agents/software-developer-agent.md for implementation
```

---

## 🏗️ System Architecture

### **Multi-Provider LLM Support**
- **Primary**: Google Gemini Pro (Cloud API)
- **Local**: Ollama integration for offline/private inference
- **Fallback**: Automatic switching when providers unavailable
- **Cost Optimization**: Rules Engine → Vector DB → LLM pipeline

### **Vector Database Options**
- **Pinecone**: Cloud-scale vector search with 1536-dim embeddings
- **ChromaDB**: Local vector storage for privacy/cost optimization
- **Automatic Switching**: Based on user configuration

### **Classification Pipeline**
```
📨 Customer Ticket
    ↓
🔧 Rules Engine (Instant <1ms routing)
    ├─ 85-99% confidence → IMMEDIATE ROUTE
    └─ <85% confidence ↓
🔍 Vector Search (Historical patterns ~45ms)
    ├─ 70-84% confidence → CONTEXTUAL ROUTE
    └─ <70% confidence ↓
🤖 LLM Analysis (Complex reasoning ~850ms)
    └─ Full AI classification with reasoning
```

---

## 🔧 Development Standards Reference

### **Framework Standards (Universal)**
- **Code Style**: `agentic-framework/standards/coding_styleguide.md`
- **API Design**: `agentic-framework/standards/api_design_patterns.md`
- **Testing**: `agentic-framework/standards/testing_strategy.md`
- **Security**: `agentic-framework/standards/secure_coding_checklist.md`

### **Domain Standards (Telco-Specific)**  
- **Architecture**: `agentic-framework/standards/architectural-principles.md`
- **Network Security**: `telco-domain/standards/network_security_policy.md`
- **Business Rules**: `telco-domain/business-rules/`

---

## 🚀 Quick Start for New AI Assistants

### **1. Initial Assessment**
```bash
# Check project health
python -c "from src.models.multi_provider_manager import MultiProviderManager; print('System Status: READY')"

# Validate environment
python validate_setup.py
```

### **2. Launch Demo**
```bash
# Start the main demo
python launch_demo.py
# OR for intelligent mode
python launch_demo_intelligent.py
```

### **3. Key Configuration Files**
- **Environment**: `.env` (Google API key for Gemini)
- **User Settings**: `user_config.json` (auto-generated)
- **Provider Config**: `provider_config.json` (LLM/Vector DB preferences)

---

## 🛠️ Common Development Tasks

### **Adding New Classification Categories**
1. Update rules in `src/models/rules_engine.py`
2. Add training data to `data/telecoms_tickets_*.csv`
3. Retrain models: `python -m src.models.enhanced_classifier`

### **Integrating New LLM Providers**
1. Follow pattern in `src/models/opensource_llm.py`
2. Register in `src/models/multi_provider_manager.py`
3. Update UI options in `src/ui/streamlit_demo.py`

### **Adding New Agent Personas**
1. Create new agent file in `agentic-framework/sub-agents/`
2. Include YAML frontmatter with metadata
3. Update `agentic-framework/agent-roster.json`

---

## 🔍 Debugging & Troubleshooting

### **Common Issues & Solutions**

**🚨 Demo Won't Launch**
```bash
# Check dependencies
pip install -r requirements.txt

# Verify API keys
python -c "import os; print('Gemini API:', 'SET' if os.getenv('GOOGLE_API_KEY') else 'MISSING')"
```

**🔧 Classification Errors**
```bash
# Test individual components
python -c "from src.models.enhanced_classifier import GeminiEnhancedClassifier; GeminiEnhancedClassifier().classify_ticket('test')"
```

**🌐 Provider Fallback Issues**
- Check logs for "Ollama not available - will use fallback"
- Verify provider display shows actual vs selected provider
- Pipeline visualization should indicate fallback scenarios

---

## 📊 Performance Optimization

### **Routing Intelligence Hierarchy**
1. **Rules Engine**: Instant pattern matching (sub-millisecond)
2. **Vector Search**: Historical similarity (40-60ms)
3. **LLM Analysis**: Complex reasoning (500-1000ms)

### **Cost Optimization**
- **FREE**: Ollama (Local) + ChromaDB (Local)
- **LOW**: Ollama (Local) + Pinecone (Cloud)
- **MEDIUM**: Gemini (Cloud) + ChromaDB (Local)
- **PREMIUM**: Gemini (Cloud) + Pinecone (Cloud)

---

## 🔐 Security & Privacy

### **Data Protection**
- **Local Mode**: Full privacy with Ollama + ChromaDB
- **Hybrid Mode**: Sensitive data stays local, processing in cloud
- **HTML Sanitization**: Multi-layer defense against XSS
- **Input Validation**: Comprehensive request sanitization

### **API Key Management**
- **Environment Variables**: `.env` file for secrets
- **Secure Transmission**: HTTPS for all external API calls
- **Fallback Security**: No degraded security in fallback scenarios

---

## 🎯 Future Development Priorities

### **Immediate Enhancements**
1. **Agent Persona Expansion**: Add more specialized domain experts
2. **Multi-Language Support**: Extend beyond English classification
3. **Real-Time Analytics**: Dashboard for system performance
4. **Custom Rule Builder**: UI for business users to create routing rules

### **Advanced Features**
1. **Conversation Continuity**: Multi-turn ticket handling
2. **Sentiment Escalation**: Automatic priority adjustment based on customer emotion
3. **Knowledge Graph**: Relationship mapping between tickets and resolutions
4. **Federated Learning**: Privacy-preserving model improvements

---

## 📚 Essential Reading for New AI Assistants

### **Must Read First**
1. `agentic-framework/master-agent.md` - Central coordination patterns
2. `telco-domain/project-brief.md` - Project scope and objectives
3. `agentic-framework/standards/coding_styleguide.md` - Code standards

### **Architecture Understanding**
1. `src/models/multi_provider_manager.py` - Multi-LLM orchestration
2. `src/ui/streamlit_demo.py` - User interface and interaction patterns
3. `src/models/rules_engine.py` - High-speed routing logic

### **Domain Knowledge**
1. `telco-domain/business-rules/` - Telecommunications industry specifics
2. `data/telecoms_tickets_*.csv` - Real-world ticket examples
3. `docs/` - Additional documentation and tutorials

---

## ⚡ Quick Reference Commands

```bash
# Launch main demo
python launch_demo.py

# Run tests
python -m pytest tests/

# Check system health
python validate_setup.py

# Update dependencies
pip install -r requirements.txt

# Generate test data
python test_data_generator.py

# Performance testing
python test_enhanced_routing_intelligence.py
```

---

## 🤝 Collaboration Guidelines

### **For GitHub Copilot Users**
- Reference agent personas with `#file:agentic-framework/sub-agents/[agent].md`
- Use `@workspace` for multi-file context awareness
- Follow established patterns in existing codebase

### **For Tabnine Users** (Primary Preference)
- Leverage universal framework structure for consistent suggestions
- Use YAML metadata in agent files for better context
- Follow coding standards for optimal code completion

### **For All AI Tools**
- **Universal Approach**: Use framework standards that work across all tools
- **Vendor Independence**: Never lock solutions to specific AI assistant
- **Context Preservation**: Always reference project structure and agent personas

---

## 📞 Support & Resources

### **Documentation Locations**
- **Technical Docs**: `docs/` directory
- **API Reference**: `docs/api/` (when available)
- **Tutorials**: `docs/tutorial/` 

### **Key Contact Points**
- **Project Owner**: LinoGoncalves (GitHub)
- **Repository**: https://github.com/LinoGoncalves/call-centre-agent
- **Issues**: Use GitHub Issues for bug reports and feature requests

---

**Remember**: This project emphasizes universal AI tool compatibility. Always consider how your changes will work across different AI assistants (Tabnine, Copilot, Cursor, Codeium, etc.) and maintain the vendor-neutral approach that makes this system accessible to all developers regardless of their preferred AI coding assistant.

---

*Last Updated: October 10, 2025*  
*Version: 2.0*  
*AI Compatibility: Universal (Tabnine, Copilot, Cursor, Codeium, JetBrains AI)*