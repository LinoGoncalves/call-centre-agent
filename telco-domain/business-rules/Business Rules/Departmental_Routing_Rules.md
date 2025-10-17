# Departmental Routing & Escalation Rules

**Version:** 1.1  
**Effective Date:** October 17, 2025  
**Department:** Customer Service Operations  
**Configuration Status:** ✨ **Now supports dynamic configuration via `config/business_rules.json`**

## 📋 Configuration Overview

This document describes business rules that are **now configurable** without code changes. Thresholds, SLA times, and confidence levels can be adjusted via:

- **Configuration File**: `config/business_rules.json`
- **Environment Overrides**: `config/business_rules.{env}.json`
- **Region Overrides**: `config/regions/{region}.json`

See **Section 8: Configuration Management** at the bottom of this document for implementation details.

---

## 1. Dispute vs General Billing Inquiry Classification

### 1.1 Dispute (Billing Dispute) - Route to Credit Management
**Definition:** A formal challenge where the customer asserts that a specific charge, fee, or the entire bill is incorrect, unauthorized, or violates the agreed-upon terms of service.

**Key Characteristics:**
- **Contesting the Validity**: Customer explicitly states they believe a charge is wrong and should be removed or corrected
- **Requires Investigation**: Agent cannot resolve on the spot with standard information
- **Must initiate investigation** involving:
  - Reviewing service records (usage logs, contract terms)
  - Involving specialized teams (billing integrity, fraud, collections)
  - Placing disputed amount on hold to prevent collection action or service interruption

**Common Examples:**
- **Unauthorized Charges**: Premium service, third-party content, or equipment never ordered/authorized
- **Incorrect Pricing/Discounts**: Bill doesn't reflect agreed-upon promotional rate, discount, or package price
- **Double Billing**: Charged twice for same service or equipment
- **Service Not Received/Used**: Charge for unavailable, defective, or undelivered services (e.g., billing during extended outage)
- **Post-Cancellation Charges**: Billed for service after confirmed cancellation

**Detection Keywords:**
- "dispute", "disagree with charges", "incorrect billing"
- "unauthorized", "never ordered", "didn't authorize"
- "double charged", "charged twice", "duplicate billing"
- "service was down", "didn't receive service", "outage"
- "cancelled but still charged", "post-cancellation"
- "refund", "credit", "overcharged", "billing error"
- "contest", "challenge", "reject", "remove this charge"

### 1.2 General Billing Inquiry - Route to Billing Team
**Definition:** Request for clarification, explanation, or general information about charges, but customer has not formally rejected the charge's validity.

**Key Characteristics:**
- **Seeking Understanding**: Customer confused, surprised, or wants explanation
- **Resolved by Explanation**: Can typically be resolved quickly by agent providing clear, itemized explanation

**Common Examples:**
- "My bill is higher than last month, why?"
- Understanding usage details (data overage, international calls, family plan breakdown)
- Clarification of fees ("regulatory recovery fee", "administrative charge")
- Payment status inquiries (payment received, due date)
- Requesting duplicate bill or detailed statement

**Detection Keywords:**
- "explain my bill", "why is my bill", "what does this mean"
- "payment options", "when is due", "payment received"
- "account balance", "billing cycle", "statement"
- "breakdown", "itemized", "details"

## 2. Departmental Routing Matrix

### 2.1 Primary Routing Rules (Priority Order)

| Priority | Department | Routing Criteria | Examples |
|----------|------------|------------------|----------|
| **1** | **Credit Management** | ALL logged disputes (regardless of category) | "I dispute this charge", "This is wrong billing" |
| **2** | **Order Management** | New orders, plan changes, installations | "Install new service", "Upgrade my plan" |
| **3** | **CRM** | General complaints, retention issues | "Poor service", "Thinking of leaving" |
| **4** | **Billing** | Non-disputed billing inquiries | "Explain my bill", "Payment options" |

### 2.2 Detailed Department Assignments

#### Credit Management Team 💰
- **All Disputes** (100% priority)
- Billing discrepancies requiring investigation
- Refund requests and credit adjustments
- Charge reversals and billing corrections
- Contract disputes and termination fees
- Fraud reports and unauthorized usage

#### Order Management Team 📋
- New service orders and installations
- Plan changes and upgrades/downgrades
- Service activations and deactivations
- Equipment orders and exchanges
- Delivery and fulfillment issues
- Service migrations

#### CRM Team 🤝
- Customer relationship management
- Retention and loyalty issues
- General complaints and satisfaction
- Account relationship problems
- Customer experience feedback
- Cancellation requests (non-billing disputes)

#### Billing Team 🧾
- Non-disputed billing inquiries
- Payment method updates
- Invoice explanations and breakdowns
- Payment arrangements and extensions
- Account balance inquiries
- Billing cycle information

## 3. Service Desk Agent & Escalation Rules

### 3.1 Service Desk Agent Role
- **Initial Classification**: First-level ticket analysis and routing
- **Quality Assurance**: Verify AI routing decisions before final assignment
- **Escalation Management**: Monitor ticket age and trigger escalations
- **HITL Validation**: Human oversight for low-confidence routing decisions

### 3.2 Age-Based Escalation Rules

| Ticket Age | Escalation Level | Action Required | Notification |
|------------|------------------|-----------------|--------------|
| **> 2 Days** | Team Lead | Route to Department Team Lead | Email + System Alert |
| **> 1 Week** | Production Support | Escalate to Production Support Manager | Email + SMS + System Alert |

### 3.3 Priority-Based SLA Response Times

| Priority | Response Time | Action Required | Escalation Trigger |
|----------|---------------|-----------------|-------------------|
| **P0 (IMMEDIATE)** | 1 Hour | Immediate attention, all hands | 30 min warning |
| **P1 (HIGH)** | 6 Hours | Same business day resolution | 4 hr warning |
| **P2 (MEDIUM)** | 24 Hours | Next business day resolution | 18 hr warning |
| **P3 (STANDARD)** | 36 Hours | Standard queue processing | 30 hr warning |

## 4. Confidence Thresholds & HITL Triggers

### 4.1 Routing Confidence Requirements
- **Credit Management (Disputes)**: ≥ 95% confidence
- **Other Departments**: ≥ 80% confidence
- **Below Threshold**: Route to Service Desk Agent for HITL validation

### 4.2 Human-in-the-Loop Triggers
1. **Low Confidence**: Routing confidence < 80%
2. **Dispute Uncertainty**: Dispute detection confidence < 95%
3. **Multi-Department**: Ticket could belong to multiple departments
4. **Edge Cases**: Unusual patterns or new ticket types
5. **Override History**: Tickets similar to previously overridden ones

## 5. Implementation Performance Requirements

### 5.1 Processing Time Targets
- **AI Classification + Routing**: < 5 minutes (acceptable threshold)
- **Service Desk Agent Review**: < 10 minutes for HITL cases
- **Department Assignment**: < 15 minutes total end-to-end

### 5.2 Accuracy Targets
- **Dispute Detection**: ≥ 98% accuracy *(configurable via `accuracy_targets.dispute_detection_accuracy`)*
- **Department Routing**: ≥ 95% accuracy overall *(configurable via `accuracy_targets.department_routing_accuracy`)*
- **False Positive Rate**: < 2% for disputes *(configurable via `accuracy_targets.false_positive_rate_max`)*
- **Internal Transfers**: < 5% between departments *(configurable via `accuracy_targets.internal_transfer_rate_max`)*

## 6. Training & Change Management

### 6.1 In-House Training Requirements
- **Service Desk Agents**: 4-hour routing system training
- **Department Teams**: 2-hour new process orientation  
- **Team Leads**: 3-hour escalation management training
- **Production Support**: 2-hour system overview

### 6.2 Switchover Strategy
- **Phase 1**: Parallel running with existing system (2 weeks)
- **Phase 2**: Gradual transition with human oversight (2 weeks)
- **Phase 3**: Full automation with exception handling (ongoing)

## 7. Monitoring & Quality Assurance

### 7.1 Daily Metrics
- Routing accuracy by department
- Average processing time
- HITL validation rate
- Escalation triggers by age and priority

### 7.2 Weekly Review
- Departmental routing effectiveness
- Training needs assessment
- System performance optimization
- Customer satisfaction impact analysis

---

## 8. Configuration Management

### 8.1 Configuration System Overview

All business rule thresholds are now externally configurable via JSON configuration files. This enables business users to adjust routing behavior, SLA targets, and escalation policies **without code changes or developer involvement**.

**Benefits:**
- ✅ **Self-Service Threshold Adjustment** - Operations teams can tune parameters independently
- ✅ **Multi-Environment Support** - Different thresholds for dev/test/prod environments  
- ✅ **Multi-Region Customization** - Region-specific rules for South Africa, Australia, US, UK
- ✅ **Gradual Rollout Control** - Feature flags enable A/B testing and phased deployment
- ✅ **Audit Trail** - Version-controlled configuration changes tracked in Git
- ✅ **Safety Validation** - Automatic bounds checking prevents invalid threshold values

### 8.2 Configuration File Locations

```
config/
├── business_rules.json              # Base configuration (applies to all environments)
├── business_rules.dev.json          # Development overrides (optional)
├── business_rules.test.json         # Test environment overrides (optional)
├── business_rules.prod.json         # Production overrides (optional)
└── regions/
    ├── business_rules.za.json       # South Africa region overrides
    ├── business_rules.au.json       # Australia region overrides
    ├── business_rules.us.json       # United States region overrides
    └── business_rules.uk.json       # United Kingdom region overrides
```

**Hierarchy:** Base config → Environment config → Region config (later values override earlier)

### 8.3 Configuration Sections Reference

| Section | Purpose | Example Keys |
|---------|---------|--------------|
| **routing_thresholds** | Confidence levels for routing decisions | `dispute_confidence_min`, `standard_confidence_min`, `hitl_trigger_threshold` |
| **department_sla_hours** | SLA targets per routing rule (R001-R015) | `R001_DISPUTE_EXPLICIT`, `R007_PASSWORD_RESET`, etc. |
| **processing_time_sla** | Stage-specific processing time limits | `triage_minutes`, `classification_minutes`, `routing_minutes` |
| **escalation_thresholds** | Age-based escalation triggers | `team_lead_days`, `production_support_days` |
| **priority_sla_response** | Priority-based response time targets | `P0_critical_hours`, `P1_high_hours`, etc. |
| **currency_settings** | Multi-region currency configurations | `default_currency`, `decimal_precision`, `region_currencies` |
| **feature_flags** | Runtime toggles for new features | `use_config_driven_thresholds`, `enable_ml_predictions` |
| **validation_rules** | Safety bounds for threshold values | `confidence_min/max`, `sla_hours_min/max` |

### 8.4 Common Configuration Changes

#### Example 1: Adjust Dispute Detection Confidence Threshold
**Business Scenario:** Reduce false positives by increasing confidence requirement from 95% to 98%

**File:** `config/business_rules.json`
```json
{
  "routing_thresholds": {
    "dispute_confidence_min": 0.98,  // Changed from 0.95
    "standard_confidence_min": 0.80,
    "hitl_trigger_threshold": 0.80
  }
}
```

**Impact:** Only disputes with ≥98% confidence will auto-route to Credit Management

#### Example 2: Reduce Password Reset SLA for Better Customer Experience
**Business Scenario:** Improve response time for password resets from 6 hours to 2 hours

**File:** `config/business_rules.json`
```json
{
  "department_sla_hours": {
    "R007_PASSWORD_RESET": 2,  // Changed from 6
    "R001_DISPUTE_EXPLICIT": 6,
    ...
  }
}
```

**Impact:** Password reset tickets now have 2-hour SLA target

#### Example 3: Environment-Specific Configuration
**Business Scenario:** Test aggressive routing thresholds in dev environment before production

**File:** `config/business_rules.dev.json`
```json
{
  "routing_thresholds": {
    "dispute_confidence_min": 0.90,  // Lower threshold for testing
    "standard_confidence_min": 0.75,
    "hitl_trigger_threshold": 0.75
  },
  "feature_flags": {
    "use_config_driven_thresholds": true,
    "enable_experimental_rules": true  // Only in dev
  }
}
```

**Impact:** Dev environment uses different thresholds than production

#### Example 4: Region-Specific Currency and SLA Adjustments
**Business Scenario:** Australia region needs faster response times due to timezone differences

**File:** `config/regions/business_rules.au.json`
```json
{
  "currency_settings": {
    "default_currency": "AUD",
    "decimal_precision": 2
  },
  "priority_sla_response": {
    "P0_critical_hours": 1,    // 1 hour (vs 1 hour globally)
    "P1_high_hours": 3,        // 3 hours (vs 6 hours globally)
    "P2_medium_hours": 12,     // 12 hours (vs 24 hours globally)
    "P3_low_hours": 24         // 24 hours (vs 36 hours globally)
  }
}
```

**Impact:** Australia region has tighter SLA targets and uses AUD currency

### 8.5 Validation and Safety Checks

All configuration changes are automatically validated against safety bounds defined in `validation_rules`:

| Parameter | Minimum | Maximum | Rationale |
|-----------|---------|---------|-----------|
| **Confidence Thresholds** | 0.50 (50%) | 1.0 (100%) | Below 50% is unreliable; 100% is maximum |
| **SLA Hours** | 1 hour | 168 hours (7 days) | Minimum responsiveness; maximum reasonable delay |
| **Processing Time** | 1 minute | 60 minutes | Minimum viable; maximum attention span |
| **Escalation Days** | 1 day | 30 days | Immediate escalation; maximum aging tolerance |

**Validation Error Example:**
```
ThresholdValidationError: Invalid threshold value for 'dispute_confidence_min': 
0.45 is below minimum allowed value of 0.5
```

### 8.6 Testing Configuration Changes

**Before Deploying to Production:**

1. **Validate JSON Syntax:**
   ```bash
   python -c "import json; print(json.load(open('config/business_rules.json')))"
   ```

2. **Run Configuration Unit Tests:**
   ```bash
   python -m pytest tests/test_business_rules_config.py -v
   ```

3. **Run Integration Tests:**
   ```bash
   python -m pytest tests/test_rules_engine_config_integration.py -v
   ```

4. **Test in Dev Environment First:**
   - Deploy changes to `config/business_rules.dev.json`
   - Validate routing behavior matches expectations
   - Monitor metrics for 24-48 hours
   - Graduate to production after validation

### 8.7 Rollback Procedure

If configuration changes cause unexpected behavior:

**Option 1: Git Rollback (Recommended)**
```bash
git checkout HEAD~1 config/business_rules.json
git commit -m "Rollback: Revert config changes due to [issue]"
```

**Option 2: Feature Flag Disable**
```json
{
  "feature_flags": {
    "use_config_driven_thresholds": false  // Revert to hard-coded defaults
  }
}
```

**Option 3: Environment Override**
Create emergency override file:
```bash
# Create emergency production override
cp config/business_rules.json.backup config/business_rules.prod.json
```

### 8.8 Configuration Change Process

**Recommended Workflow:**

1. **Identify Business Need** - Document why threshold change is needed (e.g., "too many false positives")
2. **Propose Change** - Create change request with before/after values
3. **Review Configuration Keys** - Reference section 8.3 to find correct config key
4. **Update Configuration File** - Edit appropriate JSON file (base/env/region)
5. **Validate Syntax** - Run JSON validation (section 8.6)
6. **Test in Dev** - Deploy to dev environment first
7. **Monitor Metrics** - Track impact on routing accuracy, SLA compliance
8. **Graduate to Production** - Deploy after successful dev validation
9. **Document Change** - Update this document if threshold becomes new standard

### 8.9 Support and Troubleshooting

**Common Issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Configuration not loading | JSON syntax error | Run validation command (section 8.6 step 1) |
| Changes not taking effect | Feature flag disabled | Set `use_config_driven_thresholds: true` |
| Validation error on startup | Value outside safety bounds | Check validation_rules section, adjust value |
| Environment override not working | Wrong file name | Verify file follows `business_rules.{env}.json` pattern |

**For Additional Help:**
- **Technical Issues:** Contact Development Team (dev-team@company.com)
- **Business Rule Questions:** Contact Operations Manager (ops-manager@company.com)
- **Configuration Review:** Weekly config review meeting (Fridays 2pm)

---

**Document Owner:** Customer Service Operations Manager  
**Technical Owner:** Development Team Lead  
**Review Frequency:** Monthly  
**Next Review:** October 28, 2025