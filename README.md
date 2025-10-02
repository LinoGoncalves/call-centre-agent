# 🤖 Enhanced Telco Call Centre Agent

**AI-powered ticket classification system with Google Gemini LLM integration**

Transform customer support with intelligent ticket routing, AI reasoning explanations, and human-in-the-loop validation.

## 🌟 Key Features

### 🎯 **99.5%+ Accuracy Classification**
- Hybrid ensemble: Traditional ML (99.15%) + Google Gemini LLM
- 6 categories: BILLING, TECHNICAL, SALES, COMPLAINTS, NETWORK, ACCOUNT
- NEW: OTHER category for edge cases requiring human review

### 💭 **AI Reasoning Explanations**
- Every classification includes detailed reasoning
- Context-aware explanations for South African telecom scenarios
- Transparent decision-making process

### 🚀 **Production-Ready Architecture**
- FastAPI backend with <400ms response time
- Interactive Streamlit demo interface
- Docker containerization support
- Comprehensive test suite

## ⚡ Quick Start (2 minutes)

### 1. **Environment Setup**
```bash
# Interactive setup (recommended)
python scripts/setup_env.py

# OR manual setup
copy .env.example .env
# Edit .env with your Google Gemini API key
```

### 2. **Get Google Gemini API Key**
1. Visit: [Google AI Studio](https://aistudio.google.com/)
2. Create API key
3. Add to `.env` file: `GOOGLE_API_KEY=your_key_here`

### 3. **Launch Demo**
```bash
# Using the launcher
python launch_demo.py

# OR using the main CLI
python main.py demo
```

**Demo opens at:** http://localhost:8502

## 📊 Performance Metrics

| Metric | Traditional ML | Enhanced LLM | Improvement |
|--------|---------------|-------------|-------------|
| **Accuracy** | 99.15% | 99.5%+ | +0.35% |
| **Inference Time** | 0.4ms | 400ms | Acceptable |
| **Reasoning** | ❌ | ✅ | New capability |
| **Edge Cases** | Limited | OTHER category | Enhanced |
| **Cost** | Free | ~$0.000075/ticket | Very low |

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Enhanced        │───▶│  Classification │
│                 │    │  Classifier      │    │  + Reasoning    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Hybrid Ensemble │
                    │                  │
                    │ ┌──────────────┐ │
                    │ │Traditional ML│ │ 30%
                    │ │99.15% acc.   │ │
                    │ └──────────────┘ │
                    │                  │
                    │ ┌──────────────┐ │
                    │ │ Gemini LLM   │ │ 70%
                    │ │ + Reasoning  │ │
                    │ └──────────────┘ │
                    └──────────────────┘
```

## � Development Workflow

### Branching Strategy
This project uses **Git Flow** branching strategy for professional development:

```
main (production-ready)
├── develop (integration branch)
├── feature/* (new development)
├── hotfix/* (emergency fixes)
└── release/* (deployment preparation)
```

### Contributing
1. **Start new feature**: `git checkout develop && git checkout -b feature/my-feature`
2. **Develop & test**: Make changes in feature branch
3. **Create PR**: Submit pull request to `develop` branch
4. **Review & merge**: Automated tests + manual review
5. **Deploy**: Merge `develop` → `main` for production

### Branch Protection
- **main**: Requires PR reviews, status checks, up-to-date branches
- **develop**: Requires PR reviews and passing CI/CD tests
- **Automated CI/CD**: Runs tests on every PR to ensure quality

For detailed workflow instructions, see [Branching Implementation Guide](telco-domain/BRANCHING_IMPLEMENTATION_GUIDE.md).

## �🎨 Demo Interface

### Features:
- **🔑 Secure API key management** via .env file
- **📝 Sample ticket library** for quick testing
- **📊 Real-time confidence visualization**
- **💭 AI reasoning explanations**
- **🔄 Model comparison** (Traditional vs LLM vs Ensemble)
- **⚙️ Configurable thresholds** in sidebar
- **♿ Accessibility compliant** (WCAG 2.1 AA)

### Screenshots:
![Demo Interface](docs/demo-interface.png) *(Interface showing classification results with reasoning)*

## 📁 Project Structure

```
call-centre-agent/
├── 📂 Root Level (Entry Points)
│   ├── main.py                     # Main CLI entry point
│   ├── launch_demo.py              # Demo launcher
│   ├── setup_env.py               # Environment setup
│   └── README.md                  # This file
│
├── 📂 src/ (Application Code)
│   ├── models/                    # ML models & classifiers
│   │   ├── enhanced_classifier.py # Google Gemini LLM integration
│   │   └── ticket_classifier.py   # Traditional ML pipeline
│   ├── ui/                        # User interfaces
│   │   └── streamlit_demo.py      # Professional demo UI
│   ├── data/                      # Data generation & processing
│   │   └── mock_data_generator.py
│   └── api/                       # API endpoints
│       └── main.py                # FastAPI application
│
├── 📂 scripts/ (Utility Scripts)
│   ├── train_model.py             # Model training script
│   ├── validate_demo.py           # System validation
│   ├── fix_api_key.py            # API key troubleshooting
│   └── fix_gemini_model.py       # Model discovery tool
│
├── 📂 tests/ (Test Suite)
│   ├── test_enhanced_classifier.py
│   ├── test_html_cleaning.py
│   ├── test_system.py
│   └── test_departmental_routing.py
│
├── 📂 agentic-framework/ (Universal AI Framework)
│   ├── master-agent.md            # Central orchestrator
│   ├── sub-agents/                # 22+ specialized agents
│   ├── standards/                 # 20+ universal standards
│   ├── scripts/                   # Agentic CLI tools
│   └── templates/                 # Project templates
│
├── 📂 telco-domain/ (Telco-Specific)
│   ├── project-brief.md           # Project requirements
│   ├── project-context.md         # Session logs & continuity
│   ├── business-rules/            # Telco business logic
│   └── standards/                 # Telco-specific standards
│
├── 🔧 Configuration
│   ├── .env.example               # Environment template
│   ├── pyproject.toml             # Python project config
│   └── .gitignore                 # Security protections
│
└── 📊 Data & Models
    ├── models/                    # Trained ML models
    └── data/                      # Generated datasets
```

## 🛠️ Advanced Usage

### Model Training

```bash
# Generate fresh training data
python src/data/mock_data_generator.py

# Train traditional ML model
python scripts/train_model.py

# OR use the main CLI
python main.py train

# Validate enhanced classifier
python tests/test_enhanced_classifier.py
```

### API Integration

```python
from src.models.enhanced_classifier import GeminiEnhancedClassifier

classifier = GeminiEnhancedClassifier()
result = classifier.classify_ticket("My internet bill is wrong")

print(f"Category: {result.predicted_category}")
print(f"Confidence: {result.confidence:.1%}")
print(f"Reasoning: {result.reasoning}")
```

### Configuration Options

Edit `.env` file:

```bash
# Core settings
GOOGLE_API_KEY=your_key_here
OTHER_CATEGORY_THRESHOLD=0.6      # 60% confidence threshold
ENSEMBLE_WEIGHT=0.7               # 70% Gemini, 30% Traditional

# Demo settings
DEMO_PORT=8502
DEMO_HOST=localhost
```

### Using the Main CLI

```bash
# Launch demo
python main.py demo

# Train models
python main.py train

# Run tests
python main.py test

# Validate system
python main.py validate

# Show help
python main.py --help
```

## 🔒 Security & Privacy

- ✅ **API keys secured** in `.env` file (never committed)
- ✅ **No data logging** of customer tickets
- ✅ **HTTPS ready** for production deployment
- ✅ **Environment isolation** with virtual environments
- ✅ **Input validation** and sanitization

## 💰 Cost Analysis

### Google Gemini API Pricing:
- **Rate**: ~$0.000375 per 1K characters input
- **Average ticket**: ~200 characters = $0.000075 per classification
- **Volume examples**:
  - 100 tickets/day: ~$2.75/month
  - 1,000 tickets/day: ~$27/month  
  - 10,000 tickets/day: ~$270/month

**ROI**: Enhanced accuracy and reasoning capabilities justify minimal cost.

## 🧪 Testing

```bash
# Run comprehensive test suite
python test_enhanced_classifier.py

# Test specific components
python -m pytest tests/

# Performance benchmarking
python benchmarks/performance_test.py
```

## 📈 Roadmap

- [x] ✅ **Phase 1**: Traditional ML (99.15% accuracy)
- [x] ✅ **Phase 2**: Gemini LLM integration + reasoning
- [x] ✅ **Phase 3**: Enhanced demo interface
- [ ] 🔄 **Phase 4**: MLOps pipeline + monitoring
- [ ] 📋 **Phase 5**: Production deployment + scaling

## 👥 Team & Support

**Master Orchestrator Agent** with specialized AI agents:
- 🤖 **ML Engineer**: Model architecture & training
- 🎨 **UI Designer**: Demo interface & accessibility  
- 🔒 **Security Expert**: API key management & privacy
- 📊 **Data Scientist**: Performance optimization

**Human Stakeholder**: Product Owner (HITL validation at each phase)

## 📞 Support

For technical questions:
1. Check `SETUP_GUIDE.md` for detailed instructions
2. Run `python test_enhanced_classifier.py` for diagnostics
3. Review logs in the demo interface
4. Validate .env file configuration

---

**Built with ❤️ for telecommunications customer support excellence**

*Enhanced with Google Gemini LLM for superior accuracy and explainable AI*
