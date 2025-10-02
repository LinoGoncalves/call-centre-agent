# Project Structure Guide

**Purpose**: Comprehensive walkthrough of the call-centre-agent project organization  
**Audience**: Developers joining the project or learning the codebase architecture

---

## Project Root Structure

```
call-centre-agent/
├── .github/                    # GitHub configuration and workflows
├── agentic-framework/          # Universal AI agent framework (reusable)
├── telco-domain/               # Telco-specific project context
├── src/                        # Main application source code
├── tests/                      # Test suite (unit + integration)
├── docs/                       # Documentation and tutorials
├── data/                       # Sample data and datasets
├── models/                     # Trained ML models (pickled)
├── notebooks/                  # Jupyter notebooks for exploration
├── scripts/                    # Utility scripts
├── legacy/                     # Deprecated code (kept for reference)
├── .env                        # Environment variables (API keys)
├── .env.example                # Environment template
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Multi-container orchestration
├── pyproject.toml              # Python project configuration
├── README.md                   # Project overview
├── CONTRIBUTING.md             # Contribution guidelines
└── CHANGELOG.md                # Version history
```

---

## Core Directories Explained

### `src/` - Application Source Code

**Purpose**: Main application logic, organized by functional layers

```
src/
├── models/                     # ML models and classification logic
│   ├── __init__.py
│   ├── enhanced_classifier.py  # Main classifier (983 lines)
│   ├── traditional_classifier.py
│   └── model_utils.py
│
├── ui/                         # User interfaces
│   ├── __init__.py
│   └── streamlit_demo.py       # Web demo (983 lines)
│
├── api/                        # REST API (future)
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   └── routes/
│
├── data/                       # Data processing utilities
│   ├── __init__.py
│   ├── preprocessing.py
│   └── feature_extraction.py
│
└── utils/                      # Shared utilities
    ├── __init__.py
    ├── logging_config.py
    └── validators.py
```

**Key Files:**

**`src/models/enhanced_classifier.py`** (983 lines):
- `GeminiEnhancedClassifier` class - main AI classification engine
- Integrates Google Gemini LLM with traditional ML
- Handles sentiment analysis, departmental routing, dispute detection
- **Critical Path**: All classification requests flow through this file

**`src/ui/streamlit_demo.py`** (983 lines):
- Production Streamlit web interface
- Real-time classification with visualizations
- HTML sanitization (6-layer security pipeline)
- Session state management for stateful interactions

---

### `tests/` - Test Suite

**Purpose**: Automated testing for quality assurance

```
tests/
├── __init__.py
├── conftest.py                      # pytest configuration and fixtures
├── test_enhanced_classifier.py      # Integration tests (210 lines)
├── test_departmental_routing.py     # Business logic tests (125 lines)
├── test_html_cleaning.py            # Security tests (69 lines)
└── fixtures/                        # Test data
    ├── sample_tickets.json
    └── mock_responses.py
```

**Test Organization:**
- **Integration tests**: Full end-to-end classification workflows
- **Unit tests**: Individual component validation
- **Security tests**: HTML sanitization, XSS prevention

**Run Tests:**
```bash
pytest tests/ -v                     # All tests
pytest tests/test_enhanced_classifier.py  # Specific file
pytest --cov=src --cov-report=html   # With coverage
```

---

### `agentic-framework/` - Universal AI Agent Framework

**Purpose**: Reusable multi-agent AI framework (tool-agnostic)

```
agentic-framework/
├── master-agent.md                  # Orchestration patterns
├── agent-roster.json                # Complete agent mapping
├── sub-agents/                      # 32+ specialized agent personas
│   ├── __init__.py
│   ├── business-analyst-agent.md
│   ├── solutions-architect-agent.md
│   ├── software-developer-agent.md
│   ├── data-scientist-agent.md
│   ├── devops-engineer-agent.md
│   ├── QA-engineer-agent.md
│   └── ... (28 more agents)
├── standards/                       # Universal coding guidelines
│   ├── coding_styleguide.md
│   ├── api_design_patterns.md
│   ├── testing_strategy.md
│   ├── secure_coding_checklist.md
│   └── ... (15 standards documents)
└── templates/                       # Reusable project templates
    ├── project-brief-template.md
    ├── quality-gates.md
    └── workflow-state-management.md
```

**Design Pattern**: Master-Agent Orchestration
- **Master Agent**: Coordinates complex multi-disciplinary tasks
- **Sub-Agents**: Specialized expertise (BA, Architect, Developer, QA, etc.)
- **HITL (Human-in-the-Loop)**: Human oversight at decision points

**Usage Example:**
```
@workspace Using #file:agentic-framework/master-agent.md, coordinate these agents:
- business-analyst-agent for requirements
- solutions-architect-agent for system design
- software-developer-agent for implementation
```

---

### `telco-domain/` - Telco-Specific Context

**Purpose**: Domain-specific business rules and project documentation

```
telco-domain/
├── project-brief.md              # Original requirements and scope
├── project-context.md            # Session logs and continuity
├── business-rules/               # Telco business logic
│   ├── billing_rules.md
│   ├── dispute_resolution.md
│   └── sla_policies.md
└── standards/                    # Telco-specific standards
    ├── network_security_policy.md
    └── compliance_requirements.md
```

**Key Distinction:**
- `agentic-framework/` = **Universal** (any project can use)
- `telco-domain/` = **Specific** (only this telco project)

---

### `docs/` - Documentation

**Purpose**: Tutorials, guides, and technical documentation

```
docs/
├── COMPREHENSIVE_BUILD_TUTORIAL.md  # Main tutorial (Phases 1-2)
└── tutorial/
    ├── README.md                    # Tutorial index
    ├── PHASE_3_GEMINI_INTEGRATION.md
    ├── PHASE_4_STREAMLIT_UI.md
    ├── PHASE_5_TESTING_VALIDATION.md
    ├── PHASE_6_PRODUCTION_DEPLOYMENT.md
    └── SQL_TO_PYTHON_QUICK_REFERENCE.md
```

**Tutorial Series**: 6-phase learning path (20-30 hours total)

---

### `models/` - Trained ML Models

**Purpose**: Serialized model artifacts

```
models/
├── telco_ticket_classifier.pkl   # Traditional ML model
├── vectorizer.pkl                 # TF-IDF vectorizer
└── label_encoder.pkl              # Category encoder
```

**Note**: Models are binary files (pickle format), not checked into git by default (`.gitignore` includes `*.pkl`)

**Loading Models:**
```python
import joblib

model = joblib.load('models/telco_ticket_classifier.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')
```

---

### `data/` - Datasets

**Purpose**: Sample data for training and testing

```
data/
├── telco_tickets.csv             # Original training data
├── validation_set.csv            # Labeled validation data
└── synthetic_tickets.json        # Generated test data
```

**Data Format** (CSV):
```csv
ticket_id,ticket_text,category,sentiment
1001,"My bill is too high",BILLING,NEGATIVE
1002,"Internet not working",TECHNICAL,CRITICAL
```

---

## Configuration Files

### `pyproject.toml` - Python Project Configuration

**Purpose**: Defines project metadata, dependencies, and tool settings

```toml
[project]
name = "call-centre-agent"
version = "1.0.0"
dependencies = [
    "streamlit>=1.30.0",
    "google-generativeai>=0.3.0",
    "scikit-learn>=1.3.0",
    "pandas>=2.0.0",
    "beautifulsoup4>=4.12.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 120
target-version = "py311"
```

**Install Dependencies:**
```bash
pip install -e .              # Install package in editable mode
pip install -e .[dev]         # Install with dev dependencies
```

---

### `.env` - Environment Variables

**Purpose**: Store sensitive configuration (API keys, secrets)

**Format:**
```bash
GOOGLE_API_KEY=AIzaSyC...your_key_here
LOG_LEVEL=info
MODEL_PATH=models/telco_ticket_classifier.pkl
```

**Security:**
- `.env` is in `.gitignore` (never commit secrets)
- `.env.example` shows required variables (without values)
- Cloud deployments use secrets managers (Azure Key Vault, AWS Secrets Manager)

---

### `Dockerfile` - Container Definition

**Purpose**: Defines production Docker image

**Key Elements:**
- Base image: `python:3.13-slim` (150MB, production-optimized)
- Non-root user: Security best practice
- Layer caching: Dependencies installed before code copy
- Health check: `/health` endpoint validation

**Build:**
```bash
docker build -t ticket-classifier:v1.0 .
docker run -p 8000:8000 --env-file .env ticket-classifier:v1.0
```

---

### `docker-compose.yml` - Multi-Container Orchestration

**Purpose**: Define multi-service stack for local development

**Services:**
1. **ticket-classifier-api**: Main application
2. **redis-cache**: Response caching
3. **prometheus**: Metrics collection (optional)

**Run Stack:**
```bash
docker-compose up -d          # Start all services
docker-compose logs -f api    # Follow API logs
docker-compose down           # Stop all services
```

---

## File Naming Conventions

### Python Modules

**Pattern**: `snake_case.py`

- ✅ `enhanced_classifier.py`
- ✅ `test_departmental_routing.py`
- ❌ `EnhancedClassifier.py` (wrong - not PascalCase)
- ❌ `enhanced-classifier.py` (wrong - use underscores)

### Markdown Documents

**Pattern**: `TITLE_IN_CAPS.md` or `descriptive-name.md`

- ✅ `README.md` (standard convention)
- ✅ `PHASE_4_STREAMLIT_UI.md` (tutorial)
- ✅ `project-brief.md` (descriptive)
- ❌ `Readme.MD` (wrong - inconsistent case)

### Agent Files

**Pattern**: `role-name-agent.md`

- ✅ `software-developer-agent.md`
- ✅ `solutions-architect-agent.md`
- ❌ `SoftwareDeveloperAgent.md` (wrong - use kebab-case)

---

## Module Dependencies

### Import Hierarchy

```
src/models/enhanced_classifier.py
    ↓ imports
google.generativeai           # External: Gemini API
sklearn.ensemble              # External: ML models
pandas                        # External: Data processing
    ↓ used by
src/ui/streamlit_demo.py
    ↓ imports
streamlit                     # External: Web framework
plotly                        # External: Visualizations
src.models.enhanced_classifier # Internal: Classification logic
```

**Principle**: UI layer depends on models layer, not vice versa (clean architecture)

---

## Architectural Decisions

### 1. Why Separate `agentic-framework/` from `telco-domain/`?

**Decision**: Framework is universal, domain is specific

**Rationale:**
- Framework can be reused in other projects (e-commerce, healthcare, etc.)
- Domain knowledge stays isolated
- Standards/agents are tool-agnostic (works with GitHub Copilot, Tabnine, Cursor, etc.)

### 2. Why `src/` Instead of Flat Root?

**Decision**: Organize code in `src/` directory

**Rationale:**
- Clear separation: source code vs tests vs docs
- Prevents test discovery conflicts
- Standard Python project structure
- Easier to package and distribute

### 3. Why Both `Dockerfile` and `docker-compose.yml`?

**Decision**: Dockerfile for single container, docker-compose for multi-service

**Rationale:**
- **Dockerfile**: Production deployment (Kubernetes, ECS)
- **docker-compose**: Local development (API + Redis + Prometheus stack)
- Different use cases, complementary tools

### 4. Why `models/` Directory for Pickled Files?

**Decision**: Separate directory for model artifacts

**Rationale:**
- Large binary files (10-100MB+)
- Not version-controlled (in `.gitignore`)
- Loaded at runtime, not import time
- Can be swapped without code changes

---

## Navigation Tips

### Finding Code for a Feature

**Want to understand classification?**
→ Start with `src/models/enhanced_classifier.py`

**Want to modify the UI?**
→ Edit `src/ui/streamlit_demo.py`

**Want to add tests?**
→ Add file in `tests/` directory

**Want to learn the system?**
→ Start with `docs/COMPREHENSIVE_BUILD_TUTORIAL.md`

### Using Agents for Development

**Need architecture advice?**
```
@workspace Using #file:agentic-framework/sub-agents/solutions-architect-agent.md, 
design the API layer for this system
```

**Need code review?**
```
@workspace Using #file:agentic-framework/sub-agents/QA-engineer-agent.md,
review src/models/enhanced_classifier.py for potential issues
```

---

## Key Takeaways

1. **`src/`**: Main application code (models, UI, API)
2. **`tests/`**: Automated test suite (pytest)
3. **`agentic-framework/`**: Universal AI agent framework (reusable)
4. **`telco-domain/`**: Telco-specific business rules
5. **`docs/`**: Tutorials and documentation
6. **`models/`**: Trained ML models (binary files)
7. **`data/`**: Training and validation datasets
8. **Naming conventions**: `snake_case.py`, `kebab-case.md`, `CAPS.md`
9. **Configuration**: `pyproject.toml`, `.env`, `Dockerfile`, `docker-compose.yml`
10. **Architectural principle**: Clean separation of concerns (UI → Models → Data)

Understanding project structure is the first step to effective development. This organization supports scalability, maintainability, and team collaboration.
