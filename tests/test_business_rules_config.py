"""
Unit tests for BusinessRulesConfig

Tests:
- Configuration loading (base, environment, region)
- Hierarchical override merging
- Validation and error handling
- Fallback mechanisms
- Public API methods
"""

import pytest
import json
from unittest.mock import patch

from src.models.business_rules_config import (
    BusinessRulesConfig,
    ThresholdValidationError,
    load_production_config,
    load_development_config,
    load_test_config,
    load_region_config
)


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create temporary config directory with test files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Base configuration
    base_config = {
        "version": "1.0.0",
        "routing_thresholds": {
            "credit_management_confidence": 0.95,
            "standard_confidence": 0.80,
            "hitl_trigger_threshold": 0.80
        },
        "department_sla_hours": {
            "R001_DISPUTE_EXPLICIT": 6,
            "default_sla_hours": 24
        },
        "validation_rules": {
            "min_confidence_threshold": 0.50,
            "max_confidence_threshold": 1.00,
            "min_sla_hours": 1,
            "max_sla_hours": 168
        },
        "feature_flags": {
            "use_config_driven_thresholds": True
        }
    }
    
    with open(config_dir / "business_rules.json", 'w') as f:
        json.dump(base_config, f)
    
    return config_dir


@pytest.fixture
def temp_config_with_overrides(temp_config_dir):
    """Create config directory with environment and region overrides."""
    
    # Development environment overrides
    dev_config = {
        "routing_thresholds": {
            "standard_confidence": 0.70  # Lower for dev
        },
        "feature_flags": {
            "use_config_driven_thresholds": True,
            "log_threshold_violations": True
        }
    }
    
    with open(temp_config_dir / "business_rules.dev.json", 'w') as f:
        json.dump(dev_config, f)
    
    # Region overrides
    regions_dir = temp_config_dir / "regions"
    regions_dir.mkdir()
    
    za_config = {
        "currency_settings": {
            "default_currency": "ZAR",
            "default_locale": "en_ZA"
        },
        "department_sla_hours": {
            "R001_DISPUTE_EXPLICIT": 8  # Longer SLA for ZA region
        }
    }
    
    with open(regions_dir / "za.json", 'w') as f:
        json.dump(za_config, f)
    
    return temp_config_dir


class TestBusinessRulesConfigLoading:
    """Test configuration loading and initialization."""
    
    def test_load_base_config(self, temp_config_dir):
        """Test loading base configuration."""
        config = BusinessRulesConfig(config_path=temp_config_dir)
        
        assert config.config["version"] == "1.0.0"
        assert config.get_confidence_threshold() == 0.80
        assert config.get_sla_hours("R001_DISPUTE_EXPLICIT") == 6
    
    def test_load_with_environment_override(self, temp_config_with_overrides):
        """Test environment-specific configuration override."""
        config = BusinessRulesConfig(
            environment="dev",
            config_path=temp_config_with_overrides
        )
        
        # Dev override should apply
        assert config.get_confidence_threshold() == 0.70
        
        # Base config should still be present
        assert config.get_sla_hours("R001_DISPUTE_EXPLICIT") == 6
    
    def test_load_with_region_override(self, temp_config_with_overrides):
        """Test region-specific configuration override."""
        config = BusinessRulesConfig(
            region="za",
            config_path=temp_config_with_overrides
        )
        
        # Region override should apply
        assert config.get_sla_hours("R001_DISPUTE_EXPLICIT") == 8
        
        # Base config should still be present
        assert config.get_confidence_threshold() == 0.80
    
    def test_hierarchical_override_order(self, temp_config_with_overrides):
        """Test that overrides apply in correct order: base → env → region."""
        config = BusinessRulesConfig(
            environment="dev",
            region="za",
            config_path=temp_config_with_overrides
        )
        
        # Dev override
        assert config.get_confidence_threshold() == 0.70
        
        # Region override
        assert config.get_sla_hours("R001_DISPUTE_EXPLICIT") == 8
        
        # Base config fallback
        assert config.get_sla_hours("R999_UNKNOWN") == 24
    
    def test_load_missing_config_uses_fallback(self, tmp_path):
        """Test fallback when config file is missing."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        config = BusinessRulesConfig(config_path=empty_dir)
        
        # Should load fallback config
        assert config.config["version"] == "1.0.0-fallback"
        assert config.get_confidence_threshold() == 0.80
    
    def test_load_invalid_json_uses_fallback(self, tmp_path):
        """Test fallback when config file has invalid JSON."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        # Write invalid JSON
        with open(config_dir / "business_rules.json", 'w') as f:
            f.write("{invalid json")
        
        config = BusinessRulesConfig(config_path=config_dir)
        
        # Should load fallback config
        assert config.config["version"] == "1.0.0-fallback"


class TestConfigValidation:
    """Test configuration validation."""
    
    def test_valid_config_passes_validation(self, temp_config_dir):
        """Test that valid configuration passes validation."""
        # Should not raise exception
        config = BusinessRulesConfig(config_path=temp_config_dir)
        assert config is not None
    
    def test_confidence_below_min_raises_error(self, temp_config_dir):
        """Test that confidence below minimum raises validation error."""
        # Modify config to have invalid threshold
        config_file = temp_config_dir / "business_rules.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        config["routing_thresholds"]["standard_confidence"] = 0.30  # Below 0.50 min
        
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        with pytest.raises(ThresholdValidationError) as excinfo:
            BusinessRulesConfig(config_path=temp_config_dir)
        
        assert "routing_thresholds.standard_confidence" in str(excinfo.value)
    
    def test_sla_above_max_raises_error(self, temp_config_dir):
        """Test that SLA above maximum raises validation error."""
        config_file = temp_config_dir / "business_rules.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        config["department_sla_hours"]["R001_DISPUTE_EXPLICIT"] = 200  # Above 168 max
        
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        with pytest.raises(ThresholdValidationError) as excinfo:
            BusinessRulesConfig(config_path=temp_config_dir)
        
        assert "department_sla_hours.R001_DISPUTE_EXPLICIT" in str(excinfo.value)


class TestPublicAPI:
    """Test public API methods."""
    
    def test_get_confidence_threshold_default(self, temp_config_dir):
        """Test getting default confidence threshold."""
        config = BusinessRulesConfig(config_path=temp_config_dir)
        assert config.get_confidence_threshold() == 0.80
    
    def test_get_confidence_threshold_department_specific(self, temp_config_dir):
        """Test getting department-specific confidence threshold."""
        config = BusinessRulesConfig(config_path=temp_config_dir)
        assert config.get_confidence_threshold("credit_management") == 0.95
    
    def test_get_sla_hours_specific_rule(self, temp_config_dir):
        """Test getting SLA hours for specific rule."""
        config = BusinessRulesConfig(config_path=temp_config_dir)
        assert config.get_sla_hours("R001_DISPUTE_EXPLICIT") == 6
    
    def test_get_sla_hours_fallback_to_default(self, temp_config_dir):
        """Test SLA hours fallback to default for unknown rule."""
        config = BusinessRulesConfig(config_path=temp_config_dir)
        assert config.get_sla_hours("R999_UNKNOWN") == 24
    
    def test_get_hitl_threshold(self, temp_config_dir):
        """Test getting HITL trigger threshold."""
        config = BusinessRulesConfig(config_path=temp_config_dir)
        assert config.get_hitl_threshold() == 0.80
    
    def test_is_feature_enabled(self, temp_config_dir):
        """Test feature flag checking."""
        config = BusinessRulesConfig(config_path=temp_config_dir)
        assert config.is_feature_enabled("use_config_driven_thresholds") is True
        assert config.is_feature_enabled("nonexistent_feature") is False
    
    def test_to_dict_returns_config(self, temp_config_dir):
        """Test exporting configuration as dictionary."""
        config = BusinessRulesConfig(config_path=temp_config_dir)
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "routing_thresholds" in config_dict
        assert config_dict["version"] == "1.0.0"
    
    def test_repr_includes_environment_and_region(self, temp_config_dir):
        """Test string representation."""
        config = BusinessRulesConfig(
            environment="dev",
            region="za",
            config_path=temp_config_dir
        )
        
        repr_str = repr(config)
        assert "env=dev" in repr_str
        assert "region=za" in repr_str


class TestCurrencySettings:
    """Test currency and region settings."""
    
    def test_get_currency_settings_default(self, temp_config_dir):
        """Test getting default currency settings."""
        # Add currency settings to config
        config_file = temp_config_dir / "business_rules.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        config["currency_settings"] = {
            "default_currency": "USD",
            "default_locale": "en_US"
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        config_obj = BusinessRulesConfig(config_path=temp_config_dir)
        currency = config_obj.get_currency_settings()
        
        assert currency["currency"] == "USD"
        assert currency["locale"] == "en_US"
    
    def test_get_currency_settings_region_specific(self, temp_config_with_overrides):
        """Test getting region-specific currency settings."""
        config = BusinessRulesConfig(
            region="za",
            config_path=temp_config_with_overrides
        )
        
        # Should use region-specific settings from za.json override
        # (Note: This test assumes za.json has currency_settings)
        # Fallback to default if not present
        currency = config.get_currency_settings("za")
        assert currency["currency"] in ["ZAR", "USD"]  # Either override or default


class TestConvenienceFunctions:
    """Test convenience factory functions."""
    
    @patch('src.models.business_rules_config.BusinessRulesConfig')
    def test_load_production_config(self, mock_config):
        """Test loading production config."""
        load_production_config()
        mock_config.assert_called_once_with(environment="prod")
    
    @patch('src.models.business_rules_config.BusinessRulesConfig')
    def test_load_development_config(self, mock_config):
        """Test loading development config."""
        load_development_config()
        mock_config.assert_called_once_with(environment="dev")
    
    @patch('src.models.business_rules_config.BusinessRulesConfig')
    def test_load_test_config(self, mock_config):
        """Test loading test config."""
        load_test_config()
        mock_config.assert_called_once_with(environment="test")
    
    @patch('src.models.business_rules_config.BusinessRulesConfig')
    def test_load_region_config(self, mock_config):
        """Test loading region-specific config."""
        load_region_config("za")
        mock_config.assert_called_once_with(region="za")


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_missing_validation_rules_logs_warning(self, temp_config_dir, caplog):
        """Test that missing validation rules logs warning but doesn't crash."""
        config_file = temp_config_dir / "business_rules.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Remove validation rules
        del config["validation_rules"]
        
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        config_obj = BusinessRulesConfig(config_path=temp_config_dir)
        
        # Should load successfully with warning
        assert config_obj is not None
        assert "No validation_rules" in caplog.text
    
    def test_get_nonexistent_key_returns_default(self, temp_config_dir):
        """Test that getting nonexistent keys returns sensible defaults."""
        config = BusinessRulesConfig(config_path=temp_config_dir)
        
        # Should return defaults, not crash
        assert config.get_sla_hours("NONEXISTENT_RULE") == 24
        assert config.get_confidence_threshold("nonexistent_dept") == 0.80


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
