"""
Integration tests for BusinessRulesConfig with TelcoRulesEngine

Tests that the rules engine correctly integrates with BusinessRulesConfig
for dynamic threshold management.
"""

import pytest
import json

from src.models.rules_engine import TelcoRulesEngine
from src.models.business_rules_config import BusinessRulesConfig


class TestRulesEngineConfigIntegration:
    """Test integration between rules engine and business config."""
    
    def test_legacy_mode_without_config(self):
        """Test that rules engine works in legacy mode without config."""
        engine = TelcoRulesEngine()
        
        # Should have loaded default rules
        assert len(engine.rules) > 0
        assert engine.business_config is None
        
        # Dispute should match with hard-coded confidence
        match = engine.evaluate_ticket("I dispute this charge on my bill")
        assert match is not None
        assert match.rule_id == "R001_DISPUTE_EXPLICIT"
        assert match.confidence == 0.98  # Hard-coded default
        assert match.sla_hours == 6  # Hard-coded default
    
    def test_config_driven_mode(self, tmp_path):
        """Test rules engine with BusinessRulesConfig integration."""
        # Create test config
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        config_data = {
            "version": "1.0.0",
            "routing_thresholds": {
                "credit_management_confidence": 0.99,  # Higher than default 0.98
                "standard_confidence": 0.85
            },
            "department_sla_hours": {
                "R001_DISPUTE_EXPLICIT": 4,  # Lower than default 6
                "default_sla_hours": 24
            },
            "feature_flags": {
                "use_config_driven_thresholds": True
            },
            "validation_rules": {
                "min_confidence_threshold": 0.50,
                "max_confidence_threshold": 1.00,
                "min_sla_hours": 1,
                "max_sla_hours": 168
            }
        }
        
        with open(config_dir / "business_rules.json", 'w') as f:
            json.dump(config_data, f)
        
        # Load config and create engine
        config = BusinessRulesConfig(config_path=config_dir)
        engine = TelcoRulesEngine(business_config=config)
        
        # Verify config mode
        assert engine.business_config is not None
        
        # Find the dispute rule
        dispute_rule = next((r for r in engine.rules if r.id == "R001_DISPUTE_EXPLICIT"), None)
        assert dispute_rule is not None
        
        # Should use config values, not hard-coded defaults
        assert dispute_rule.confidence == 0.99  # From config
        assert dispute_rule.sla_hours == 4  # From config
    
    def test_feature_flag_controls_config_usage(self, tmp_path):
        """Test that feature flag controls whether config is used."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        # Config with feature flag DISABLED
        config_data = {
            "version": "1.0.0",
            "routing_thresholds": {
                "credit_management_confidence": 0.99
            },
            "department_sla_hours": {
                "R001_DISPUTE_EXPLICIT": 4
            },
            "feature_flags": {
                "use_config_driven_thresholds": False  # DISABLED
            },
            "validation_rules": {
                "min_confidence_threshold": 0.50,
                "max_confidence_threshold": 1.00,
                "min_sla_hours": 1,
                "max_sla_hours": 168
            }
        }
        
        with open(config_dir / "business_rules.json", 'w') as f:
            json.dump(config_data, f)
        
        config = BusinessRulesConfig(config_path=config_dir)
        engine = TelcoRulesEngine(business_config=config)
        
        # Find dispute rule
        dispute_rule = next((r for r in engine.rules if r.id == "R001_DISPUTE_EXPLICIT"), None)
        
        # Should use hard-coded defaults because feature flag is disabled
        assert dispute_rule.confidence == 0.98  # Hard-coded default
        assert dispute_rule.sla_hours == 6  # Hard-coded default
    
    def test_all_rules_use_config_when_available(self, tmp_path):
        """Test that all 15 rules respect configuration."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        # Config with custom SLA for all rules
        config_data = {
            "version": "1.0.0",
            "routing_thresholds": {
                "credit_management_confidence": 0.96,
                "technical_support_l2_confidence": 0.92,
                "standard_confidence": 0.85
            },
            "department_sla_hours": {
                "R001_DISPUTE_EXPLICIT": 2,
                "R002_REFUND_REQUEST": 3,
                "R003_DOUBLE_BILLING": 4,
                "R004_ACCOUNT_LOCKED": 1,
                "R005_PASSWORD_RESET": 2,
                "R006_SECURITY_BREACH": 1,  # Changed from 0.5 to meet min requirement
                "R007_SERVICE_OUTAGE": 2,
                "R008_SLOW_INTERNET": 6,
                "R009_BILLING_INQUIRY": 8,
                "R010_PAYMENT_ISSUES": 4,
                "R011_NEW_SERVICE": 12,
                "R012_UPGRADE_PLAN": 16,
                "R013_CANCELLATION": 12,
                "R014_RETENTION_RISK": 6,
                "R015_POSITIVE_FEEDBACK": 24,
                "default_sla_hours": 24
            },
            "feature_flags": {
                "use_config_driven_thresholds": True
            },
            "validation_rules": {
                "min_confidence_threshold": 0.50,
                "max_confidence_threshold": 1.00,
                "min_sla_hours": 1,
                "max_sla_hours": 168
            }
        }
        
        with open(config_dir / "business_rules.json", 'w') as f:
            json.dump(config_data, f)
        
        config = BusinessRulesConfig(config_path=config_dir)
        engine = TelcoRulesEngine(business_config=config)
        
        # Verify a sample of rules use config values
        dispute_rule = next((r for r in engine.rules if r.id == "R001_DISPUTE_EXPLICIT"), None)
        assert dispute_rule.sla_hours == 2  # From config
        
        security_rule = next((r for r in engine.rules if r.id == "R006_SECURITY_BREACH"), None)
        assert security_rule.sla_hours == 1  # From config
        
        feedback_rule = next((r for r in engine.rules if r.id == "R015_POSITIVE_FEEDBACK"), None)
        assert feedback_rule.sla_hours == 24  # From config
    
    def test_ticket_evaluation_with_config_driven_thresholds(self, tmp_path):
        """Test actual ticket evaluation uses config-driven values."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        config_data = {
            "version": "1.0.0",
            "routing_thresholds": {
                "credit_management_confidence": 0.99,
                "standard_confidence": 0.85
            },
            "department_sla_hours": {
                "R001_DISPUTE_EXPLICIT": 2,  # Urgent disputes
                "R009_BILLING_INQUIRY": 24,  # Standard billing
                "default_sla_hours": 24
            },
            "feature_flags": {
                "use_config_driven_thresholds": True
            },
            "validation_rules": {
                "min_confidence_threshold": 0.50,
                "max_confidence_threshold": 1.00,
                "min_sla_hours": 1,
                "max_sla_hours": 168
            }
        }
        
        with open(config_dir / "business_rules.json", 'w') as f:
            json.dump(config_data, f)
        
        config = BusinessRulesConfig(config_path=config_dir)
        engine = TelcoRulesEngine(business_config=config)
        
        # Test dispute ticket
        match = engine.evaluate_ticket("I strongly dispute this unauthorized charge")
        assert match is not None
        assert match.rule_id == "R001_DISPUTE_EXPLICIT"
        assert match.confidence == 0.99  # Config value
        assert match.sla_hours == 2  # Config value
        
        # Test billing inquiry
        match = engine.evaluate_ticket("Can you explain my bill breakdown?")
        assert match is not None
        assert match.rule_id == "R009_BILLING_INQUIRY"
        assert match.sla_hours == 24  # Config value
    
    def test_backward_compatibility_with_existing_code(self):
        """Test that existing code without config still works."""
        # Old way - no config parameter
        engine = TelcoRulesEngine()
        
        # Should work exactly as before
        assert len(engine.rules) == 15  # All default rules loaded
        
        # Test dispute matching
        match = engine.evaluate_ticket("I dispute this billing error")
        assert match is not None
        assert match.department == "credit_management"
        assert 0.90 <= match.confidence <= 1.0  # Within expected range
        assert match.sla_hours > 0
    
    def test_environment_specific_config(self, tmp_path):
        """Test environment-specific configuration overrides."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        # Base config
        base_config = {
            "version": "1.0.0",
            "routing_thresholds": {
                "credit_management_confidence": 0.95,
                "standard_confidence": 0.80
            },
            "department_sla_hours": {
                "R001_DISPUTE_EXPLICIT": 6,
                "default_sla_hours": 24
            },
            "feature_flags": {
                "use_config_driven_thresholds": True
            },
            "validation_rules": {
                "min_confidence_threshold": 0.50,
                "max_confidence_threshold": 1.00,
                "min_sla_hours": 1,
                "max_sla_hours": 168
            }
        }
        
        # Dev override - lower thresholds
        dev_config = {
            "routing_thresholds": {
                "credit_management_confidence": 0.85  # Lower for dev testing
            },
            "department_sla_hours": {
                "R001_DISPUTE_EXPLICIT": 1  # Faster dev testing
            }
        }
        
        with open(config_dir / "business_rules.json", 'w') as f:
            json.dump(base_config, f)
        
        with open(config_dir / "business_rules.dev.json", 'w') as f:
            json.dump(dev_config, f)
        
        # Load dev config
        config = BusinessRulesConfig(environment="dev", config_path=config_dir)
        engine = TelcoRulesEngine(business_config=config)
        
        # Should use dev overrides
        dispute_rule = next((r for r in engine.rules if r.id == "R001_DISPUTE_EXPLICIT"), None)
        assert dispute_rule.confidence == 0.85  # Dev override
        assert dispute_rule.sla_hours == 1  # Dev override
    
    def test_logging_indicates_config_mode(self, tmp_path, caplog):
        """Test that logging clearly indicates which mode is active."""
        import logging
        caplog.set_level(logging.INFO)
        
        # Legacy mode
        _ = TelcoRulesEngine()
        assert "hard-coded" in caplog.text.lower() or "legacy" in caplog.text.lower()
        
        caplog.clear()
        
        # Config mode
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        config_data = {
            "version": "1.0.0",
            "routing_thresholds": {"standard_confidence": 0.80},
            "department_sla_hours": {"default_sla_hours": 24},
            "feature_flags": {"use_config_driven_thresholds": True},
            "validation_rules": {
                "min_confidence_threshold": 0.50,
                "max_confidence_threshold": 1.00,
                "min_sla_hours": 1,
                "max_sla_hours": 168
            }
        }
        
        with open(config_dir / "business_rules.json", 'w') as f:
            json.dump(config_data, f)
        
        config = BusinessRulesConfig(config_path=config_dir)
        _ = TelcoRulesEngine(business_config=config)
        
        assert "config" in caplog.text.lower()


class TestConfigDrivenBehaviorEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_missing_rule_id_in_config_uses_default(self, tmp_path):
        """Test that missing rule IDs fall back to defaults."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        # Config missing R002 SLA
        config_data = {
            "version": "1.0.0",
            "routing_thresholds": {"credit_management_confidence": 0.95},
            "department_sla_hours": {
                "R001_DISPUTE_EXPLICIT": 4,
                # R002_REFUND_REQUEST missing
                "default_sla_hours": 24
            },
            "feature_flags": {"use_config_driven_thresholds": True},
            "validation_rules": {
                "min_confidence_threshold": 0.50,
                "max_confidence_threshold": 1.00,
                "min_sla_hours": 1,
                "max_sla_hours": 168
            }
        }
        
        with open(config_dir / "business_rules.json", 'w') as f:
            json.dump(config_data, f)
        
        config = BusinessRulesConfig(config_path=config_dir)
        engine = TelcoRulesEngine(business_config=config)
        
        # R002 should use default_sla_hours
        refund_rule = next((r for r in engine.rules if r.id == "R002_REFUND_REQUEST"), None)
        assert refund_rule.sla_hours == 24  # Default fallback
    
    def test_invalid_config_falls_back_gracefully(self, tmp_path):
        """Test graceful fallback when config is invalid."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        # Write invalid JSON
        with open(config_dir / "business_rules.json", 'w') as f:
            f.write("{invalid json")
        
        # Should load fallback config without crashing
        config = BusinessRulesConfig(config_path=config_dir)
        engine = TelcoRulesEngine(business_config=config)
        
        # Should still work with fallback config
        assert len(engine.rules) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
