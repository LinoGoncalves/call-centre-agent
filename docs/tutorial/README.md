# 📚 Call Centre AI Agent - Complete Tutorial Series

## 🎯 Tutorial Overview

This comprehensive tutorial series teaches you how to build a production-ready AI-powered call centre ticket classification system from the ground up.

**Perfect for**: IT professionals with SQL expertise transitioning to Python/ML/AI

---

## 👤 Learner Profile

**You are**:
- ✅ IT professional with 15+ years experience
- ✅ Very strong SQL skills
- ✅ Working in Telco industry (billing support focus)
- ✅ Python beginner
- ✅ Basic ML/AI knowledge

**You will become**:
- 🎓 Confident Python developer for ML applications
- 🎓 Capable of building and maintaining AI systems
- 🎓 Skilled in LLM integration and prompt engineering
- 🎓 Able to make architectural decisions for ML projects
- 🎓 Ready to extend and customize the system

---

## 📖 Tutorial Structure

### 🗺️ Learning Path

```
Phase 1: Foundation (4 hrs)
   ↓  Learn: Data handling, SQL→Python translation
   ↓
Phase 2: Traditional ML (6 hrs)
   ↓  Learn: Text classification, model training
   ↓
Phase 3: LLM Integration (4 hrs)
   ↓  Learn: Gemini API, prompt engineering, ensemble
   ↓
Phase 4: User Interface (3 hrs)
   ↓  Learn: Streamlit, web apps, visualization
   ↓
Phase 5: Testing (3 hrs)
   ↓  Learn: Unit tests, integration tests, validation
   ↓
Phase 6: Production (4 hrs)
   ↓  Learn: Deployment, monitoring, maintenance
   ↓
Master: Full System
```

**Total Time**: 20-30 hours over 2-3 weeks

---

## 📚 Tutorial Modules

### **Main Tutorial** (Start Here)
📄 [COMPREHENSIVE_BUILD_TUTORIAL.md](./COMPREHENSIVE_BUILD_TUTORIAL.md)
- Complete overview and Phases 1-2
- Environment setup
- Traditional ML classifier
- Estimated time: 10 hours

### **Phase 3: LLM Integration**
📄 [PHASE_3_GEMINI_INTEGRATION.md](./tutorial/PHASE_3_GEMINI_INTEGRATION.md)
- Google Gemini API integration
- Prompt engineering techniques
- Ensemble prediction logic
- Estimated time: 4-6 hours

### **Phase 4: User Interface** (Coming Next)
📄 [PHASE_4_STREAMLIT_UI.md](./tutorial/PHASE_4_STREAMLIT_UI.md)
- Interactive web application
- Real-time classification demo
- Visualization and insights
- Estimated time: 3-4 hours

### **Phase 5: Testing & Validation** (Coming Next)
📄 [PHASE_5_TESTING.md](./tutorial/PHASE_5_TESTING.md)
- Unit testing strategies
- Integration testing
- Performance validation
- Estimated time: 3-4 hours

### **Phase 6: Production Deployment** (Coming Next)
📄 [PHASE_6_PRODUCTION.md](./tutorial/PHASE_6_PRODUCTION.md)
- Deployment strategies
- Monitoring and logging
- Maintenance and updates
- Estimated time: 4-5 hours

---

## 🎓 Learning Approach

### **Hands-On Philosophy**

Every tutorial follows this pattern:

1. **Concept Explanation** - Why we're building this
2. **SQL Analogy** - Connect to your existing knowledge
3. **Step-by-Step Code** - Build it yourself
4. **Checkpoint** - Verify understanding
5. **Troubleshooting** - Common issues and solutions

### **Progressive Complexity**

```
Simple → Intermediate → Advanced
  ↓          ↓             ↓
Basic    Traditional    Production
Python      ML+LLM       Deployment
```

### **Real-World Focus**

- ✅ Production-ready code (not toy examples)
- ✅ Error handling and fallbacks
- ✅ Telco industry context
- ✅ Maintainability and extensibility

---

## 🛠️ Prerequisites

### **Before You Start**

1. **Install Required Software**:
   - Python 3.11+
   - Git
   - VS Code (recommended)

2. **Get API Keys**:
   - Google Gemini API key (free tier)

3. **Set Up Environment**:
   - Follow Phase 1 setup instructions
   - Create virtual environment
   - Install dependencies

4. **Clone Reference Project** (Optional):
   ```powershell
   git clone https://github.com/LinoGoncalves/call-centre-agent.git
   cd call-centre-agent
   ```

---

## 📊 What You'll Build

### **System Architecture**

```
┌─────────────────────────────────────────────────────────┐
│              Streamlit Web Interface                     │
│  • Input tickets                                         │
│  • View classifications                                  │
│  • See AI reasoning                                      │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│           Enhanced Classifier (Orchestrator)             │
│  • Routes to appropriate model                           │
│  • Combines predictions                                  │
│  • Manages fallbacks                                     │
└──────┬───────────────────────────────────────┬──────────┘
       ↓                                       ↓
┌──────────────────┐                 ┌─────────────────────┐
│ Traditional ML   │                 │   Gemini LLM AI     │
│ (Scikit-learn)   │                 │  (Google Gemini)    │
│                  │                 │                     │
│ • Fast (ms)      │                 │ • Intelligent       │
│ • Offline work   │                 │ • Deep reasoning    │
│ • Baseline       │                 │ • Explanations      │
└──────────────────┘                 └─────────────────────┘
```

### **Key Features**

✅ **Multi-label Classification**
- Department routing (5 categories)
- Sentiment analysis (3 levels)
- Urgency assessment (4 levels)

✅ **Hybrid Intelligence**
- Traditional ML for speed
- LLM for complex cases
- Ensemble for best results

✅ **Production Ready**
- Error handling
- API rate limiting
- Offline fallbacks
- Comprehensive logging

✅ **User-Friendly Interface**
- Real-time classification
- AI reasoning display
- Confidence indicators
- Department insights

---

## 🎯 Learning Outcomes

### **Technical Skills**

By the end, you will be able to:

✅ **Python Development**
- Write clean, maintainable Python code
- Use modern Python project structure
- Understand object-oriented programming
- Work with virtual environments and dependencies

✅ **Machine Learning**
- Train text classification models
- Evaluate model performance
- Understand ML pipelines
- Save and load trained models

✅ **LLM Integration**
- Use Google Gemini API
- Design effective prompts
- Parse and validate LLM responses
- Handle API errors and rate limits

✅ **System Design**
- Architect hybrid ML+LLM systems
- Implement ensemble logic
- Design fallback strategies
- Structure modular codebases

✅ **Testing & Validation**
- Write unit tests for ML code
- Validate model performance
- Test API integrations
- Debug classification issues

✅ **Deployment**
- Package Python applications
- Deploy web applications
- Monitor system performance
- Maintain production ML systems

### **Domain Knowledge**

You will understand:

✅ Telco call centre operations and routing
✅ Customer sentiment analysis techniques
✅ Urgency assessment criteria
✅ AI-assisted decision making
✅ Audit trail and explainability requirements

---

## 📈 Progress Tracking

### **Checkpoint System**

Each phase includes checkpoints to verify your progress:

- **Phase 1**: ☐ Can load and query data with pandas
- **Phase 2**: ☐ Can train and evaluate ML models
- **Phase 3**: ☐ Can integrate LLM APIs successfully
- **Phase 4**: ☐ Can build interactive web UIs
- **Phase 5**: ☐ Can write and run automated tests
- **Phase 6**: ☐ Can deploy to production environment

### **Validation Exercises**

Each phase includes exercises to test understanding:

1. **Conceptual Questions** - Test your understanding
2. **Coding Challenges** - Apply what you learned
3. **Troubleshooting Scenarios** - Debug common issues
4. **Extension Projects** - Go beyond the tutorial

---

## 🆘 Getting Help

### **Resources**

📚 **Documentation**
- [Python Official Docs](https://docs.python.org/3/)
- [Scikit-learn Tutorials](https://scikit-learn.org/stable/tutorial/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Streamlit Docs](https://docs.streamlit.io/)

🔍 **SQL → Python Translation**
- [Pandas SQL Comparison](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html)
- Built-in SQL analogies throughout tutorial

💬 **Community Support**
- Stack Overflow (tag: python, machine-learning)
- Reddit r/learnpython and r/MachineLearning
- Python Discord communities

### **Troubleshooting Guide**

Common issues and solutions are documented in each phase. If stuck:

1. Check the **Troubleshooting** section in that phase
2. Review the **Checkpoint** - did you complete all steps?
3. Check the **Common Issues** list
4. Refer to the **reference implementation** in the repo

---

## 🚀 Getting Started

### **Quick Start (30 Minutes)**

1. **Read**: [COMPREHENSIVE_BUILD_TUTORIAL.md](./COMPREHENSIVE_BUILD_TUTORIAL.md) - Section 1 & 2
2. **Install**: Python, Git, VS Code
3. **Setup**: Virtual environment and dependencies
4. **Test**: Run `scripts/explore_data.py`

### **First Milestone (Day 1)**

Complete **Phase 1: Foundation**
- Understand the project architecture
- Set up development environment
- Load and explore training data
- Run your first pandas queries

### **Recommended Schedule**

**Week 1**: Phases 1-2 (Foundation + Traditional ML)
- Days 1-2: Environment setup, data exploration
- Days 3-5: Build traditional classifier
- Weekend: Review and practice

**Week 2**: Phases 3-4 (LLM + UI)
- Days 1-3: Gemini integration
- Days 4-5: Streamlit interface
- Weekend: Testing and refinement

**Week 3**: Phases 5-6 (Testing + Production)
- Days 1-2: Write tests
- Days 3-4: Deployment preparation
- Day 5: Final review and documentation

---

## 🎓 Beyond the Tutorial

### **Extension Projects**

Once you complete the tutorial, try these:

1. **Add New Features**
   - Multi-language support
   - Historical trend analysis
   - Automated ticket responses
   - Performance dashboards

2. **Improve ML Models**
   - Fine-tune Gemini with examples
   - Try other LLMs (Claude, GPT-4)
   - Implement active learning
   - Add confidence calibration

3. **Scale the System**
   - Add database backend (PostgreSQL)
   - Implement API endpoints (FastAPI)
   - Add authentication/authorization
   - Deploy to cloud (Azure, AWS, GCP)

4. **Apply to Your Domain**
   - Customize for your company's tickets
   - Add domain-specific routing rules
   - Integrate with existing systems
   - Train on your historical data

---

## 📝 Tutorial Philosophy

### **Teaching Approach**

This tutorial series follows the Agentic AI Framework principles:

1. **Human-AI Collaboration**: You're learning to work *with* AI, not be replaced by it
2. **Progressive Enhancement**: Start simple, add complexity gradually
3. **Real-World Context**: Every example rooted in actual Telco scenarios
4. **SQL-First Mindset**: Leverage your SQL expertise to understand Python/ML
5. **Production Quality**: Learn best practices from day one

### **Learning Methodology**

- **Explain Why**: Understand the reasoning behind design decisions
- **Show How**: Step-by-step implementation with code
- **Practice**: Hands-on exercises at every checkpoint
- **Validate**: Test your understanding before moving forward
- **Extend**: Challenge yourself with additional projects

---

## 🌟 Success Criteria

You'll know you've succeeded when you can:

✅ Explain the system architecture to a colleague
✅ Modify and extend the code confidently
✅ Debug issues independently
✅ Train models on new data
✅ Deploy updates to production
✅ Make informed ML/AI technology decisions

**Most importantly**: You'll have a production-ready system you built and understand completely!

---

## 🙏 Acknowledgments

This tutorial was created by the **Agentic AI Framework** team:

- **Master Orchestrator Agent**: Overall coordination and learning path design
- **Technical Writer Agent**: Tutorial structure and documentation
- **Solutions Architect Agent**: System design and architecture explanations
- **Data Scientist Agent**: ML/AI concepts and beginner-friendly explanations
- **Software Developer Agent**: Code examples and implementation details
- **QA Engineer Agent**: Testing exercises and validation checkpoints

Built with ❤️ for IT professionals transitioning to AI/ML development.

---

**Ready to start?** → [Begin with the Main Tutorial](./COMPREHENSIVE_BUILD_TUTORIAL.md)

**Questions?** → Check the troubleshooting sections or refer to the reference implementation

**Feedback?** → Your learnings help improve future tutorials!

---

*Tutorial Series Index - Version 1.0 - October 2025*
*Part of the Agentic AI Framework Educational Resources*
