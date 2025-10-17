"""
Business Rules Configuration Management

Provides hierarchical configuration loading for business rules thresholds,
SLA times, escalation policies, and multi-region support.

Architecture:
- Hierarchical config loading (default → environment → region)
- Schema validation with safety bounds
- Graceful fallback to defaults on errors
- Audit trail for configuration changes

Usage:
    # Load default production config
    config = BusinessRulesConfig()
    
    # Load environment-specific config
    config = BusinessRulesConfig(environment="dev")
    
    # Load region-specific overrides
    config = BusinessRulesConfig(region="za")
    
    # Get configuration values
    confidence = config.get_confidence_threshold("credit_management")
    sla_hours = config.get_sla_hours("R001_DISPUTE_EXPLICIT")
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ThresholdValidationError(Exception):
    """Raised when configuration threshold violates validation rules."""
    key: str
    value: Any
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    
    def __str__(self):
        return (f"Invalid threshold for '{self.key}': {self.value} "
                f"(allowed range: {self.min_value} - {self.max_value})")


class BusinessRulesConfig:
    """
    Configuration manager for business rules thresholds and policies.
    
    Supports hierarchical configuration loading with validation and fallback:
    1. Load base config from config/business_rules.json
    2. Apply environment overrides from config/business_rules.{env}.json
    3. Apply region overrides from config/regions/{region}.json
    """
    
    DEFAULT_CONFIG_PATH = Path(__file__).parent.parent.parent / "config"
    DEFAULT_CONFIG_FILE = "business_rules.json"
    
    def __init__(
        self,
        environment: Optional[str] = None,
        region: Optional[str] = None,
        config_path: Optional[Path] = None
    ):
        """
        Initialize business rules configuration.
        
        Args:
            environment: Environment name (dev/test/prod). None = production
            region: Region code (za/au/us/uk). None = default
            config_path: Custom config directory path. None = default
        """
        self.environment = environment or "prod"
        self.region = region
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        
        # Load hierarchical configuration
        self.config = self._load_hierarchical_config()
        
        # Validate configuration
        self._validate_config()
        
        logger.info(
            f"BusinessRulesConfig initialized: "
            f"env={self.environment}, region={self.region}"
        )
    
    def _load_hierarchical_config(self) -> Dict[str, Any]:
        """
        Load configuration with hierarchical override support.
        
        Loading order (later overrides earlier):
        1. Base: config/business_rules.json
        2. Environment: config/business_rules.{env}.json
        3. Region: config/regions/{region}.json
        
        Returns:
            Merged configuration dictionary
        """
        # Load base configuration
        base_config = self._load_config_file(
            self.config_path / self.DEFAULT_CONFIG_FILE
        )
        
        if base_config is None:
            logger.error("Failed to load base configuration, using fallback defaults")
            return self._get_fallback_config()
        
        config = base_config.copy()
        
        # Apply environment overrides
        if self.environment != "prod":
            env_config_file = f"business_rules.{self.environment}.json"
            env_config = self._load_config_file(
                self.config_path / env_config_file
            )
            if env_config:
                config = self._merge_configs(config, env_config)
                logger.info(f"Applied environment overrides: {self.environment}")
        
        # Apply region overrides
        if self.region:
            region_config_file = f"regions/{self.region}.json"
            region_config = self._load_config_file(
                self.config_path / region_config_file
            )
            if region_config:
                config = self._merge_configs(config, region_config)
                logger.info(f"Applied region overrides: {self.region}")
        
        return config
    
    def _load_config_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load JSON configuration file with error handling.
        
        Args:
            file_path: Path to configuration file
            
        Returns:
            Configuration dictionary or None on error
        """
        try:
            if not file_path.exists():
                logger.debug(f"Config file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            logger.debug(f"Loaded config: {file_path}")
            return config
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading config {file_path}: {e}")
            return None
    
    def _merge_configs(
        self,
        base: Dict[str, Any],
        override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Deep merge override config into base config.
        
        Args:
            base: Base configuration dictionary
            override: Override configuration dictionary
            
        Returns:
            Merged configuration dictionary
        """
        merged = base.copy()
        
        for key, value in override.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                merged[key] = self._merge_configs(merged[key], value)
            else:
                # Override value
                merged[key] = value
        
        return merged
    
    def _validate_config(self) -> None:
        """
        Validate configuration against validation rules.
        
        Raises:
            ThresholdValidationError: If any threshold violates validation rules
        """
        if "validation_rules" not in self.config:
            logger.warning("No validation_rules in config, skipping validation")
            return
        
        validation_rules = self.config["validation_rules"]
        
        # Validate routing thresholds
        if "routing_thresholds" in self.config:
            self._validate_thresholds(
                self.config["routing_thresholds"],
                validation_rules.get("min_confidence_threshold", 0.0),
                validation_rules.get("max_confidence_threshold", 1.0),
                "routing_thresholds"
            )
        
        # Validate SLA hours
        if "department_sla_hours" in self.config:
            self._validate_thresholds(
                self.config["department_sla_hours"],
                validation_rules.get("min_sla_hours", 1),
                validation_rules.get("max_sla_hours", 168),
                "department_sla_hours"
            )
        
        logger.debug("Configuration validation passed")
    
    def _validate_thresholds(
        self,
        thresholds: Dict[str, Union[int, float]],
        min_value: Union[int, float],
        max_value: Union[int, float],
        section: str
    ) -> None:
        """
        Validate threshold values are within acceptable range.
        
        Args:
            thresholds: Dictionary of threshold values
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            section: Configuration section name (for error messages)
            
        Raises:
            ThresholdValidationError: If any threshold is out of range
        """
        for key, value in thresholds.items():
            # Skip comment keys
            if key.startswith("_"):
                continue
            
            # Skip non-numeric values
            if not isinstance(value, (int, float)):
                continue
            
            if value < min_value or value > max_value:
                raise ThresholdValidationError(
                    key=f"{section}.{key}",
                    value=value,
                    min_value=min_value,
                    max_value=max_value
                )
    
    def _get_fallback_config(self) -> Dict[str, Any]:
        """
        Get hard-coded fallback configuration for critical failures.
        
        Returns:
            Minimal safe configuration dictionary
        """
        logger.warning("Using hard-coded fallback configuration")
        
        return {
            "version": "1.0.0-fallback",
            "routing_thresholds": {
                "credit_management_confidence": 0.95,
                "standard_confidence": 0.80,
                "hitl_trigger_threshold": 0.80,
            },
            "department_sla_hours": {
                "default_sla_hours": 24
            },
            "processing_time_sla": {
                "ai_classification_minutes": 5,
                "total_routing_minutes": 15
            },
            "feature_flags": {
                "use_config_driven_thresholds": False,
                "log_threshold_violations": True
            }
        }
    
    # ========== Public API Methods ==========
    
    def get_confidence_threshold(
        self,
        department: Optional[str] = None
    ) -> float:
        """
        Get confidence threshold for department routing.
        
        Args:
            department: Department name (e.g., 'credit_management')
                       None = standard threshold
        
        Returns:
            Confidence threshold (0.0 - 1.0)
        """
        thresholds = self.config.get("routing_thresholds", {})
        
        if department:
            key = f"{department}_confidence"
            if key in thresholds:
                return float(thresholds[key])
        
        # Fallback to standard confidence
        return float(thresholds.get("standard_confidence", 0.80))
    
    def get_sla_hours(self, rule_id: str) -> int:
        """
        Get SLA response time in hours for specific rule.
        
        Args:
            rule_id: Rule identifier (e.g., 'R001_DISPUTE_EXPLICIT')
        
        Returns:
            SLA hours (integer)
        """
        sla_config = self.config.get("department_sla_hours", {})
        return int(sla_config.get(rule_id, sla_config.get("default_sla_hours", 24)))
    
    def get_processing_time_sla(self, stage: str = "total") -> int:
        """
        Get processing time SLA in minutes.
        
        Args:
            stage: Processing stage ('ai_classification', 'service_desk_review', 'total')
        
        Returns:
            SLA time in minutes
        """
        sla_config = self.config.get("processing_time_sla", {})
        key = f"{stage}_routing_minutes" if stage == "total" else f"{stage}_minutes"
        return int(sla_config.get(key, 15))
    
    def get_hitl_threshold(self) -> float:
        """
        Get Human-In-The-Loop trigger threshold.
        
        Returns:
            HITL confidence threshold (0.0 - 1.0)
        """
        thresholds = self.config.get("routing_thresholds", {})
        return float(thresholds.get("hitl_trigger_threshold", 0.80))
    
    def get_escalation_threshold(self, level: str) -> int:
        """
        Get age-based escalation threshold.
        
        Args:
            level: Escalation level ('team_lead', 'production_support')
        
        Returns:
            Age threshold in days
        """
        escalation = self.config.get("escalation_thresholds", {})
        key = f"{level}_age_days"
        return int(escalation.get(key, 7))
    
    def get_priority_sla(self, priority: str) -> Dict[str, Any]:
        """
        Get SLA configuration for priority level.
        
        Args:
            priority: Priority code (P0_IMMEDIATE, P1_HIGH, P2_MEDIUM, P3_STANDARD)
        
        Returns:
            Dictionary with response_hours and escalation_warning
        """
        priority_config = self.config.get("priority_sla_response", {})
        return priority_config.get(priority, {
            "response_hours": 24,
            "escalation_warning_hours": 18
        })
    
    def get_currency_settings(self, region: Optional[str] = None) -> Dict[str, str]:
        """
        Get currency settings for region.
        
        Args:
            region: Region code (za/au/us/uk). None = default
        
        Returns:
            Dictionary with currency, locale, symbol
        """
        currency_config = self.config.get("currency_settings", {})
        
        if region and region in currency_config.get("region_currencies", {}):
            return currency_config["region_currencies"][region]
        
        # Return default
        return {
            "currency": currency_config.get("default_currency", "USD"),
            "locale": currency_config.get("default_locale", "en_US"),
            "symbol": "$"
        }
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if feature flag is enabled.
        
        Args:
            feature_name: Feature flag name
        
        Returns:
            True if feature is enabled
        """
        features = self.config.get("feature_flags", {})
        return features.get(feature_name, False)
    
    def get_accuracy_target(self, metric: str) -> float:
        """
        Get accuracy target for quality metric.
        
        Args:
            metric: Metric name (dispute_detection_accuracy, department_routing_accuracy, etc.)
        
        Returns:
            Target accuracy (0.0 - 1.0)
        """
        targets = self.config.get("accuracy_targets", {})
        return float(targets.get(metric, 0.95))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Export complete configuration as dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return self.config.copy()
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        return (f"BusinessRulesConfig("
                f"env={self.environment}, "
                f"region={self.region}, "
                f"version={self.config.get('version', 'unknown')})")


# ========== Convenience Factory Functions ==========

def load_production_config() -> BusinessRulesConfig:
    """Load production configuration (default)."""
    return BusinessRulesConfig(environment="prod")


def load_development_config() -> BusinessRulesConfig:
    """Load development configuration with relaxed thresholds."""
    return BusinessRulesConfig(environment="dev")


def load_test_config() -> BusinessRulesConfig:
    """Load test configuration for unit/integration testing."""
    return BusinessRulesConfig(environment="test")


def load_region_config(region: str) -> BusinessRulesConfig:
    """Load region-specific configuration."""
    return BusinessRulesConfig(region=region)
