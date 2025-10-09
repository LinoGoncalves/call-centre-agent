
# Documentation Styleguide (2025)

## Overview

This styleguide defines documentation standards for AI/ML, LLM, and agentic projects, supporting multi-tool and multi-agent collaboration.

---

## 1. General Principles
- Write concise, clear, and actionable documentation
- Use consistent formatting (Markdown, YAML frontmatter for agents)
- Include diagrams, code samples, and metadata where relevant

## 2. Structure
- Use standard templates for user guides, API references, and experiment docs
- Organize docs by audience: user, developer, operator, compliance
- Maintain a changelog and version history

## 3. Accessibility
- Use plain language and avoid jargon
- Provide alt text for images and diagrams
- Ensure docs are usable with screen readers

## 4. Multi-Agent & Tool Support
- Include agent metadata and context in agent files
- Reference universal standards and orchestration patterns
- Document agent roles, triggers, and escalation paths

---

## 5. Honesty-First Documentation Principle

**CRITICAL: Never claim statistical methods, models, or data that do not exist.**

### 5.1 Capability Labeling System

All technical claims MUST be labeled with implementation status:

- ✅ **IMPLEMENTED** - Code exists, tested, production-ready
  - Example: "The logistic regression model (trained on 500 samples, 78% test accuracy) predicts..."
  
- ⚠️ **HEURISTIC / PROPOSED** - Logic/framework exists but NOT statistically validated
  - Example: "Pool concentration estimated ~60% ±20% using risk profile heuristics (⚠️ NOT DATA-DRIVEN)"
  
- ❌ **NOT IMPLEMENTED** - Mentioned in requirements/roadmap but NO code/data
  - Example: "Monte Carlo simulation (❌ PLANNED - not yet built) would test..."

### 5.2 Statistical Claims Requirements

When documenting statistical methods, ALWAYS include:

1. **Data Source & Size**: "Trained on 500 rival pick samples from rounds R01-R20"
2. **Validation Method**: "5-fold cross-validation, 80-20 train-test split"
3. **Performance Metrics**: "Test accuracy 78% ±10%, Log-loss 0.42"
4. **Uncertainty Quantification**: "Confidence interval [68%, 88%] at 95% level"
5. **Out-of-Sample Testing**: "Validated on unseen rounds R21-R25"

**Example (Honest Statistical Documentation)**:
```markdown
## Rival Pick Prediction Model ✅ IMPLEMENTED

**Model**: Logistic Regression (scikit-learn 1.3.0)
**Dataset**: 500 samples (rival picks from R01-R20)
**Features**: odds_deviation, rival_position_delta, fixture_importance (3 features)
**Training**: 80-20 split, L2 regularization (C=1.0)
**Performance**: 
  - Test Accuracy: 78% ±10% (95% CI)
  - Log-loss: 0.42
  - F1-score: 0.76
**Validation**: 5-fold cross-validation + out-of-sample test on R21-R25
**Status**: ✅ PRODUCTION (code in `src/models/rival_predictor.py`)
```

**Counter-Example (Dishonest - NEVER DO THIS)**:
```markdown
## Rival Pick Prediction Model

Our advanced neural network analyzes 50+ features using deep learning to predict rival picks with 94% accuracy. Monte Carlo simulations run 10,000 iterations to optimize EV.
```
*Issues*: Claims neural network (none exists), 50+ features (only 3 exist), 94% accuracy (not validated), Monte Carlo (no code). This is **dishonest documentation**.

### 5.3 Heuristic Documentation Standards

When documenting heuristics (pattern-based logic, NOT statistical models):

1. **Label Clearly**: "⚠️ HEURISTIC - Pattern-based, NOT data-driven"
2. **Explain Logic**: "If rival is Conservative AND odds <2.0, predict they bank favorite"
3. **State Uncertainty**: "Estimated accuracy 60-70% (WIDE uncertainty, no validation data)"
4. **Admit Gaps**: "NO historical database exists. Inference from risk profiles only."

**Example (Honest Heuristic Documentation)**:
```markdown
## Pool Concentration Estimation ⚠️ HEURISTIC

**Method**: Risk profile pattern inference (NO statistical model)
**Logic**: 
  - Conservative rivals (70% of pool) → Follow odds favorites 80% of time
  - High-Variance rivals (20% of pool) → Contrarian 50% of time
  - Balanced rivals (10% of pool) → 50-50 mix
**Estimate**: Pool on Liverpool ~60% ±20% (WIDE uncertainty range)
**Confidence**: LOW (pattern-based, NO historical pick data)
**Validation**: NONE (no database to validate against)
**Status**: ⚠️ PROPOSED (operational heuristic, NOT proven)
```

### 5.4 Red Flags - Phrases to AVOID

❌ **Dishonest phrases** (unless you have evidence):
- "Our model predicts..." (Do you have a trained model? Where's the code?)
- "Statistical analysis shows..." (What analysis? Show methodology, data, results)
- "Monte Carlo simulation proves..." (Have you run the simulation? Show code + results)
- "Data indicates..." (What data? How much? Where from? When collected?)
- "Neural network achieves 95% accuracy" (Trained on what? Validated how?)
- "Industry best practice is..." (Citation needed. Which industry? Which source?)

✅ **Honest alternatives**:
- "The logistic regression model (trained on 500 samples) predicts..." ✅ IMPLEMENTED
- "Heuristic estimates 60% ±20%..." ⚠️ HEURISTIC
- "Monte Carlo simulation (❌ PLANNED - not yet built) would..." ❌ NOT IMPLEMENTED
- "500 samples collected from Superbru rounds R01-R20..." (explicit data source)
- "Proposed neural network (roadmap Phase 3)..." ❌ NOT IMPLEMENTED
- "Gartner report (2024) recommends..." (cited source)

### 5.5 Documentation Review Checklist

Before publishing technical documentation, verify:

- [ ] All statistical claims have ✅ IMPLEMENTED / ⚠️ HEURISTIC / ❌ NOT IMPLEMENTED labels
- [ ] All models cite: dataset size, validation method, performance metrics
- [ ] All heuristics state: logic, uncertainty range, confidence level
- [ ] All data claims specify: source, size, collection method, timestamp
- [ ] No phrases like "our model predicts..." without supporting evidence
- [ ] Uncertainty is quantified (not vague "approximately" but "60% ±20%")
- [ ] Citations provided for external claims (industry standards, research papers)

### 5.6 Correcting Dishonest Documentation

If you find documentation that violates honesty principles:

1. **Identify the claim**: "Our neural network predicts with 94% accuracy"
2. **Check implementation**: Does code exist? Is it tested? What are real metrics?
3. **Relabel appropriately**:
   - If code exists: ✅ IMPLEMENTED + add real metrics
   - If logic exists but not validated: ⚠️ HEURISTIC + explain logic + uncertainty
   - If mentioned only in requirements: ❌ NOT IMPLEMENTED + clarify it's planned
4. **Update documentation**: Replace dishonest claim with honest, labeled version
5. **Prevent recurrence**: Add this section to review checklist

**Example Correction**:

*Before (Dishonest)*:
> "Our advanced Monte Carlo simulation runs 10,000 iterations to optimize Expected Value, achieving a 15% improvement over naive strategies."

*After (Honest)*:
> "Monte Carlo simulation ❌ NOT IMPLEMENTED (planned for Phase 3 - statistical-tools-roadmap.md). Current EV calculations use closed-form odds-based formulas (✅ IMPLEMENTED in `src/calculations/ev.py`)."

---

## References
- See `user_guide_template.md`, `api_reference_template.md`, and `master-agent.md` for more details.

Last updated: 2025-10-01
