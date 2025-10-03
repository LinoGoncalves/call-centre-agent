# Call Centre Agent — Overview & Onboarding

This repository contains a production-focused hybrid ML + LLM system for call-centre ticket classification and routing. It includes a tutorial series, an agentic orchestration framework, a production-ready Streamlit demo, and a roadmap/backlog for taking the demo to full production.

If you're joining the project, start with `docs/tutorial/PHASE_0_AGENTIC_FRAMEWORK.md` (Agentic framework). Then follow `docs/tutorial/README.md` for the phased learning path.

---

## Quick links

- Tutorials: `docs/tutorial/README.md`
- Phase 0 (Agentic framework): `docs/tutorial/PHASE_0_AGENTIC_FRAMEWORK.md`
- Roadmap: `ROADMAP.md`
- Backlog (prioritized): `BACKLOG.md`
- Contribution & Onboarding: `CONTRIBUTING.md`

---

## Quick start (local dev)

1. Clone the repo and create a virtual environment:

```powershell
git clone https://github.com/LinoGoncalves/call-centre-agent.git
cd call-centre-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy environment template and add API keys:

```powershell
copy .env.example .env
# Edit .env to add GOOGLE_API_KEY and other secrets
```

3. Run tests to verify your environment:

```powershell
pytest -q
```

4. Launch the demo (Streamlit):

```powershell
python launch_demo.py
# or
python -m streamlit run src/ui/streamlit_demo.py --server.port=8501
```

---

## Project structure (short)

- `src/` — application code (models, UI, API)
- `docs/` — tutorials, standards, agentic-framework
- `agentic-framework/` — sub-agent personas, templates, standards
- `telco-domain/` — domain business rules and project brief
- `ROADMAP.md` / `BACKLOG.md` — strategic roadmap and tactical backlog
- `CONTRIBUTING.md` — onboarding, PR process, code review guidelines

See `docs/PROJECT_STRUCTURE.md` for a full map.

---

## What to read first (recommended onboarding)

1. `docs/tutorial/PHASE_0_AGENTIC_FRAMEWORK.md` — Understand master orchestrator and agent roles
2. `docs/tutorial/README.md` — Tutorial phases and learning path
3. `COMPREHENSIVE_BUILD_TUTORIAL.md` — Hands-on build walkthrough
4. `ROADMAP.md` and `BACKLOG.md` — Strategy and prioritized work
5. `CONTRIBUTING.md` — How to contribute and run the project

---

## Production roadmap highlights

- Use a Vector DB (Pinecone/Weaviate/Qdrant) to store embeddings of historical tickets and implement RAG to reduce LLM calls.
- Implement a rules engine for deterministic routing where confidence ≥85%.
- Build an MLOps pipeline (Airflow + MLflow + KServe/FastAPI) for retraining and serving.
- Integrate with ServiceNow/Zendesk/Jira using idempotent webhooks and field mapping.
- Implement governance (audit logs, model cards, GDPR right-to-delete) and observability (Prometheus/Grafana/OpenTelemetry).

Full details: `ROADMAP.md` and `BACKLOG.md`.

---

## Contributor workflow (short)

1. Branch from `develop` or create `feature/*` (see `CONTRIBUTING.md`).
2. Add tests for new behavior and update docs.
3. Open a PR to `develop`, add reviewers and link related ROADMAP/BACKLOG items.
4. Use CI to run tests and linters; once green, request approvals and merge.

---

## Support

If you run into issues:
1. Check `docs/tutorial/README.md` and `docs/COMPREHENSIVE_BUILD_TUTORIAL.md`.
2. Run `pytest -q` and attach failing traces to issues.
3. For environment or deployment issues, check `CONTRIBUTING.md` for recommended dev setup.

---

If you'd like, I can also open GitHub Issues for the top-priority backlog items, or create architecture diagrams under `docs/diagrams/`.

---

Updated to reflect Phase 0, roadmap/backlog, and contributor onboarding.

