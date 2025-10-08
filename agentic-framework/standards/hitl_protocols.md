# Human-in-the-Loop (HITL) Protocols for Agentic Framework

## 🧑‍💻 Overview

This document defines the mandatory Human-in-the-Loop protocols for the agentic framework, ensuring proper oversight and control in all AI-assisted development workflows.

## 🎯 HITL Mode Types

### STEPWISE Mode
```yaml
description: "Human approval required at every major phase"
checkpoint_frequency: "Before each significant action"
automation_level: "Minimal - Heavy human oversight"
use_cases: ["Critical production changes", "Architecture decisions", "New feature development"]
```

### AUTONOMOUS Mode  
```yaml
description: "AI proceeds with minimal human intervention"
checkpoint_frequency: "Major milestones only"
automation_level: "High - Light human oversight"
use_cases: ["Routine maintenance", "Documentation updates", "Bug fixes"]
```

### HYBRID Mode
```yaml
description: "Mixed approach based on risk assessment"
checkpoint_frequency: "Risk-based checkpoints"
automation_level: "Medium - Balanced oversight"
use_cases: ["Refactoring", "Testing", "Code optimization"]
```

### STANDARD Mode
```yaml
description: "Default balanced approach"
checkpoint_frequency: "Standard development gates"
automation_level: "Medium - Standard oversight"
use_cases: ["General development", "Feature implementation"]
```

## 🚦 STEPWISE Mode Enforcement Protocol

### Phase Gates (All require explicit human approval)

#### 1. Requirements & Analysis Phase
```yaml
trigger: "Before any requirements analysis begins"
required_deliverables:
  - Problem statement confirmation
  - Scope boundaries definition
  - Success criteria establishment
approval_format: "PROCEED | MODIFY [reason] | REJECT [reason]"
```

#### 2. Architecture & Design Phase  
```yaml
trigger: "Before architectural decisions are made"
required_deliverables:
  - System architecture proposal
  - Technology stack recommendations
  - Risk assessment matrix
approval_format: "PROCEED | MODIFY [reason] | REJECT [reason]"
```

#### 3. Implementation Phase
```yaml
trigger: "Before code generation begins"
required_deliverables:
  - Implementation plan breakdown
  - File structure proposal
  - Integration strategy
approval_format: "PROCEED | MODIFY [reason] | REJECT [reason]"
```

#### 4. Testing & Validation Phase
```yaml
trigger: "Before testing protocols are executed"
required_deliverables:
  - Test strategy proposal
  - Coverage requirements
  - Validation criteria
approval_format: "PROCEED | MODIFY [reason] | REJECT [reason]"
```

#### 5. Documentation & Delivery Phase
```yaml
trigger: "Before final documentation and handover"
required_deliverables:
  - Documentation completeness check
  - Deployment readiness assessment
  - Knowledge transfer plan
approval_format: "PROCEED | MODIFY [reason] | REJECT [reason]"
```

## 📋 Checkpoint Display Format

### Standard Checkpoint Template
```yaml
🧑‍✈️ Master Orchestrator - STEPWISE MODE
📍 Current Phase: [PHASE_NAME]
🎯 Next Action: [SPECIFIC_ACTION_DESCRIPTION]
📊 Progress: [X/Y phases complete]
⏸️  Status: AWAITING HUMAN APPROVAL

Proposed Action Details:
- Agent: [agent_persona]
- Deliverables: [specific_outputs]
- Risk Level: [LOW|MEDIUM|HIGH]
- Estimated Duration: [time_estimate]

Options:
- PROCEED: Continue with proposed action
- MODIFY: Request changes (specify requirements)
- REJECT: Cancel this action
- PAUSE: Temporarily halt for review

Type your response:
```

### Decision Logging Format
```yaml
timestamp: [ISO_8601_TIMESTAMP]
phase: [PHASE_NAME]
action_proposed: [ACTION_DESCRIPTION]
human_decision: [PROCEED|MODIFY|REJECT|PAUSE]
human_feedback: [OPTIONAL_HUMAN_COMMENTS]
agent_response: [AGENT_ACKNOWLEDGMENT]
next_checkpoint: [NEXT_PHASE_NAME]
```

## 🔍 Audit Trail Requirements

### Mandatory Logging Points
1. **Phase Initiation**: Log when each phase begins
2. **Human Decisions**: Record all approval/rejection decisions  
3. **Modification Requests**: Track changes requested by humans
4. **Completion Status**: Mark phase completion with timestamps
5. **Error Handling**: Log any workflow deviations or errors

### Audit Trail Storage
```yaml
location: "agentic-framework/audit-logs/[PROJECT_NAME]/[SESSION_ID].jsonl"
format: "JSON Lines (one decision per line)"
retention: "90 days minimum"
access_control: "Human oversight required for audit log access"
```

## ⚡ Implementation Rules

### For AI Assistants
1. **Never skip checkpoints** in STEPWISE mode
2. **Always display current phase** and next action
3. **Wait for explicit approval** before proceeding
4. **Log all decisions** to audit trail
5. **Provide clear options** (PROCEED/MODIFY/REJECT/PAUSE)

### For Master Agent
1. **Enforce mode compliance** across all sub-agents
2. **Validate checkpoint completion** before phase transitions
3. **Maintain context** across checkpoint boundaries
4. **Handle mode switching** when requested by humans
5. **Generate audit reports** on demand

### For Sub-Agents
1. **Report to Master Agent** before major actions
2. **Respect HITL boundaries** defined by current mode
3. **Provide detailed proposals** at checkpoints
4. **Accept human modifications** gracefully
5. **Update progress tracking** after each action

## 🛡️ Error Handling & Recovery

### Checkpoint Violations
```yaml
violation: "Proceeding without approval"
response: "Immediate halt and rollback to last approved state"
escalation: "Log violation and require explicit human re-authorization"
```

### Mode Confusion
```yaml
violation: "Operating in wrong HITL mode"
response: "Stop current action and request mode clarification"
escalation: "Reset to STEPWISE mode as safe default"
```

### Communication Failures
```yaml
violation: "Human approval timeout or unclear response"
response: "Halt and request clarification"
escalation: "Default to most restrictive option (REJECT/PAUSE)"
```

## 📊 Success Metrics

### STEPWISE Mode Effectiveness
- **Checkpoint Compliance**: 100% adherence to approval gates
- **Human Satisfaction**: Post-project approval rating
- **Decision Quality**: Reduced rework and scope creep
- **Audit Completeness**: Full decision trail maintained

### Mode Performance Comparison
- **Time to Completion**: By mode type
- **Error Rates**: Human intervention requirements
- **Satisfaction Scores**: Human feedback by mode
- **Rework Frequency**: Changes after completion

---

## 🔧 Integration Points

This protocol integrates with:
- `agentic-framework/master-agent.md` - Central orchestration
- `agentic-framework/sub-agents/` - All specialized agents
- `telco-domain/project-context.md` - Project-specific requirements
- Git workflow enforcement - Branch protection rules

**Version**: 1.0  
**Created**: October 9, 2025  
**Last Updated**: October 9, 2025  
**Review Cycle**: Monthly or after significant workflow changes