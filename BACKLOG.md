# Call Centre Agent — Product Backlog

This backlog provides prioritized, actionable epics and user stories for transforming the demo into a production system. Items are organized by strategic pillar (see `ROADMAP.md`) and priority (P0 = Critical, P1 = High, P2 = Medium, P3 = Low).

---

## Epic 1: Vector DB + RAG Integration (Q1 2026)

### P0: Set Up Vector Database Infrastructure
**Goal**: Deploy and configure vector database for historical ticket embeddings.

**Tasks**:
- [ ] **1.1**: Evaluate vector DB providers (Pinecone, Weaviate, Qdrant) — criteria: cost, latency, Azure integration.
- [ ] **1.2**: Provision Pinecone serverless index (or Weaviate Cloud) with 1536-dim vectors.
- [ ] **1.3**: Create Python client wrapper with connection pooling and retry logic.
- [ ] **1.4**: Implement health check endpoint (`/vector-db/health`).
- [ ] **1.5**: Write integration tests for upsert, query, and delete operations.

**Acceptance Criteria**:
- Vector DB responds to queries in <50ms (p95).
- Client library handles transient failures with exponential backoff.
- 100% test coverage for client wrapper.

**Estimated Effort**: 1 week (1 engineer)

---

### P0: Implement Embedding Generation Pipeline
**Goal**: Batch-generate embeddings for historical tickets and new tickets.

**Tasks**:
- [ ] **1.6**: Integrate OpenAI Embeddings API (`text-embedding-3-small`).
- [ ] **1.7**: Build batch processing script (1000 tickets/batch) with rate limiting.
- [ ] **1.8**: Store embeddings in PostgreSQL (`ticket_embeddings` table) with ticket_id foreign key.
- [ ] **1.9**: Upsert embeddings to vector DB with metadata (department, urgency, sentiment).
- [ ] **1.10**: Schedule nightly Airflow job to embed new tickets.

**Acceptance Criteria**:
- Embedding generation cost: <$0.10 per 10,000 tickets.
- Zero data loss during batch processing.
- Embeddings indexed in vector DB within 1 hour of ticket creation.

**Estimated Effort**: 1.5 weeks (1 engineer)

---

### P1: Build RAG-Based LLM Prompting
**Goal**: Retrieve top-k similar tickets and use as few-shot examples for LLM.

**Tasks**:
- [ ] **1.11**: Implement similarity search function (cosine similarity, k=5).
- [ ] **1.12**: Format retrieved tickets as few-shot examples in LLM prompt.
- [ ] **1.13**: Measure accuracy improvement with RAG vs. zero-shot prompting (A/B test on 500 tickets).
- [ ] **1.14**: Add fallback to zero-shot if similarity score <0.75.
- [ ] **1.15**: Cache LLM responses in Redis (TTL: 24 hours).

**Prompt Template Example**:
```
You are a call centre ticket classifier. Here are 5 similar historical tickets and their classifications:

1. Ticket: "My bill shows duplicate charges"
   Department: Billing | Urgency: Medium | Sentiment: Negative

2. Ticket: "Refund request for incorrect charge"
   Department: Billing | Urgency: High | Sentiment: Negative

[...3 more examples...]

Now classify this ticket:
Ticket: "I was charged twice for the same service"
Department: ? | Urgency: ? | Sentiment: ?
```

**Acceptance Criteria**:
- RAG-enhanced prompts improve accuracy by ≥3% vs. zero-shot.
- LLM token usage reduced by 20% (fewer tokens in prompt due to targeted examples).

**Estimated Effort**: 2 weeks (1 engineer)

---

### P1: Implement Confidence-Based Routing Logic
**Goal**: Route to cached classification if similarity ≥ 0.92 and accuracy ≥ 85%.

**Tasks**:
- [ ] **1.16**: Query vector DB for top-1 match similarity score.
- [ ] **1.17**: Fetch historical accuracy for that ticket's classification from PostgreSQL.
- [ ] **1.18**: If both thresholds met, return cached classification (skip LLM).
- [ ] **1.19**: Log routing decision (cache hit/miss) for analysis.
- [ ] **1.20**: Monitor cache hit rate daily in Grafana.

**Decision Logic**:
```python
top_match = vector_db.query(ticket_embedding, top_k=1)
if top_match.score >= 0.92 and top_match.historical_accuracy >= 0.85:
    return top_match.classification  # Cache hit
else:
    return llm_classify_with_rag(ticket, top_k=5)  # LLM call
```

**Acceptance Criteria**:
- Achieve 60% cache hit rate within 4 weeks.
- Zero false positives (incorrect cached classifications).

**Estimated Effort**: 1 week (1 engineer)

---

## Epic 2: Rules Engine + Hybrid Routing (Q1 2026)

### P0: Design and Implement Rules Engine
**Goal**: Create a deterministic rules engine for high-confidence patterns.

**Tasks**:
- [ ] **2.1**: Define 10 initial rules in YAML (e.g., "account locked" → Security, 100% confidence).
- [ ] **2.2**: Build Python rules engine that evaluates rules sequentially (first match wins).
- [ ] **2.3**: Add confidence scores to each rule (100% for exact match, 90% for regex).
- [ ] **2.4**: Implement short-circuit logic (if rule matches with ≥85% confidence, skip ML/LLM).
- [ ] **2.5**: Create `/rules/validate` API endpoint for testing rules before deployment.

**Example Rule (YAML)**:
```yaml
rules:
  - id: R001
    pattern: "account.*locked|cannot.*login"
    regex: true
    department: Security
    urgency: High
    confidence: 0.95
    
  - id: R002
    pattern: "refund"
    keywords: ["billing", "charge", "payment"]
    department: Billing
    urgency: Medium
    confidence: 0.90
```

**Acceptance Criteria**:
- Rules engine processes 10,000 tickets/sec (in-memory evaluation).
- Business analysts can add rules via UI (future enhancement).

**Estimated Effort**: 2 weeks (1 engineer)

---

### P1: Integrate Rules Engine into Classification Pipeline
**Goal**: Add rules engine as the first routing layer.

**Tasks**:
- [ ] **2.6**: Modify `classify_ticket()` function to check rules first.
- [ ] **2.7**: Log rule matches vs. ML/LLM predictions for accuracy validation.
- [ ] **2.8**: A/B test rules engine vs. direct ML for 2 weeks (50/50 split).
- [ ] **2.9**: Gradually increase rule confidence threshold based on accuracy.
- [ ] **2.10**: Add Grafana dashboard for rule hit rate and accuracy per rule.

**Acceptance Criteria**:
- Rules engine accuracy ≥95% (manual audit of 1000 tickets).
- 15-25% of tickets routed by rules (no ML/LLM needed).

**Estimated Effort**: 1.5 weeks (1 engineer)

---

## Epic 3: MLOps Pipeline (Q2 2026)

### P0: Set Up Experiment Tracking with MLflow
**Goal**: Track all model training experiments centrally.

**Tasks**:
- [ ] **3.1**: Deploy MLflow server on Azure (App Service or AKS).
- [ ] **3.2**: Integrate MLflow logging in `train_model.py` script.
- [ ] **3.3**: Log hyperparameters (C, max_iter, ngram_range), metrics (F1, precision, recall), and model artifacts.
- [ ] **3.4**: Create MLflow project template for reproducible training.
- [ ] **3.5**: Set up model registry (staging/production stages).

**Acceptance Criteria**:
- All training runs logged to MLflow with <5s overhead per run.
- Model artifacts stored in Azure Blob Storage.

**Estimated Effort**: 1 week (1 engineer)

---

### P1: Automate Weekly Model Retraining
**Goal**: Schedule automatic retraining on fresh data.

**Tasks**:
- [ ] **3.6**: Create Airflow DAG for weekly retraining (Sunday 2am UTC).
- [ ] **3.7**: Pull last 90 days of validated tickets from PostgreSQL.
- [ ] **3.8**: Split into train/validation/test (70/15/15).
- [ ] **3.9**: Train model, log to MLflow, and compare against production baseline.
- [ ] **3.10**: If new model F1 > baseline + 0.02, promote to staging; else discard.

**Acceptance Criteria**:
- Retraining completes in <2 hours.
- Zero manual intervention required.

**Estimated Effort**: 1.5 weeks (1 engineer)

---

### P1: Deploy FastAPI Model Serving Layer
**Goal**: Serve models via REST API with versioning and auto-scaling.

**Tasks**:
- [ ] **3.11**: Create FastAPI app with `/classify`, `/batch-classify`, `/health` endpoints.
- [ ] **3.12**: Load model from MLflow Model Registry at startup.
- [ ] **3.13**: Add Prometheus metrics endpoint (`/metrics`).
- [ ] **3.14**: Deploy to AKS with HPA (3-20 replicas, CPU target: 70%).
- [ ] **3.15**: Implement canary deployment (10% traffic to new model version).

**Acceptance Criteria**:
- API responds in <200ms (p95) for single classification.
- Zero downtime during model updates.

**Estimated Effort**: 2 weeks (1 engineer)

---

## Epic 4: Data Engineering & Sanitization (Q2 2026)

### P0: Build Data Sanitization Pipeline
**Goal**: Remove PII and normalize tickets before processing.

**Tasks**:
- [ ] **4.1**: Implement regex-based PII detection (email, phone, account ID).
- [ ] **4.2**: Integrate spaCy NER for additional PII detection (PERSON, ORG, GPE).
- [ ] **4.3**: Replace detected PII with placeholders (`<EMAIL>`, `<PHONE>`, `<ACCOUNT_ID>`).
- [ ] **4.4**: Normalize text (lowercase, remove extra whitespace, expand contractions).
- [ ] **4.5**: Store sanitized tickets in `tickets_clean` table.

**Example**:
```
Before: "My account abc123 was charged $50 to john.doe@example.com"
After: "my account <ACCOUNT_ID> was charged $50 to <EMAIL>"
```

**Acceptance Criteria**:
- 99.5% PII detection rate (validated on 10,000 sample tickets).
- Processing speed: 1000 tickets/sec.

**Estimated Effort**: 1.5 weeks (1 engineer)

---

### P1: Build Airflow Data Pipeline for Ticket Ingestion
**Goal**: Automate hourly ticket sync from ServiceNow/Zendesk.

**Tasks**:
- [ ] **4.6**: Create Airflow DAG for hourly ticket pull (every hour at :05).
- [ ] **4.7**: Integrate ServiceNow REST API client with OAuth authentication.
- [ ] **4.8**: Upsert tickets to PostgreSQL (idempotent on ticket_id).
- [ ] **4.9**: Trigger sanitization and embedding generation for new tickets.
- [ ] **4.10**: Send Slack alert if ingestion fails or falls behind by >2 hours.

**Acceptance Criteria**:
- 99.9% ingestion success rate.
- Tickets available for classification within 15 minutes of creation.

**Estimated Effort**: 2 weeks (1 engineer)

---

## Epic 5: Enterprise Integration (Q3 2026)

### P0: Integrate with ServiceNow
**Goal**: Bi-directional integration with ServiceNow for ticket classification.

**Tasks**:
- [ ] **5.1**: Set up ServiceNow webhook to call `/classify` API on ticket creation.
- [ ] **5.2**: Update `assignment_group` and `urgency` fields in ServiceNow based on classification.
- [ ] **5.3**: Post AI reasoning as work note for agent visibility.
- [ ] **5.4**: Implement retry logic with exponential backoff (max 3 retries).
- [ ] **5.5**: Pilot with Billing department (500 tickets/day).

**Acceptance Criteria**:
- 99% successful ticket updates in ServiceNow.
- Agents report improved routing accuracy (qualitative survey).

**Estimated Effort**: 2 weeks (1 engineer)

---

### P2: Integrate with Zendesk and Jira
**Goal**: Extend integration to Zendesk and Jira Service Desk.

**Tasks**:
- [ ] **5.6**: Zendesk webhook → classify → set tags and priority.
- [ ] **5.7**: Jira webhook → classify → assign to team and set SLA.
- [ ] **5.8**: Build abstraction layer to normalize ticket fields across platforms.
- [ ] **5.9**: Add configuration UI for mapping fields (department → tag/assignee).

**Estimated Effort**: 3 weeks (1 engineer)

---

## Epic 6: Cloud Deployment & Scaling (Q3 2026)

### P0: Deploy to Azure Kubernetes Service (AKS)
**Goal**: Production-grade Kubernetes deployment with auto-scaling.

**Tasks**:
- [ ] **6.1**: Provision AKS cluster (3 node pools: system, user, spot).
- [ ] **6.2**: Deploy FastAPI app with Helm chart (ConfigMap, Secrets, HPA).
- [ ] **6.3**: Set up NGINX Ingress with TLS termination (Let's Encrypt).
- [ ] **6.4**: Configure Azure Front Door for multi-region load balancing.
- [ ] **6.5**: Implement Pod Disruption Budgets (min 2 replicas always available).

**Acceptance Criteria**:
- Zero downtime deployments (rolling updates).
- Auto-scale from 3 to 20 pods based on CPU/memory.

**Estimated Effort**: 2 weeks (1 DevOps engineer)

---

### P1: Set Up PostgreSQL and Redis on Azure
**Goal**: Deploy managed databases with high availability.

**Tasks**:
- [ ] **6.6**: Provision Azure Database for PostgreSQL (Flexible Server, HA enabled).
- [ ] **6.7**: Enable read replicas for reporting queries.
- [ ] **6.8**: Provision Azure Cache for Redis (Premium tier, 6GB).
- [ ] **6.9**: Configure private endpoints (no public IPs).
- [ ] **6.10**: Set up automated backups (daily, 30-day retention).

**Estimated Effort**: 1 week (1 DevOps engineer)

---

## Epic 7: Governance & Security (Q4 2026)

### P0: Implement Audit Logging
**Goal**: Log every classification decision for compliance.

**Tasks**:
- [ ] **7.1**: Create `audit_log` table in PostgreSQL with fields: ticket_id, model_version, prediction, confidence, routing_method, timestamp, user_id.
- [ ] **7.2**: Append-only writes (no updates/deletes).
- [ ] **7.3**: Partition by month for performance.
- [ ] **7.4**: Replicate to Azure Table Storage for long-term retention (7 years).
- [ ] **7.5**: Build compliance report generator (monthly accuracy, bias checks).

**Acceptance Criteria**:
- 100% of classifications logged with <5ms write latency.
- Audit logs tamper-proof (append-only).

**Estimated Effort**: 1.5 weeks (1 engineer)

---

### P1: Implement GDPR Compliance (Right to Deletion)
**Goal**: Allow customers to request deletion of their data.

**Tasks**:
- [ ] **7.6**: Create `/gdpr/delete-customer-data` API endpoint (authenticated).
- [ ] **7.7**: Delete customer tickets from PostgreSQL (cascade to embeddings).
- [ ] **7.8**: Delete vectors from vector DB by metadata filter (customer_id).
- [ ] **7.9**: Anonymize audit logs (replace ticket_id with hash).
- [ ] **7.10**: Return deletion confirmation within 30 days (GDPR requirement).

**Estimated Effort**: 1 week (1 engineer)

---

## Epic 8: Monitoring & Observability (Ongoing)

### P0: Set Up Prometheus + Grafana
**Goal**: Real-time monitoring of API and model performance.

**Tasks**:
- [ ] **8.1**: Deploy Prometheus on AKS (scrape interval: 15s).
- [ ] **8.2**: Instrument FastAPI with Prometheus client (request count, latency, error rate).
- [ ] **8.3**: Add custom metrics: llm_cost_daily, cache_hit_rate, classification_accuracy.
- [ ] **8.4**: Deploy Grafana with dashboards: API performance, model metrics, cost tracking.
- [ ] **8.5**: Set up PagerDuty alerts for p95 latency >2s, error rate >1%.

**Acceptance Criteria**:
- Dashboards accessible to all engineers 24/7.
- Alert response time <10 minutes (automated or manual).

**Estimated Effort**: 1.5 weeks (1 SRE)

---

### P1: Implement Distributed Tracing with OpenTelemetry
**Goal**: Trace requests across services for debugging.

**Tasks**:
- [ ] **8.6**: Integrate OpenTelemetry SDK in FastAPI, ML service, LLM client.
- [ ] **8.7**: Export traces to Jaeger or Azure Application Insights.
- [ ] **8.8**: Add correlation IDs to logs and traces.
- [ ] **8.9**: Build trace analysis dashboard (identify slow spans).

**Estimated Effort**: 1 week (1 SRE)

---

## Prioritized Sprint Backlog (Next 12 Weeks)

### Sprint 1-2 (Weeks 1-4): Vector DB + RAG Foundation
- [ ] 1.1-1.5: Vector DB setup
- [ ] 1.6-1.10: Embedding pipeline
- [ ] 1.11-1.15: RAG prompting

### Sprint 3-4 (Weeks 5-8): Rules Engine + MLOps
- [ ] 2.1-2.5: Rules engine
- [ ] 3.1-3.5: MLflow setup
- [ ] 1.16-1.20: Confidence routing

### Sprint 5-6 (Weeks 9-12): Data Engineering + Integration
- [ ] 4.1-4.5: Sanitization pipeline
- [ ] 4.6-4.10: Airflow ingestion
- [ ] 5.1-5.5: ServiceNow integration

---

## Backlog Grooming Cadence

- **Weekly**: Review top 5 P0 items in standup.
- **Bi-weekly**: Refine upcoming sprint stories (add acceptance criteria, estimates).
- **Monthly**: Reprioritize backlog based on production metrics and stakeholder feedback.

---

For strategic context, see `ROADMAP.md`.
