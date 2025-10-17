"""
Rules Engine for Deterministic Routing
=====================================
High-confidence pattern matching for ticket routing before ML/LLM analysis.
Based on telco domain business rules and routing logic.

Now supports configuration-driven thresholds via BusinessRulesConfig for:
- Department-specific confidence thresholds
- Rule-specific SLA hours
- Dynamic threshold adjustment without code changes
"""

import re
import yaml
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import business rules configuration (optional dependency)
try:
    from .business_rules_config import BusinessRulesConfig
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    logger.warning("BusinessRulesConfig not available - using hard-coded defaults")

@dataclass
class RuleMatch:
    """Represents a matched routing rule with confidence and metadata."""
    rule_id: str
    department: str
    urgency: str
    confidence: float
    pattern_matched: str
    keywords_matched: List[str]
    reasoning: str
    sla_hours: int
    requires_escalation: bool = False

@dataclass  
class RoutingRule:
    """Individual routing rule configuration."""
    id: str
    pattern: str
    department: str
    urgency: str = "Medium"
    confidence: float = 0.90
    keywords: Optional[List[str]] = None
    regex: bool = False
    sla_hours: int = 24
    description: str = ""
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []

class TelcoRulesEngine:
    """
    Telco domain-specific rules engine for deterministic ticket routing.
    
    Implements business rules from telco-domain/business-rules/Departmental_Routing_Rules.md
    with high-confidence pattern matching for common scenarios.
    
    Now supports configuration-driven thresholds via BusinessRulesConfig:
    - Pass business_config parameter to use configurable thresholds
    - Falls back to hard-coded defaults if no config provided (backward compatible)
    """
    
    def __init__(
        self, 
        rules_config_path: Optional[str] = None,
        business_config: Optional['BusinessRulesConfig'] = None
    ):
        """
        Initialize rules engine with telco domain rules.
        
        Args:
            rules_config_path: Optional path to YAML rules configuration
            business_config: Optional BusinessRulesConfig for dynamic thresholds
        """
        self.rules: List[RoutingRule] = []
        self.business_config = business_config
        self.rule_stats = {
            "total_evaluations": 0,
            "total_matches": 0,
            "matches_by_rule": {},
            "confidence_distribution": {"high": 0, "medium": 0, "low": 0}
        }
        
        # Log configuration mode
        if self.business_config:
            logger.info("TelcoRulesEngine initialized with BusinessRulesConfig (config-driven mode)")
        else:
            logger.info("TelcoRulesEngine initialized with hard-coded defaults (legacy mode)")
        
        if rules_config_path:
            self.load_rules_from_yaml(rules_config_path)
        else:
            self._load_default_telco_rules()
    
    def _get_sla_hours(self, rule_id: str, default: int = 24) -> int:
        """
        Get SLA hours for rule from config or use default.
        
        Args:
            rule_id: Rule identifier (e.g., 'R001_DISPUTE_EXPLICIT')
            default: Fallback SLA hours if config not available
            
        Returns:
            SLA hours (integer)
        """
        if self.business_config and self.business_config.is_feature_enabled("use_config_driven_thresholds"):
            return self.business_config.get_sla_hours(rule_id)
        return default
    
    def _get_confidence(self, rule_id: str, department: str, default: float) -> float:
        """
        Get confidence threshold from config or use default.
        
        Args:
            rule_id: Rule identifier
            department: Department name (credit_management, billing_team, etc.)
            default: Fallback confidence value
            
        Returns:
            Confidence threshold (0.0 - 1.0)
        """
        if self.business_config and self.business_config.is_feature_enabled("use_config_driven_thresholds"):
            return self.business_config.get_confidence_threshold(department)
        return default
    
    def _load_default_telco_rules(self):
        """Load default telco domain routing rules based on business requirements."""
        
        # High-confidence dispute detection rules
        dispute_rules = [
            RoutingRule(
                id="R001_DISPUTE_EXPLICIT",
                pattern=r"dispute|disagree with.*charge|incorrect.*billing|unauthorized.*charge",
                department="credit_management",
                urgency="High",
                confidence=self._get_confidence("R001_DISPUTE_EXPLICIT", "credit_management", 0.98),
                regex=True,
                sla_hours=self._get_sla_hours("R001_DISPUTE_EXPLICIT", 6),
                description="Explicit dispute language - route to Credit Management"
            ),
            RoutingRule(
                id="R002_REFUND_REQUEST",
                pattern=r"refund|credit.*account|remove.*charge|billing.*error",
                department="credit_management", 
                urgency="High",
                confidence=self._get_confidence("R002_REFUND_REQUEST", "credit_management", 0.95),
                regex=True,
                sla_hours=self._get_sla_hours("R002_REFUND_REQUEST", 6),
                description="Refund requests - Credit Management priority"
            ),
            RoutingRule(
                id="R003_DOUBLE_BILLING",
                pattern=r"charged.*twice|double.*billing|duplicate.*charge",
                department="credit_management",
                urgency="High", 
                confidence=self._get_confidence("R003_DOUBLE_BILLING", "credit_management", 0.97),
                regex=True,
                sla_hours=self._get_sla_hours("R003_DOUBLE_BILLING", 6),
                description="Double billing issues - immediate investigation required"
            )
        ]
        
        # Security and account access rules
        security_rules = [
            RoutingRule(
                id="R004_ACCOUNT_LOCKED",
                pattern=r"account.*locked|cannot.*login|access.*denied|locked.*out",
                department="technical_support_l2",
                urgency="High",
                confidence=self._get_confidence("R004_ACCOUNT_LOCKED", "technical_support_l2", 0.99),
                regex=True,
                sla_hours=self._get_sla_hours("R004_ACCOUNT_LOCKED", 2),
                description="Account access issues - high priority technical support"
            ),
            RoutingRule(
                id="R005_PASSWORD_RESET",
                pattern=r"password.*reset|forgot.*password|password.*not.*working",
                department="technical_support_l1",
                urgency="Medium",
                confidence=self._get_confidence("R005_PASSWORD_RESET", "technical_support_l1", 0.92),
                regex=True,
                sla_hours=self._get_sla_hours("R005_PASSWORD_RESET", 4),
                description="Password reset requests - L1 technical support"
            ),
            RoutingRule(
                id="R006_SECURITY_BREACH",
                pattern=r"security.*breach|unauthorized.*access|account.*compromised|fraud.*alert",
                department="security_team",
                urgency="Critical",
                confidence=self._get_confidence("R006_SECURITY_BREACH", "security_team", 0.98),
                regex=True,
                sla_hours=self._get_sla_hours("R006_SECURITY_BREACH", 1),
                description="Security incidents - immediate security team response"
            )
        ]
        
        # Service and technical issues
        technical_rules = [
            RoutingRule(
                id="R007_SERVICE_OUTAGE", 
                pattern=r"service.*down|outage|cannot.*connect|no.*internet|network.*issue",
                department="technical_support_l2",
                urgency="High",
                confidence=self._get_confidence("R007_SERVICE_OUTAGE", "technical_support_l2", 0.94),
                regex=True,
                sla_hours=self._get_sla_hours("R007_SERVICE_OUTAGE", 4),
                description="Service outage reports - L2 technical investigation"
            ),
            RoutingRule(
                id="R008_SLOW_INTERNET",
                pattern=r"slow.*internet|connection.*slow|speed.*issue|bandwidth.*problem",
                department="technical_support_l1",
                urgency="Medium",
                confidence=self._get_confidence("R008_SLOW_INTERNET", "technical_support_l1", 0.89),
                regex=True,
                sla_hours=self._get_sla_hours("R008_SLOW_INTERNET", 8),
                description="Performance issues - L1 technical diagnostics"
            )
        ]
        
        # Billing and account management
        billing_rules = [
            RoutingRule(
                id="R009_BILLING_INQUIRY",
                pattern=r"explain.*bill|billing.*question|understand.*charges|bill.*breakdown",
                department="billing_team",
                urgency="Medium",
                confidence=self._get_confidence("R009_BILLING_INQUIRY", "billing_team", 0.87),
                regex=True,
                sla_hours=self._get_sla_hours("R009_BILLING_INQUIRY", 12),
                description="General billing inquiries - billing team explanation"
            ),
            RoutingRule(
                id="R010_PAYMENT_ISSUES",
                pattern=r"payment.*failed|card.*declined|payment.*problem|cannot.*pay",
                keywords=["payment", "failed", "card", "declined", "pay"],
                department="billing_team",
                urgency="Medium",
                confidence=self._get_confidence("R010_PAYMENT_ISSUES", "billing_team", 0.91),
                regex=True,
                sla_hours=self._get_sla_hours("R010_PAYMENT_ISSUES", 8),
                description="Payment processing issues - billing team resolution"
            )
        ]
        
        # Service orders and changes
        order_rules = [
            RoutingRule(
                id="R011_NEW_SERVICE",
                pattern=r"new.*service|install.*internet|setup.*account|activate.*service",
                department="order_management",
                urgency="Medium",
                confidence=self._get_confidence("R011_NEW_SERVICE", "order_management", 0.93),
                regex=True,
                sla_hours=self._get_sla_hours("R011_NEW_SERVICE", 24),
                description="New service orders - order management processing"
            ),
            RoutingRule(
                id="R012_UPGRADE_PLAN",
                pattern=r"upgrade.*plan|change.*plan|faster.*internet|higher.*speed",
                department="order_management",
                urgency="Low",
                confidence=self._get_confidence("R012_UPGRADE_PLAN", "order_management", 0.88),
                regex=True,
                sla_hours=self._get_sla_hours("R012_UPGRADE_PLAN", 24),
                description="Plan changes and upgrades - order management"
            )
        ]
        
        # Customer satisfaction and retention
        crm_rules = [
            RoutingRule(
                id="R013_CANCELLATION",
                pattern=r"cancel.*service|thinking.*leaving|switch.*provider|poor.*service",
                department="crm_team",
                urgency="High",
                confidence=self._get_confidence("R013_CANCELLATION", "crm_team", 0.91),
                regex=True,
                sla_hours=self._get_sla_hours("R013_CANCELLATION", 24),
                description="Cancellation request - CRM team engagement required"
            ),
            RoutingRule(
                id="R014_RETENTION_RISK",
                pattern=r"retention|churn.*risk|considering.*switching",
                department="crm_team",
                urgency="High",
                confidence=self._get_confidence("R014_RETENTION_RISK", "crm_team", 0.91),
                regex=True,
                sla_hours=self._get_sla_hours("R014_RETENTION_RISK", 12),
                description="Retention risk - CRM team engagement required"
            ),
            RoutingRule(
                id="R015_POSITIVE_FEEDBACK",
                pattern=r"thank.*you|excellent.*service|great.*support|satisfied.*service",
                department="crm_team",
                urgency="Low",
                confidence=self._get_confidence("R015_POSITIVE_FEEDBACK", "crm_team", 0.85),
                regex=True,
                sla_hours=self._get_sla_hours("R015_POSITIVE_FEEDBACK", 48),
                description="Positive feedback - CRM team relationship management"
            )
        ]
        
        # Combine all rules
        self.rules = (dispute_rules + security_rules + technical_rules + 
                     billing_rules + order_rules + crm_rules)
        
        config_mode = "config-driven" if self.business_config else "hard-coded"
        logger.info(f"Loaded {len(self.rules)} default telco routing rules ({config_mode} mode)")
    
    def load_rules_from_yaml(self, file_path: str):
        """Load routing rules from YAML configuration file."""
        try:
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)
            
            self.rules = []
            for rule_data in config.get('rules', []):
                rule = RoutingRule(**rule_data)
                self.rules.append(rule)
            
            logger.info(f"Loaded {len(self.rules)} rules from {file_path}")
        except Exception as e:
            logger.error(f"Failed to load rules from {file_path}: {e}")
            self._load_default_telco_rules()
    
    def evaluate_ticket(self, ticket_text: str, metadata: Dict = None) -> Optional[RuleMatch]:
        """
        Evaluate ticket against all rules and return best match.
        
        Args:
            ticket_text: The ticket content to analyze
            metadata: Additional ticket metadata (priority, category, etc.)
            
        Returns:
            RuleMatch if a high-confidence rule matches, None otherwise
        """
        self.rule_stats["total_evaluations"] += 1
        
        best_match = None
        highest_confidence = 0.0
        
        ticket_lower = ticket_text.lower()
        
        for rule in self.rules:
            match_confidence = 0.0
            matched_keywords = []
            
            # Pattern matching (regex or simple string)
            if rule.regex:
                if re.search(rule.pattern, ticket_lower, re.IGNORECASE):
                    match_confidence = rule.confidence
            else:
                if rule.pattern.lower() in ticket_lower:
                    match_confidence = rule.confidence
            
            # Keyword boosting
            if rule.keywords and match_confidence > 0:
                keyword_matches = sum(1 for kw in rule.keywords if kw.lower() in ticket_lower)
                if keyword_matches > 0:
                    matched_keywords = [kw for kw in rule.keywords if kw.lower() in ticket_lower]
                    # Boost confidence by 1% per matched keyword (max 5% boost)
                    match_confidence = min(0.99, match_confidence + (keyword_matches * 0.01))
            
            # Check if this is the best match so far
            if match_confidence > highest_confidence and match_confidence >= 0.85:  # Minimum threshold
                highest_confidence = match_confidence
                
                best_match = RuleMatch(
                    rule_id=rule.id,
                    department=rule.department,
                    urgency=rule.urgency,
                    confidence=match_confidence,
                    pattern_matched=rule.pattern,
                    keywords_matched=matched_keywords,
                    reasoning=f"Rule {rule.id}: {rule.description}",
                    sla_hours=rule.sla_hours,
                    requires_escalation=(rule.urgency in ["Critical", "High"])
                )
        
        # Update statistics
        if best_match:
            self.rule_stats["total_matches"] += 1
            self.rule_stats["matches_by_rule"][best_match.rule_id] = \
                self.rule_stats["matches_by_rule"].get(best_match.rule_id, 0) + 1
            
            # Update confidence distribution
            if best_match.confidence >= 0.95:
                self.rule_stats["confidence_distribution"]["high"] += 1
            elif best_match.confidence >= 0.85:
                self.rule_stats["confidence_distribution"]["medium"] += 1
            else:
                self.rule_stats["confidence_distribution"]["low"] += 1
        
        return best_match
    
    def get_rule_statistics(self) -> Dict:
        """Get rules engine performance statistics."""
        total_evals = self.rule_stats["total_evaluations"]
        total_matches = self.rule_stats["total_matches"]
        
        return {
            "total_evaluations": total_evals,
            "total_matches": total_matches, 
            "match_rate": total_matches / max(total_evals, 1),
            "matches_by_rule": self.rule_stats["matches_by_rule"],
            "confidence_distribution": self.rule_stats["confidence_distribution"],
            "rules_loaded": len(self.rules)
        }
    
    def get_rule_coverage(self) -> Dict:
        """Analyze rule coverage by department and urgency."""
        departments = {}
        urgency_levels = {}
        
        for rule in self.rules:
            dept = rule.department
            urgency = rule.urgency
            
            departments[dept] = departments.get(dept, 0) + 1
            urgency_levels[urgency] = urgency_levels.get(urgency, 0) + 1
        
        return {
            "departments": departments,
            "urgency_levels": urgency_levels,
            "total_rules": len(self.rules)
        }

def create_sample_rules_yaml() -> str:
    """Create a sample YAML configuration for rules."""
    sample_config = """
rules:
  - id: "R001_EXPLICIT_DISPUTE"
    pattern: "dispute|incorrect.*billing|unauthorized.*charge"
    regex: true
    department: "credit_management"
    urgency: "High"
    confidence: 0.98
    sla_hours: 6
    keywords: ["refund", "error", "wrong"]
    description: "Explicit dispute language requiring investigation"
    
  - id: "R002_ACCOUNT_ACCESS"
    pattern: "account.*locked|cannot.*login"
    regex: true
    department: "technical_support_l2"
    urgency: "High"
    confidence: 0.99
    sla_hours: 2
    description: "Account access issues requiring immediate attention"
    
  - id: "R003_SERVICE_OUTAGE"
    pattern: "service.*down|no.*internet|outage"
    regex: true
    department: "technical_support_l2"
    urgency: "High"
    confidence: 0.94
    sla_hours: 4
    description: "Service outage requiring technical investigation"
"""
    return sample_config

# Example usage and testing
if __name__ == "__main__":
    # Initialize rules engine
    engine = TelcoRulesEngine()
    
    # Test cases
    test_tickets = [
        "I dispute this charge on my bill, it's completely wrong!",
        "My account is locked and I cannot login to the portal",
        "The internet service is down in my area, no connection",
        "Can you please explain why my bill is higher this month?",
        "I want to upgrade my internet plan to faster speed",
        "Thank you for the excellent customer service today"
    ]
    
    print("🔧 TELCO RULES ENGINE DEMO")
    print("=" * 50)
    
    for i, ticket in enumerate(test_tickets, 1):
        print(f"\n📧 Test Ticket {i}: {ticket}")
        
        match = engine.evaluate_ticket(ticket)
        if match:
            print(f"✅ RULE MATCH: {match.rule_id}")
            print(f"   📍 Department: {match.department}")
            print(f"   🚨 Urgency: {match.urgency}")
            print(f"   📊 Confidence: {match.confidence:.1%}")
            print(f"   ⏰ SLA: {match.sla_hours}h")
            print(f"   💡 Reasoning: {match.reasoning}")
        else:
            print("❌ No rule match - would proceed to Vector DB + ML/LLM")
    
    # Show statistics
    stats = engine.get_rule_statistics()
    coverage = engine.get_rule_coverage()
    
    print("\n📊 RULES ENGINE STATISTICS")
    print("=" * 50)
    print(f"Total Evaluations: {stats['total_evaluations']}")
    print(f"Total Matches: {stats['total_matches']}")
    print(f"Match Rate: {stats['match_rate']:.1%}")
    print(f"Rules Loaded: {stats['rules_loaded']}")
    
    print("\n🏢 DEPARTMENT COVERAGE:")
    for dept, count in coverage['departments'].items():
        print(f"   {dept}: {count} rules")
    
    print("\n🚨 URGENCY DISTRIBUTION:")
    for urgency, count in coverage['urgency_levels'].items():
        print(f"   {urgency}: {count} rules")