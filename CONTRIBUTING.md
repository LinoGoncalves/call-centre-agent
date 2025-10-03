# Contributing to Call Centre Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the Call Centre AI Agent project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Agentic Framework Coordination](#agentic-framework-coordination)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:
- Be respectful and professional in all interactions
- Provide constructive feedback
- Focus on the technical merits of contributions
- Respect differing viewpoints and experiences

---

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git
- VS Code (recommended) or your preferred IDE
- Google Gemini API key (for LLM features)

### Initial Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/call-centre-agent.git
   cd call-centre-agent
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Verify Setup**
   ```bash
   # Run tests
   pytest -q
   
   # Launch demo
   python launch_demo.py
   ```

---

## Development Workflow

### Branching Strategy

We use a modified Git Flow:

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features (e.g., `feature/vector-db-integration`)
- `bugfix/*`: Bug fixes (e.g., `bugfix/sanitization-regex`)
- `epic/*`: Major epics (e.g., `epic/mlops-pipeline`)

### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Build/tooling changes

**Examples**:
```
feat(vector-db): add Pinecone integration for semantic search

Implements vector similarity search using Pinecone with top-k retrieval.
Includes caching layer and confidence-based routing logic.

Closes #2
```

```
fix(sanitization): improve PII detection for phone numbers

Extended regex pattern to handle international formats.
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specific guidelines:

1. **Type Hints**: Use type hints for all function signatures
   ```python
   def classify_ticket(ticket_text: str) -> ClassificationResult:
       ...
   ```

2. **Docstrings**: Use Google-style docstrings
   ```python
   def calculate_confidence(scores: list[float]) -> float:
       """Calculate ensemble confidence from multiple model scores.
       
       Args:
           scores: List of confidence scores from different models (0-1 range).
           
       Returns:
           Weighted average confidence score.
           
       Raises:
           ValueError: If scores list is empty or contains invalid values.
       """
       ...
   ```

3. **Code Formatting**: Use `black` for auto-formatting
   ```bash
   black src/ tests/
   ```

4. **Linting**: Use `ruff` for linting
   ```bash
   ruff check src/ tests/
   ```

5. **Import Organization**
   ```python
   # Standard library
   import os
   from typing import Optional
   
   # Third-party
   import pandas as pd
   from sklearn.pipeline import Pipeline
   
   # Local
   from src.models import EnhancedClassifier
   ```

### Standards Reference

Always reference project standards before implementing:
- **Coding Style**: `agentic-framework/standards/coding_styleguide.md`
- **API Design**: `agentic-framework/standards/api_design_patterns.md`
- **Security**: `agentic-framework/standards/secure_coding_checklist.md`
- **Testing**: `agentic-framework/standards/testing_strategy.md`

---

## Pull Request Process

### Before Opening a PR

1. **Run Tests Locally**
   ```bash
   pytest -v
   pytest --cov=src tests/  # With coverage
   ```

2. **Run Linting and Formatting**
   ```bash
   black src/ tests/
   ruff check src/ tests/
   ```

3. **Update Documentation**
   - Add/update docstrings
   - Update relevant markdown files in `docs/`
   - Update CHANGELOG.md

4. **Check for Errors**
   ```bash
   # No Python errors
   python -m py_compile src/**/*.py
   ```

### Opening a PR

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**
   - Use a descriptive title (follows commit convention)
   - Fill out the PR template completely
   - Link related issues (e.g., "Closes #2")
   - Add appropriate labels

3. **PR Template** (auto-populated):
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Related Issues
   Closes #
   
   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Integration tests added/updated
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] Tests pass locally
   - [ ] No new warnings introduced
   ```

### Code Review Process

**Review Timeline**:
- Initial review: Within 2 business days
- Follow-up reviews: Within 1 business day

**Reviewers**:
- Assign at least 1 reviewer (2 for critical changes)
- Reference appropriate agent experts (see Agentic Framework below)

**Review Criteria**:
- Code quality and readability
- Test coverage (aim for 80%+)
- Documentation completeness
- Security considerations
- Performance implications
- Alignment with project standards

**Approval Requirements**:
- 1 approval for minor changes (docs, tests, small fixes)
- 2 approvals for major changes (new features, refactors, API changes)
- Security team approval for security-sensitive changes

---

## Agentic Framework Coordination

This project uses an **agentic orchestration pattern** for coordinated development. Before making changes, consult the appropriate agent persona for guidance.

### Master Orchestrator

For high-level task planning and multi-agent coordination:
- **File**: `.github/chatmodes/agent-orchestrator.md`
- **Use When**: Complex features spanning multiple disciplines

**Example Prompt**:
```
@workspace Using .github/chatmodes/agent-orchestrator.md, coordinate agents for:
"Add vector DB integration with Pinecone and RAG-based LLM prompting"
```

### Sub-Agent Specializations

Reference these agents for domain-specific guidance:

#### Software Development
- **Agent**: `agentic-framework/sub-agents/software-developer-agent.md`
- **Responsibilities**: Code implementation, refactoring, debugging
- **Use For**: Python code changes, API development

#### Architecture & Design
- **Agent**: `agentic-framework/sub-agents/solutions-architect-agent.md`
- **Responsibilities**: System design, integration patterns
- **Use For**: New component design, cloud architecture decisions

#### Data Science & ML
- **Agent**: `agentic-framework/sub-agents/data-scientist-agent.md`
- **Responsibilities**: Model training, evaluation, feature engineering
- **Use For**: ML algorithm changes, model tuning, experimentation

#### Security
- **Agent**: `agentic-framework/sub-agents/security-expert-agent.md`
- **Responsibilities**: Security reviews, threat modeling, vulnerability assessment
- **Use For**: PII handling, API authentication, data sanitization

#### Testing & QA
- **Agent**: `agentic-framework/sub-agents/QA-engineer-agent.md`
- **Responsibilities**: Test strategy, quality assurance
- **Use For**: Test planning, coverage improvements, bug validation

#### DevOps & Cloud
- **Agent**: `agentic-framework/sub-agents/cloud-engineer-agent.md`
- **Responsibilities**: Infrastructure, CI/CD, deployment
- **Use For**: Kubernetes configs, Airflow pipelines, cloud resources

#### Documentation
- **Agent**: `agentic-framework/sub-agents/technical-writer-agent.md`
- **Responsibilities**: User guides, API docs, tutorials
- **Use For**: Documentation updates, tutorial creation

### Agent Coordination Example

For a feature like "Add vector DB search with confidence routing":

1. **Architect** designs the routing logic and vector DB schema
2. **Developer** implements the Python integration
3. **Data Scientist** defines similarity thresholds and confidence scoring
4. **Security Expert** reviews PII handling in embeddings
5. **QA Engineer** creates test plan for caching behavior
6. **DevOps** sets up Pinecone infrastructure in Azure
7. **Tech Writer** documents the new routing behavior

**Coordination Prompt**:
```
@workspace Acting as master orchestrator from .github/chatmodes/agent-orchestrator.md:
Coordinate solutions-architect, software-developer, data-scientist, security-expert,
QA-engineer, and cloud-engineer agents to implement vector DB integration.
```

### YAML Metadata Updates

When changing agent behavior, update YAML frontmatter:

```yaml
---
agent_type: specialist
specialization: software-developer
tools_compatible:
  - tabnine
  - copilot
  - cursor
context_scope: project-level
interaction_patterns:
  - request-response
  - task-decomposition
version: 0.2.0  # Increment on material changes
---
```

---

## Testing Guidelines

### Test Structure

```
tests/
├── unit/              # Unit tests (fast, isolated)
├── integration/       # Integration tests (DB, API)
├── e2e/              # End-to-end tests (full system)
└── conftest.py       # Shared fixtures
```

### Test Requirements

1. **Coverage**: Aim for 80% overall, 90% for critical paths
2. **Speed**: Unit tests <100ms, integration tests <5s
3. **Isolation**: Use mocks/fixtures for external dependencies
4. **Clarity**: Descriptive test names and clear assertions

### Example Test

```python
def test_vector_search_returns_top_k_results():
    """Test that vector search returns exactly k most similar tickets."""
    # Arrange
    vector_db = MockVectorDB()
    query_embedding = [0.1, 0.2, 0.3]
    k = 5
    
    # Act
    results = vector_db.search(query_embedding, top_k=k)
    
    # Assert
    assert len(results) == k
    assert all(r.score >= 0.0 and r.score <= 1.0 for r in results)
    assert results[0].score >= results[-1].score  # Descending order
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_vector_search.py

# Specific test function
pytest tests/unit/test_vector_search.py::test_vector_search_returns_top_k_results

# With coverage
pytest --cov=src --cov-report=html

# Fast tests only (skip integration/e2e)
pytest -m "not integration and not e2e"
```

### Mocking External Services

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_gemini_client():
    """Mock Gemini API client for testing."""
    mock = Mock()
    mock.generate_content.return_value.text = "Billing department"
    return mock

def test_llm_classification_with_mocked_api(mock_gemini_client):
    classifier = EnhancedClassifier(llm_client=mock_gemini_client)
    result = classifier.classify_ticket("Billing issue")
    assert result.department == "Billing"
```

---

## Documentation

### Documentation Standards

1. **Code Comments**: Explain *why*, not *what*
   ```python
   # Good
   # Use exponential backoff to avoid rate limits during high load
   time.sleep(2 ** retry_count)
   
   # Bad
   # Sleep for 2 to the power of retry_count
   time.sleep(2 ** retry_count)
   ```

2. **API Documentation**: Use docstrings + type hints
   ```python
   def search_similar_tickets(
       query: str,
       top_k: int = 5,
       filters: Optional[dict] = None
   ) -> list[SimilarTicket]:
       """Search for similar historical tickets using vector similarity.
       
       Args:
           query: The ticket text to search for.
           top_k: Number of results to return (default: 5).
           filters: Optional metadata filters (department, urgency, etc.).
           
       Returns:
           List of similar tickets sorted by similarity score (descending).
           
       Raises:
           ValueError: If top_k < 1 or > 100.
           VectorDBError: If vector database connection fails.
       """
   ```

3. **README Updates**: Update relevant README files when:
   - Adding new features
   - Changing setup process
   - Adding new dependencies
   - Modifying architecture

4. **Tutorial Updates**: If your change affects user workflows:
   - Update `docs/COMPREHENSIVE_BUILD_TUTORIAL.md`
   - Update relevant phase tutorials in `docs/tutorial/`
   - Add code examples where appropriate

### Documentation Checklist

- [ ] Docstrings for all public functions/classes
- [ ] Type hints for all function signatures
- [ ] README.md updated (if setup/usage changed)
- [ ] Tutorial updated (if user workflow changed)
- [ ] CHANGELOG.md entry added
- [ ] API documentation generated (if public API changed)

---

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Creating a Release

1. **Update CHANGELOG.md**
   ```markdown
   ## [1.2.0] - 2026-01-15
   
   ### Added
   - Vector DB integration with Pinecone
   - RAG-based LLM prompting
   
   ### Changed
   - Improved PII detection accuracy
   
   ### Fixed
   - Fixed HTML sanitization edge case
   ```

2. **Create Release Branch**
   ```bash
   git checkout develop
   git checkout -b release/v1.2.0
   ```

3. **Tag Release**
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

4. **Create GitHub Release**
   - Go to Releases → Draft New Release
   - Select tag `v1.2.0`
   - Add release notes from CHANGELOG.md
   - Attach build artifacts (if any)

---

## Getting Help

### Resources
- **Documentation**: `docs/` directory
- **Tutorials**: `docs/tutorial/`
- **Agentic Framework**: `agentic-framework/`
- **Issues**: [GitHub Issues](https://github.com/LinoGoncalves/call-centre-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/LinoGoncalves/call-centre-agent/discussions)

### Quick Links
- [Project Roadmap](ROADMAP.md)
- [Product Backlog](BACKLOG.md)
- [Phase 0: Agentic Framework](docs/tutorial/PHASE_0_AGENTIC_FRAMEWORK.md)
- [Coding Style Guide](agentic-framework/standards/coding_styleguide.md)
- [Security Checklist](agentic-framework/standards/secure_coding_checklist.md)

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

Thank you for contributing to the Call Centre AI Agent project! 🎉
