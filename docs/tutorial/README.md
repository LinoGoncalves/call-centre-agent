# 📚 Call Centre AI Agent — Onboarding & Tutorial Index

This README is the single-page onboarding and map for the tutorial series. It gets a new contributor from zero to a runnable demo, explains the architecture and the agentic framework used by the project, and points to the deeper phase tutorials.

Key goals:
- Give a clear mental model of the system and responsibilities
- Provide an actionable quick start that finishes with a working demo
- Point to the canonical agentic-framework docs and contribution process

Recommended reading order for a new engineer:
1. `docs/tutorial/PHASE_0_AGENTIC_FRAMEWORK.md` (this project's master orchestrator + sub-agent rules)
2. `docs/PROJECT_STRUCTURE.md` (how the repo is laid out)
3. `COMPREHENSIVE_BUILD_TUTORIAL.md` (high-level walkthrough)
4. Phase tutorials (1 → 6) as needed

---

## What this project is (one line)
Hybrid ML + LLM ticket classifier with an agentic orchestration layer and a production-ready Streamlit demo for telco call centre routing and triage.

## High-level architecture (quick)

Streamlit UI → Orchestrator / Enhanced Classifier → (Traditional ML | Gemini LLM)

- UI: `src/ui/streamlit_demo.py` — interactive demo used in the Phase 4 tutorial
- Orchestrator: `src/enhanced_classifier.py` (or equivalent) — fuses model outputs, applies business rules and fallbacks
- Traditional ML: `src/models/` — scikit-learn pipelines for fast, local predictions
- Gemini LLM integration: wrapper module around Google generative APIs

Key documents:
- `docs/tutorial/PHASE_0_AGENTIC_FRAMEWORK.md` — master orchestrator and sub-agent patterns (must-read)
- `agentic-framework/` — sub-agent persona files, standards, templates
- `telco-domain/` — business rules and project brief
- `docs/PROJECT_STRUCTURE.md` — file layout and conventions
- `COMPREHENSIVE_BUILD_TUTORIAL.md` — consolidated build tutorial and rationale

---

## Quick start — get a demo running (10–30 minutes)

1. Clone and enter the repo:

```powershell
git clone https://github.com/LinoGoncalves/call-centre-agent.git
cd call-centre-agent
```

2. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Create a `.env` file with required API keys. At minimum:

```text
GOOGLE_API_KEY=your_key_here
```

4. Run unit tests to verify environment:

```powershell
pytest -q
```

5. Launch the demo (Streamlit):

```powershell
python launch_demo.py
# or directly
python -m streamlit run src/ui/streamlit_demo.py --server.port=8501
```

If the Streamlit server fails to start, check the venv activation, port conflicts, and the `.env` keys.

---

## Phase map (what to read and when)

- Phase 0 — Agentic Framework (15–30 min): `docs/tutorial/PHASE_0_AGENTIC_FRAMEWORK.md`
  - Master orchestrator rules, YAML metadata conventions, prompt examples, quick snippets
- Phase 1 — Foundation (4–6 hrs): `PHASE_1_FOUNDATION.md`
  - Environment, data loading, pandas patterns, SQL→Python translations
- Phase 2 — Traditional ML (6–8 hrs): `PHASE_2_TRADITIONAL_ML.md`
  - Pipelines, TF-IDF, model evaluation, explainability
- Phase 3 — LLM Integration (4–6 hrs): `PHASE_3_GEMINI_INTEGRATION.md`
  - Gemini usage, prompt design, ensemble patterns
- Phase 4 — UI (4–6 hrs): `PHASE_4_STREAMLIT_UI.md`
  - Streamlit design, sanitization, UX decisions
- Phase 5 — Testing & Validation: `PHASE_5_TESTING_VALIDATION.md`
  - Unit/integration tests, mocking LLMs, property-based tests
- Phase 6 — Production Deployment: `PHASE_6_PRODUCTION_DEPLOYMENT.md`
  - Docker, Kubernetes, cloud deployment patterns, observability

---

## Agentic framework: where to look and how to contribute

Core locations:
- `agentic-framework/sub-agents/` — persona markdown files with YAML frontmatter
- `agentic-framework/standards/` — coding, security, testing standards
- `.github/chatmodes/agent-orchestrator.md` — canonical orchestrator behavior (single source of truth)
- `agentic-framework/agent-roster.json` — mapping between task types and agents

If you need to add or change an agent:
1. Create or edit `agentic-framework/sub-agents/<name>-agent.md` following the YAML frontmatter convention.
2. Add the agent to `agent-roster.json` with routing rules.
3. Update `agentic-framework/CHANGELOG.md` with a short note.
4. Optionally add a template under `agentic-framework/templates/` for repeatable prompts.

Security and HITL policy:
- High-risk changes must require explicit human approval. See the HITL prompts in Phase 0.
- Agents must never auto-merge PRs that touch security-sensitive code.

---

## Key files you should open now

- `src/ui/streamlit_demo.py` — Streamlit demo used for Phase 4
- `src/enhanced_classifier.py` or `src/models/` — classifier and fusion logic
- `docs/tutorial/PHASE_0_AGENTIC_FRAMEWORK.md` — orchestrator rules and prompt examples
- `docs/PROJECT_STRUCTURE.md` — project layout and contribution steps
- `telco-domain/project-brief.md` — business context and acceptance criteria

---

## Minimal contributor checklist (first PR)

1. Pick a small issue or documentation task.
2. Fork and create a branch: `feature/<short-desc>`
3. Add tests or docs for your change.
4. Update YAML frontmatter if changing agent behavior.
5. Open a PR and request review from the relevant agent owner(s).

---

## Troubleshooting tips

- Tests failing? Run `pytest -q` and read the first failing trace. Many tests expect `.env` keys to be present.
- Streamlit not starting? Kill lingering python processes and check the port.
- LLM errors? Check `GOOGLE_API_KEY` and quota/region restrictions.

---

## After you’re set up — suggested first tasks

1. Read `PHASE_0_AGENTIC_FRAMEWORK.md` and run through the quick copy-ready prompts.
2. Run the demo and send test tickets through the UI.
3. Explore `src/enhanced_classifier.py` to see fusion logic and where to add experiments.
4. Propose a small experiment in an issue and use the `data-scientist-agent` prompt recipe to scope it.

---

If you want, I can now:
- create `agentic-framework/templates/` files from the Phase 0 snippets, or
- open a PR with this README change and link reviewers, or
- run a quick markdown-lint pass and fix cosmetic warnings.

Tell me which you want next.
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
