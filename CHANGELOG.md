# Changelog

All notable changes to the Enhanced Telco Call Centre Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Universal Agentic AI Framework with 22+ specialized agents
- Master agent orchestration system
- Comprehensive development standards (27 files)
- Multi-tool AI compatibility (Tabnine, Copilot, Cursor, Codeium, JetBrains AI)
- Human-in-the-loop oversight modes (stepwise, autonomous, hybrid)
- Project context tracking for AI continuity
- Autonomous cognitive trigger system
- Documentation reorganization and archive structure

### Changed
- Updated telco-call-centre/README.md with comprehensive framework documentation
- Moved historical planning docs to docs/archive/
- Enhanced project documentation structure

## [1.2.0] - 2025-10-01

### Added
- Google Gemini LLM integration
- AI reasoning explanations for classifications
- Ensemble weight control (0-100% LLM vs Traditional ML)
- OTHER category for edge cases requiring human review
- HTML sanitization for secure output rendering
- Multi-layer defense security architecture

### Changed
- Improved UI accessibility and contrast ratios
- Enhanced Streamlit demo interface
- Updated classification confidence thresholds

### Fixed
- HTML injection vulnerabilities in LLM responses
- Output sanitization for production safety

## [1.1.0] - 2024-Q4

### Added
- FastAPI backend with <400ms response time
- Departmental routing logic
- Comprehensive test suite

### Changed
- Optimized classification pipeline
- Enhanced model accuracy to 99.15%

## [1.0.0] - 2024-Q3

### Added
- Initial release
- Traditional ML classification (6 categories)
- Streamlit demo interface
- Basic API endpoints
- Training pipeline
- Model persistence

### Core Features
- BILLING, TECHNICAL, SALES, COMPLAINTS, NETWORK, ACCOUNT categories
- South African telecom context
- Model training and evaluation scripts

---

## Version History Summary

- **v1.2.0**: LLM Integration & AI Reasoning
- **v1.1.0**: FastAPI Backend & Production Features
- **v1.0.0**: Initial ML Classification System

## Future Roadmap

See [project-context.md](telco-call-centre/project-context.md) for current development status and upcoming features.
