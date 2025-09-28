# Departmental Routing & Escalation Rules

**Version:** 1.0  
**Effective Date:** September 28, 2025  
**Department:** Customer Service Operations  

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
- **Dispute Detection**: ≥ 98% accuracy
- **Department Routing**: ≥ 95% accuracy overall
- **False Positive Rate**: < 2% for disputes
- **Internal Transfers**: < 5% between departments

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
**Document Owner:** Customer Service Operations Manager  
**Review Frequency:** Monthly  
**Next Review:** October 28, 2025  