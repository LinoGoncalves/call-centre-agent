# Contributing to Call Centre Agent

## Welcome!

We appreciate your interest in contributing to the Enhanced Telco Call Centre Agent project. This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature/fix
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/LinoGoncalves/call-centre-agent.git
cd call-centre-agent

# Set up environment
python setup_env.py

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## Code Standards

Please follow the development standards in `telco-call-centre/development-standards/`:

- **Coding Style**: See `coding_styleguide.md`
- **API Design**: See `api_design_patterns.md`
- **Security**: See `secure_coding_checklist.md`
- **Testing**: See `testing_strategy.md`

## Pull Request Process

1. **Branch Naming**: Use descriptive names (e.g., `feature/llm-integration`, `fix/classification-bug`)
2. **Commit Messages**: Follow conventional commits format
3. **Tests**: Add/update tests for your changes
4. **Documentation**: Update relevant documentation
5. **Standards Compliance**: Ensure all linters pass

## Agent Framework Contributions

When contributing to the agentic framework:

- Follow the YAML metadata schema in agent files
- Maintain universal AI tool compatibility
- Document any new agent specializations
- Update `master-agent.md` for orchestration changes

## Reporting Issues

Use GitHub Issues to report bugs or request features. Include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Follow the code of conduct
- Help others in discussions

## Questions?

For questions or discussions, please open an issue or reach out to the maintainers.

---

Thank you for contributing to the Call Centre Agent project!
