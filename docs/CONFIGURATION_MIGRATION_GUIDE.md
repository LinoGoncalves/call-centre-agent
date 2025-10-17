# Configuration Migration Guide

## Overview

This guide documents the migration from **hard-coded business rule thresholds** to a **configuration-driven architecture** for the Call Centre Agent system. This migration enables business teams to adjust routing behavior, SLA targets, and escalation policies without code changes.

**Migration Date:** October 2025  
**System Impact:** Zero breaking changes - backward compatible  
**Deployment Risk:** Low - feature flag controlled rollout  
**Rollback Time:** < 5 minutes via feature flag

---

## Table of Contents

1. [What Changed](#what-changed)
2. [Why This Change](#why-this-change)
3. [Before vs After Comparison](#before-vs-after-comparison)
4. [Migration Strategy](#migration-strategy)
5. [Implementation Details](#implementation-details)
6. [Testing & Validation](#testing--validation)
7. [Deployment Process](#deployment-process)
8. [Rollback Procedures](#rollback-procedures)
9. [Post-Migration Monitoring](#post-migration-monitoring)
10. [FAQ](#faq)

---

## What Changed

### System Architecture

**Before:** Business logic thresholds embedded in Python source code
- 15 routing rules with hard-coded confidence levels (0.85-0.99)
- 15 routing rules with hard-coded SLA hours (1-72 hours)
- Processing time thresholds (5-30 minutes)
- Escalation age thresholds (2-7 days)
- Single-region support only

**After:** External JSON configuration with hierarchical overrides
- All thresholds externalized to `config/business_rules.json`
- Multi-environment support (dev/test/prod)
- Multi-region support (za/au/us/uk)
- Feature flag controlled rollout
- Automatic validation with safety bounds

### New Components

| Component | Purpose | Lines of Code | Test Coverage |
|-----------|---------|---------------|---------------|
| `config/business_rules.json` | Base configuration file | 98 | N/A (data) |
| `src/models/business_rules_config.py` | Configuration management class | 430 | 88% |
| `tests/test_business_rules_config.py` | Unit tests for config system | 407 | 100% pass |
| `tests/test_rules_engine_config_integration.py` | Integration tests | 370 | 100% pass |

### Modified Components

| Component | Change Type | Backward Compatible |
|-----------|-------------|---------------------|
| `src/models/rules_engine.py` | Optional config parameter added | ✅ Yes |
| `config/README.md` | Documentation updated | N/A |
| `pyproject.toml` | Test markers added | N/A |

---

## Why This Change

### Business Drivers

1. **Agility** - Business teams can adjust thresholds in minutes vs days (no developer involvement)
2. **Multi-Region Support** - Different thresholds for South Africa, Australia, US, UK markets
3. **A/B Testing** - Feature flags enable experimentation without code deployment
4. **Audit Trail** - Git version control tracks all configuration changes
5. **Risk Reduction** - Validation prevents invalid threshold values

### Technical Debt Resolution

**Original Issue:** Hard-coded $500 threshold in routing rule was brittle and required code changes
**Root Cause:** Multiple hard-coded thresholds across 15 routing rules
**Solution Scope:** Comprehensive configuration system replacing ALL hard-coded thresholds

### Compliance Benefits

- **Change Management** - Configuration changes tracked via Git commits
- **Audit Requirements** - Version history provides full audit trail
- **Disaster Recovery** - Instant rollback via Git or feature flags
- **Multi-Region Compliance** - Region-specific configurations for local regulations

---

## Before vs After Comparison

### Code Example 1: Routing Rule Definition

**Before (Hard-Coded):**
```python
# src/models/rules_engine.py
def _load_default_telco_rules(self) -> List[RoutingRule]:
    return [
        RoutingRule(
            rule_id="R001_DISPUTE_EXPLICIT",
            priority=1,
            conditions={
                "keywords": ["dispute", "chargeback", "refund"],
                "confidence": 0.98  # HARD-CODED - requires code change
            },
            department="credit_management",
            sla_hours=6,  # HARD-CODED - requires code change
            description="Explicit dispute keywords detected"
        ),
        # ... 14 more rules with hard-coded values
    ]
```

**After (Config-Driven):**
```python
# src/models/rules_engine.py
def _load_default_telco_rules(self) -> List[RoutingRule]:
    return [
        RoutingRule(
            rule_id="R001_DISPUTE_EXPLICIT",
            priority=1,
            conditions={
                "keywords": ["dispute", "chargeback", "refund"],
                "confidence": self._get_confidence(
                    "R001_DISPUTE_EXPLICIT",
                    "credit_management",
                    0.98  # Fallback if config unavailable
                )
            },
            department="credit_management",
            sla_hours=self._get_sla_hours("R001_DISPUTE_EXPLICIT", 6),
            description="Explicit dispute keywords detected"
        ),
        # ... 14 more rules now config-driven
    ]

def _get_confidence(self, rule_id: str, department: str, default: float) -> float:
    """Get confidence threshold from config or use default"""
    if self.business_config and self.business_config.is_feature_enabled("use_config_driven_thresholds"):
        return self.business_config.get_confidence_threshold(department)
    return default

def _get_sla_hours(self, rule_id: str, default: int) -> int:
    """Get SLA hours from config or use default"""
    if self.business_config and self.business_config.is_feature_enabled("use_config_driven_thresholds"):
        return self.business_config.get_sla_hours(rule_id)
    return default
```

### Configuration File Example

**New File:** `config/business_rules.json`
```json
{
  "routing_thresholds": {
    "dispute_confidence_min": 0.95,
    "standard_confidence_min": 0.80,
    "hitl_trigger_threshold": 0.80
  },
  "department_sla_hours": {
    "R001_DISPUTE_EXPLICIT": 6,
    "R002_DISPUTE_IMPLIED": 12,
    "R003_SECURITY_FRAUD": 1,
    "R004_SECURITY_ACCOUNT_COMPROMISE": 2,
    "R005_PASSWORD_RESET": 6,
    ...
  },
  "feature_flags": {
    "use_config_driven_thresholds": true
  }
}
```

### Threshold Adjustment Comparison

| Task | Before (Hard-Coded) | After (Config-Driven) |
|------|---------------------|----------------------|
| **Change dispute confidence** | 1. Edit `rules_engine.py`<br>2. Run unit tests<br>3. Create PR<br>4. Code review<br>5. Deploy to prod<br>**Time:** 2-3 days | 1. Edit `business_rules.json`<br>2. Commit change<br>3. Deploy config<br>**Time:** 5-10 minutes |
| **Adjust SLA target** | Same as above | Same as above |
| **Region-specific rules** | Not possible without code duplication | Create `regions/business_rules.{region}.json` |
| **Rollback** | Git revert + redeploy code | Git revert config OR feature flag disable |
| **A/B Testing** | Requires feature branch + deployment | Toggle feature flag in config |

---

## Migration Strategy

### Phase 1: Infrastructure (✅ Completed)
- Create configuration schema and JSON files
- Implement `BusinessRulesConfig` class with validation
- Write 25 unit tests (100% passing)
- Update documentation

### Phase 2: Integration (✅ Completed)
- Modify `TelcoRulesEngine` to accept optional config
- Replace hard-coded thresholds with config lookups
- Add helper methods for config access
- Write 10 integration tests (100% passing)
- Validate backward compatibility (0 regressions)

### Phase 3: Documentation (✅ Completed)
- Update business rules documentation
- Add Section 8: Configuration Management
- Document common configuration changes
- Provide troubleshooting guide

### Phase 4: Deployment (Current Phase)
- Deploy with feature flag DISABLED initially
- Monitor system stability for 24 hours
- Enable feature flag in dev environment
- Validate dev environment for 48 hours
- Gradually enable in test, then production

### Phase 5: Optimization (Future)
- Collect business feedback on configuration UX
- Add web UI for configuration changes (optional)
- Implement configuration change approval workflow
- Add configuration diff visualization

---

## Implementation Details

### Hierarchical Configuration Loading

Configuration files are loaded in order of precedence:

```
1. Base:        config/business_rules.json
2. Environment: config/business_rules.{env}.json     (optional)
3. Region:      config/regions/business_rules.{region}.json  (optional)
```

**Example:**
```python
from src.models.business_rules_config import BusinessRulesConfig

# Load production config for Australia region
config = BusinessRulesConfig(
    environment="prod",
    region="au"
)

# Loads in order:
# 1. config/business_rules.json (base)
# 2. config/business_rules.prod.json (prod overrides)
# 3. config/regions/business_rules.au.json (AU regional overrides)
```

### Backward Compatibility Mechanism

The system supports **dual-mode operation**:

**Mode 1: Legacy (Hard-Coded)** - Used when:
- No config file present
- Config parameter not provided to `TelcoRulesEngine`
- Feature flag `use_config_driven_thresholds` is `false`

**Mode 2: Config-Driven** - Used when:
- Config file exists and is valid
- Config parameter provided to `TelcoRulesEngine`
- Feature flag `use_config_driven_thresholds` is `true`

**Code Pattern:**
```python
# Optional import - won't break if config system not available
try:
    from src.models.business_rules_config import BusinessRulesConfig
except ImportError:
    BusinessRulesConfig = None

# Optional config parameter
def __init__(self, business_config: Optional['BusinessRulesConfig'] = None):
    self.business_config = business_config
    # System works with or without config
```

### Validation System

All configuration values are validated against safety bounds:

```python
# From config/business_rules.json
"validation_rules": {
    "confidence_min": 0.5,      # 50% minimum
    "confidence_max": 1.0,      # 100% maximum
    "sla_hours_min": 1,         # 1 hour minimum
    "sla_hours_max": 168,       # 7 days maximum
    "processing_time_min": 1,   # 1 minute minimum
    "processing_time_max": 60   # 60 minutes maximum
}
```

**Validation Error Example:**
```python
# Invalid configuration
{
  "routing_thresholds": {
    "dispute_confidence_min": 0.45  # Below 0.5 minimum
  }
}

# Raises exception:
ThresholdValidationError: Invalid threshold value for 'dispute_confidence_min': 
0.45 is below minimum allowed value of 0.5
```

---

## Testing & Validation

### Pre-Migration Testing Checklist

- [x] **Unit Tests**: 25/25 passing (business_rules_config.py)
- [x] **Integration Tests**: 10/10 passing (rules_engine + config)
- [x] **Backward Compatibility**: 4/4 existing tests passing
- [x] **Code Coverage**: 88% for config system
- [x] **Regression Testing**: 0 breaking changes detected

### Test Execution Commands

```bash
# Run all configuration unit tests
python -m pytest tests/test_business_rules_config.py -v

# Run integration tests
python -m pytest tests/test_rules_engine_config_integration.py -v

# Run full test suite
python -m pytest tests/ -v --tb=short

# Run with coverage report
python -m pytest tests/ --cov=src/models --cov-report=term-missing
```

### Expected Test Results

```
tests/test_business_rules_config.py::test_default_initialization PASSED
tests/test_business_rules_config.py::test_hierarchical_override_order PASSED
tests/test_business_rules_config.py::test_environment_override PASSED
tests/test_business_rules_config.py::test_region_override PASSED
tests/test_business_rules_config.py::test_validation_catches_invalid_confidence PASSED
... (25 tests total, 100% passing)

tests/test_rules_engine_config_integration.py::test_legacy_mode_without_config PASSED
tests/test_rules_engine_config_integration.py::test_config_driven_mode PASSED
tests/test_rules_engine_config_integration.py::test_feature_flag_control PASSED
... (10 tests total, 100% passing)

==================== 39 passed in 2.45s ====================
```

### Manual Testing Scenarios

**Scenario 1: Config-Driven Routing**
```python
from src.models.business_rules_config import BusinessRulesConfig
from src.models.rules_engine import TelcoRulesEngine

# Load config
config = BusinessRulesConfig(environment="dev")

# Create rules engine with config
engine = TelcoRulesEngine(business_config=config)

# Verify config values are used
dispute_rule = next(r for r in engine.rules if r.rule_id == "R001_DISPUTE_EXPLICIT")
assert dispute_rule.conditions["confidence"] == config.get_confidence_threshold("credit_management")
assert dispute_rule.sla_hours == config.get_sla_hours("R001_DISPUTE_EXPLICIT")
```

**Scenario 2: Legacy Mode (No Config)**
```python
# Create rules engine without config (legacy mode)
engine = TelcoRulesEngine()

# Verify hard-coded defaults are used
dispute_rule = next(r for r in engine.rules if r.rule_id == "R001_DISPUTE_EXPLICIT")
assert dispute_rule.conditions["confidence"] == 0.98  # Hard-coded default
assert dispute_rule.sla_hours == 6  # Hard-coded default
```

**Scenario 3: Feature Flag Disabled**
```python
# Config exists but feature flag disabled
config = BusinessRulesConfig()
# Manually disable in config file: "use_config_driven_thresholds": false

engine = TelcoRulesEngine(business_config=config)
# System falls back to hard-coded defaults despite config being present
```

---

## Deployment Process

### Step 1: Pre-Deployment Checklist

- [ ] All tests passing (39/39 expected)
- [ ] Configuration files validated (JSON syntax)
- [ ] Feature flag set to `false` initially
- [ ] Rollback procedure documented and tested
- [ ] Monitoring dashboards prepared
- [ ] Stakeholders notified of deployment window

### Step 2: Deploy Configuration Files

```bash
# Copy configuration files to production server
scp config/business_rules.json prod-server:/app/config/
scp config/business_rules.prod.json prod-server:/app/config/

# Verify file permissions
ssh prod-server "chmod 644 /app/config/business_rules*.json"

# Validate JSON syntax on server
ssh prod-server "python -c \"import json; json.load(open('/app/config/business_rules.json'))\""
```

### Step 3: Deploy Code Changes

```bash
# Deploy updated rules_engine.py and business_rules_config.py
git pull origin main
pip install -r requirements.txt

# Restart application (config will be in legacy mode due to feature flag)
systemctl restart call-centre-agent
```

### Step 4: Validation in Production (Legacy Mode)

```bash
# Monitor logs for startup
tail -f /var/log/call-centre-agent.log

# Expected log line:
# "TelcoRulesEngine initialized in hard-coded mode (config not provided)"

# Run health checks
curl http://localhost:8000/health

# Verify routing accuracy metrics (should be unchanged)
```

**Soak Period:** Monitor for 24 hours in legacy mode to ensure deployment stability

### Step 5: Enable Config-Driven Mode (Dev First)

```bash
# Edit dev environment config
vi config/business_rules.dev.json

# Set feature flag to true
{
  "feature_flags": {
    "use_config_driven_thresholds": true
  }
}

# Restart dev environment
ssh dev-server "systemctl restart call-centre-agent"

# Monitor dev logs
# Expected: "TelcoRulesEngine initialized in config-driven mode"
```

**Validation Period:** 48 hours in dev environment

### Step 6: Gradual Production Rollout

```bash
# Enable in test environment (48 hours)
# Enable in production (monitor for 1 week)

# Final production config
vi config/business_rules.prod.json
{
  "feature_flags": {
    "use_config_driven_thresholds": true
  }
}
```

---

## Rollback Procedures

### Option 1: Feature Flag Disable (Fastest - 30 seconds)

```bash
# Disable feature flag in production config
vi config/business_rules.prod.json
{
  "feature_flags": {
    "use_config_driven_thresholds": false  # Reverts to hard-coded
  }
}

# Restart application
systemctl restart call-centre-agent

# Verify legacy mode active
grep "hard-coded mode" /var/log/call-centre-agent.log
```

**Impact:** Immediate reversion to hard-coded thresholds
**Data Loss:** None (configuration files preserved for investigation)
**Risk:** Minimal

### Option 2: Git Revert Configuration (5 minutes)

```bash
# Revert configuration file changes
git checkout HEAD~1 config/business_rules.json
git commit -m "Rollback: Revert config changes - [issue description]"
git push origin main

# Deploy reverted config
scp config/business_rules.json prod-server:/app/config/
ssh prod-server "systemctl restart call-centre-agent"
```

**Impact:** Reverts to previous configuration values
**Data Loss:** None (can re-apply changes later)
**Risk:** Low

### Option 3: Full Code Rollback (15 minutes)

```bash
# Revert entire commit (config + code changes)
git revert <commit-hash>
git push origin main

# Deploy previous version
ssh prod-server "cd /app && git pull origin main"
ssh prod-server "systemctl restart call-centre-agent"
```

**Impact:** Full reversion to pre-migration state
**Data Loss:** None
**Risk:** Low (thoroughly tested backward compatibility)

### Rollback Decision Matrix

| Issue Severity | Recommended Option | Expected Downtime |
|----------------|-------------------|-------------------|
| **Critical** (routing failures) | Option 1: Feature Flag | < 1 minute |
| **High** (incorrect thresholds) | Option 2: Git Revert Config | < 5 minutes |
| **Medium** (performance degradation) | Option 2: Git Revert Config | < 5 minutes |
| **Low** (minor bugs) | Fix forward + config adjustment | N/A |

---

## Post-Migration Monitoring

### Key Metrics to Track

**Week 1: Stability Metrics**
- Application startup time (should be unchanged)
- Memory usage (config loading overhead ~1MB)
- Routing latency (should be < 5ms difference)
- Error rate (should remain at baseline)

**Week 2-4: Business Metrics**
- Routing accuracy by department (compare to pre-migration baseline)
- SLA compliance rate (should improve with tuned thresholds)
- HITL validation rate (should be configurable now)
- False positive rate (can be reduced via config tuning)

**Ongoing: Configuration Change Metrics**
- Frequency of configuration changes
- Time from threshold issue identified to resolution
- Number of rollbacks required
- Business team satisfaction with self-service capability

### Monitoring Commands

```bash
# Check which mode is active
grep "TelcoRulesEngine initialized" /var/log/call-centre-agent.log

# Verify configuration values loaded
curl http://localhost:8000/api/config/status

# Monitor routing decisions
tail -f /var/log/routing-decisions.log | grep "config-driven"

# Check for validation errors
grep "ThresholdValidationError" /var/log/call-centre-agent.log
```

### Success Criteria (30-day evaluation)

- [ ] Zero production incidents related to configuration system
- [ ] At least 5 successful configuration changes without developer involvement
- [ ] Routing accuracy maintained or improved (≥ 95% baseline)
- [ ] Business team reports improved agility (survey)
- [ ] Configuration change cycle time < 1 hour (from request to deployment)

---

## FAQ

### Q1: Will this migration cause downtime?
**A:** No. The system is backward compatible and deploys with feature flag disabled. Downtime only occurs during normal application restart (~30 seconds).

### Q2: What happens if the configuration file is invalid?
**A:** The system validates configuration on startup. If validation fails, it falls back to hard-coded defaults and logs an error. The application continues running.

### Q3: Can we gradually enable config-driven mode for specific rules?
**A:** Not in the current implementation. The feature flag controls all 15 rules together. Future enhancement could add per-rule feature flags.

### Q4: How do we test configuration changes before production?
**A:** Use the environment hierarchy:
1. Test changes in `business_rules.dev.json` first
2. Validate in dev environment for 48 hours
3. Graduate to `business_rules.test.json`
4. Finally deploy to `business_rules.prod.json`

### Q5: What if we need region-specific rules that don't exist in base config?
**A:** Region-specific configurations inherit from base and override specific values. You cannot add entirely new configuration keys in regional overrides (safety limitation).

### Q6: Can we roll back just one threshold change without reverting all changes?
**A:** Yes. Edit the specific key in the configuration file and commit the change. Git history preserves all previous values.

### Q7: How do we audit who changed what configuration?
**A:** All configuration changes are tracked via Git commits:
```bash
git log --follow config/business_rules.json
git blame config/business_rules.json
```

### Q8: What's the performance impact of configuration loading?
**A:** Negligible. Configuration is loaded once at application startup (~10ms). Runtime performance is identical to hard-coded approach.

### Q9: Can we use configuration for ML model thresholds too?
**A:** Yes, but that's a future enhancement. Current implementation focuses on routing rules. ML model configuration could be added in Phase 6.

### Q10: What if we want to experiment with different thresholds on a subset of tickets?
**A:** Current implementation doesn't support A/B testing at the ticket level. You can use the dev environment to test threshold changes before production deployment. Future enhancement could add percentage-based rollout.

---

## Support Contacts

**Technical Issues:**
- Development Team Lead: dev-lead@company.com
- DevOps Engineer: devops@company.com

**Configuration Questions:**
- Operations Manager: ops-manager@company.com
- Customer Service Team Lead: cs-lead@company.com

**Emergency Escalation:**
- On-Call Rotation: +1-555-ONCALL (665-2255)
- Production Incident Channel: #prod-incidents (Slack)

---

## Appendix A: Configuration Schema Reference

See `config/README.md` for complete schema documentation.

**Quick Reference:**
- `routing_thresholds.*` - Confidence levels for classification
- `department_sla_hours.*` - SLA targets per routing rule
- `processing_time_sla.*` - Stage-specific time limits
- `escalation_thresholds.*` - Age-based escalation triggers
- `priority_sla_response.*` - Priority-based response times
- `currency_settings.*` - Multi-region currency support
- `feature_flags.*` - Runtime toggles for features
- `validation_rules.*` - Safety bounds for all thresholds

## Appendix B: Related Documentation

- **Business Rules**: `telco-domain/business-rules/Business Rules/Departmental_Routing_Rules.md`
- **Configuration Guide**: `config/README.md`
- **API Documentation**: `docs/api/business_rules_config.md`
- **Architecture Decision**: `docs/ADR-001-configuration-driven-architecture.md`

---

**Document Version:** 1.0  
**Last Updated:** October 2025  
**Next Review:** November 2025  
**Maintained By:** Development Team Lead
