# Configuration Directory

This directory contains configuration files for the Call Centre Agent system.

## Files

### User Configuration

#### `user_config.example.json` (Committed to Git)
Template configuration file showing available options and default values.

**Copy this file to create your personal configuration:**
```bash
copy user_config.example.json user_config.json
```

#### `user_config.json` (Ignored by Git)
Your personal configuration file. This file is auto-generated when you run the application and save preferences through the UI.

**This file contains:**
- LLM provider preference (Gemini, Ollama, etc.)
- Vector database preference (Pinecone, ChromaDB, etc.)
- UI preferences (theme, visualization settings)
- Debug mode settings
- Performance thresholds

**Note**: This file is excluded from version control via `.gitignore` because it contains user-specific settings.

---

### Business Rules Configuration ⚙️

#### `business_rules.json` (Committed to Git)
**NEW**: Configurable business rules for routing thresholds, SLA policies, and escalation rules.

**Key Features:**
- 🎯 **Routing Thresholds**: Confidence levels for department routing (95% for disputes, 80% standard)
- ⏱️ **SLA Policies**: Response time targets by rule ID (1-48 hours)
- 🚨 **Escalation Rules**: Age-based escalation thresholds (2 days → Team Lead, 7 days → Production Support)
- 🌍 **Multi-Region Support**: Currency settings and region-specific overrides
- 🧪 **Feature Flags**: Toggle config-driven behavior on/off
- ✅ **Validation**: Min/max bounds for all numeric thresholds

**Architecture:**
```
config/
├── business_rules.json              # Base production config
├── business_rules.dev.json          # Development overrides (optional)
├── business_rules.test.json         # Test environment (optional)
└── regions/
    ├── za.json                      # South Africa overrides
    ├── au.json                      # Australia overrides
    └── us.json                      # United States overrides
```

**Loading Hierarchy** (later overrides earlier):
1. Base: `business_rules.json`
2. Environment: `business_rules.{env}.json`
3. Region: `regions/{region}.json`

---

## Configuration Options

### User Configuration (`user_config.json`)

```json
{
  "llm_provider": "Gemini Pro (Cloud)",        // LLM service to use
  "vector_provider": "Pinecone (Cloud)",       // Vector database to use
  "show_pipeline_viz": true,                   // Show pipeline visualization
  "debug_mode": false,                         // Enable debug logging
  "ensemble_weight": 0.7,                      // Weight for ensemble routing
  "other_threshold": 0.6,                      // Threshold for "Other" category
  "auto_initialize": true,                     // Auto-initialize on startup
  "preferences": {
    "theme": "default",                        // UI theme
    "show_cost_info": true,                    // Display cost information
    "show_performance_metrics": true           // Display performance metrics
  }
}
```

---

### Business Rules Configuration (`business_rules.json`)

#### 1. Routing Thresholds
```json
{
  "routing_thresholds": {
    "credit_management_confidence": 0.95,    // High bar for dispute routing
    "standard_confidence": 0.80,             // Default for other departments
    "hitl_trigger_threshold": 0.80,          // Below this = Human review
    "dispute_detection_confidence": 0.95,    // Dispute vs inquiry detection
    "min_confidence_floor": 0.50,            // Safety minimum
    "max_confidence_ceiling": 1.00           // Safety maximum
  }
}
```

#### 2. Department SLA Hours (by Rule ID)
```json
{
  "department_sla_hours": {
    "R001_DISPUTE_EXPLICIT": 6,              // Billing disputes - urgent
    "R004_ACCOUNT_LOCKED": 2,                // Account access - critical
    "R006_SECURITY_BREACH": 1,               // Security - immediate
    "R009_BILLING_INQUIRY": 12,              // General billing - standard
    "default_sla_hours": 24                  // Fallback for unknown rules
  }
}
```

#### 3. Processing Time SLA (minutes)
```json
{
  "processing_time_sla": {
    "ai_classification_minutes": 5,          // AI processing target
    "service_desk_review_minutes": 10,       // HITL review target
    "total_routing_minutes": 15,             // End-to-end target
    "max_processing_timeout_minutes": 30     // Hard timeout
  }
}
```

#### 4. Escalation Thresholds
```json
{
  "escalation_thresholds": {
    "team_lead_age_days": 2,                 // Escalate to team lead after 2 days
    "production_support_age_days": 7,        // Escalate to support after 1 week
    "p0_warning_minutes": 30,                // P0 pre-escalation warning
    "p1_warning_hours": 4,                   // P1 pre-escalation warning
    "p2_warning_hours": 18,                  // P2 pre-escalation warning
    "p3_warning_hours": 30                   // P3 pre-escalation warning
  }
}
```

#### 5. Priority SLA Response Times
```json
{
  "priority_sla_response": {
    "P0_IMMEDIATE": {
      "response_hours": 1,                   // Critical outage - 1 hour
      "escalation_warning_minutes": 30,
      "description": "Critical outage or security incident"
    },
    "P1_HIGH": {
      "response_hours": 6,                   // High priority - same day
      "escalation_warning_hours": 4
    },
    "P2_MEDIUM": {
      "response_hours": 24,                  // Medium - next business day
      "escalation_warning_hours": 18
    },
    "P3_STANDARD": {
      "response_hours": 36,                  // Standard queue
      "escalation_warning_hours": 30
    }
  }
}
```

#### 6. Currency Settings (Multi-Region)
```json
{
  "currency_settings": {
    "default_currency": "USD",
    "default_locale": "en_US",
    "region_currencies": {
      "za": {
        "currency": "ZAR",
        "locale": "en_ZA",
        "symbol": "R",
        "description": "South Africa - Rand"
      },
      "au": {
        "currency": "AUD",
        "locale": "en_AU",
        "symbol": "$",
        "description": "Australia - Dollar"
      }
    }
  }
}
```

#### 7. Feature Flags
```json
{
  "feature_flags": {
    "use_config_driven_thresholds": true,    // Enable config-driven system
    "enable_multi_region_support": true,     // Enable region overrides
    "enable_dynamic_sla_adjustment": true,   // Enable runtime SLA changes
    "enable_ab_testing": false,              // A/B testing (experimental)
    "log_threshold_violations": true         // Log when thresholds violated
  }
}
```

---

## Python API Usage

### Loading Configuration

```python
from src.models.business_rules_config import BusinessRulesConfig

# Load production config (default)
config = BusinessRulesConfig()

# Load development config with relaxed thresholds
config = BusinessRulesConfig(environment="dev")

# Load region-specific config
config = BusinessRulesConfig(region="za")

# Load both environment and region overrides
config = BusinessRulesConfig(environment="prod", region="au")
```

### Using Configuration Values

```python
# Get confidence thresholds
standard_confidence = config.get_confidence_threshold()
dispute_confidence = config.get_confidence_threshold("credit_management")

# Get SLA hours for specific rule
sla_hours = config.get_sla_hours("R001_DISPUTE_EXPLICIT")  # Returns 6
unknown_sla = config.get_sla_hours("R999_UNKNOWN")         # Returns 24 (default)

# Get HITL threshold
hitl_threshold = config.get_hitl_threshold()  # Returns 0.80

# Get processing time targets
ai_sla = config.get_processing_time_sla("ai_classification")  # Returns 5 minutes
total_sla = config.get_processing_time_sla("total")           # Returns 15 minutes

# Get escalation thresholds
team_lead_days = config.get_escalation_threshold("team_lead")  # Returns 2 days

# Get priority SLA
p1_sla = config.get_priority_sla("P1_HIGH")
# Returns: {"response_hours": 6, "escalation_warning_hours": 4, ...}

# Get currency settings
za_currency = config.get_currency_settings("za")
# Returns: {"currency": "ZAR", "locale": "en_ZA", "symbol": "R"}

# Check feature flags
if config.is_feature_enabled("use_config_driven_thresholds"):
    # Use config values instead of hard-coded
    pass

# Get accuracy targets
dispute_accuracy = config.get_accuracy_target("dispute_detection_accuracy")  # 0.98

# Export complete config as dictionary
config_dict = config.to_dict()
```

---

## Environment-Specific Overrides

Create environment-specific config files to override base values:

### Development (`business_rules.dev.json`)
```json
{
  "routing_thresholds": {
    "standard_confidence": 0.70,             // Lower for easier testing
    "hitl_trigger_threshold": 0.70
  },
  "feature_flags": {
    "log_threshold_violations": true,        // Verbose logging in dev
    "enable_ab_testing": true                // Enable experiments
  }
}
```

### Testing (`business_rules.test.json`)
```json
{
  "processing_time_sla": {
    "max_processing_timeout_minutes": 5     // Faster timeouts for tests
  },
  "department_sla_hours": {
    "default_sla_hours": 1                  // Accelerated SLAs for testing
  }
}
```

---

## Region-Specific Overrides

Create region files in `config/regions/` to customize per geography:

### South Africa (`regions/za.json`)
```json
{
  "currency_settings": {
    "default_currency": "ZAR",
    "default_locale": "en_ZA"
  },
  "department_sla_hours": {
    "R001_DISPUTE_EXPLICIT": 8              // Longer SLA due to timezone
  }
}
```

---

## Provider Options

### LLM Providers
- `"Gemini Pro (Cloud)"` - Google's Gemini AI (requires API key)
- `"Ollama (Local)"` - Local Ollama models
- Other providers as configured

### Vector Providers
- `"Pinecone (Cloud)"` - Cloud-based vector database (requires API key)
- `"ChromaDB (Local)"` - Local vector database (no API key needed)

## Usage

The application automatically:
1. Looks for `config/user_config.json` on startup
2. Falls back to default values if not found
3. Creates the file when you save preferences through the UI

## Manual Configuration

You can manually edit `user_config.json` to set preferences before launching the application.

**Example - Use local providers:**
```json
{
  "llm_provider": "Ollama (Local)",
  "vector_provider": "ChromaDB (Local)",
  "show_pipeline_viz": true,
  "debug_mode": false
}
```

## Security Note

Never commit `user_config.json` to version control if it contains sensitive information or API keys. The file is already excluded via `.gitignore`.

## Related Files

- **Code**: `src/models/config_manager.py` - Configuration management logic
- **UI**: `src/ui/streamlit_demo.py` - Loads and saves preferences
