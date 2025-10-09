#!/usr/bin/env python3
"""
💾 Configuration Persistence System
Save and load user preferences for provider selection and settings

Features:
1. Save user provider preferences
2. Load preferences on startup
3. Configuration validation
4. Default fallback settings

Author: GitHub Copilot Assistant
Date: October 9, 2025
Purpose: Multi-provider configuration persistence
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages user configuration persistence"""
    
    def __init__(self, config_path: str = "user_config.json"):
        """Initialize config manager with file path"""
        self.config_path = Path(config_path)
        self.default_config = {
            "llm_provider": "Gemini Pro (Cloud)",
            "vector_provider": "Pinecone (Cloud)",
            "show_pipeline_viz": True,
            "debug_mode": False,
            "ensemble_weight": 0.7,
            "other_threshold": 0.6,
            "auto_initialize": True,
            "preferences": {
                "theme": "default",
                "show_cost_info": True,
                "show_performance_metrics": True
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file, return defaults if not found"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # Merge with defaults to handle new settings
                merged_config = self.default_config.copy()
                merged_config.update(config)
                
                logger.info(f"✅ Configuration loaded from {self.config_path}")
                return merged_config
            else:
                logger.info("ℹ️ No config file found, using defaults")
                return self.default_config.copy()
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to load config: {e}, using defaults")
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            # Validate config structure
            if not self._validate_config(config):
                logger.error("❌ Invalid config structure, not saving")
                return False
            
            # Create directory if needed
            self.config_path.parent.mkdir(exist_ok=True)
            
            # Write config file
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save config: {e}")
            return False
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration structure"""
        try:
            # Check required top-level keys
            required_keys = ["llm_provider", "vector_provider", "preferences"]
            for key in required_keys:
                if key not in config:
                    logger.warning(f"Missing required config key: {key}")
                    return False
            
            # Validate provider values
            valid_llm_providers = ["Gemini Pro (Cloud)", "Ollama (Local)"]
            valid_vector_providers = ["Pinecone (Cloud)", "ChromaDB (Local)"]
            
            if config["llm_provider"] not in valid_llm_providers:
                logger.warning(f"Invalid LLM provider: {config['llm_provider']}")
                return False
                
            if config["vector_provider"] not in valid_vector_providers:
                logger.warning(f"Invalid Vector provider: {config['vector_provider']}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Config validation error: {e}")
            return False
    
    def get_provider_costs(self, llm_provider: str, vector_provider: str) -> Dict[str, Any]:
        """Get cost information for provider combination"""
        costs = {
            "llm_cost_per_request": 0.0,
            "vector_cost_per_query": 0.0,
            "estimated_monthly": 0.0,
            "cost_level": "FREE"
        }
        
        # LLM costs
        if "Gemini" in llm_provider:
            costs["llm_cost_per_request"] = 0.002
        elif "Ollama" in llm_provider:
            costs["llm_cost_per_request"] = 0.0
        
        # Vector DB costs  
        if "Pinecone" in vector_provider:
            costs["vector_cost_per_query"] = 0.0001
        elif "ChromaDB" in vector_provider:
            costs["vector_cost_per_query"] = 0.0
        
        # Calculate totals
        total_per_request = costs["llm_cost_per_request"] + costs["vector_cost_per_query"]
        costs["estimated_monthly"] = total_per_request * 1000  # Estimate 1000 requests/month
        
        # Determine cost level
        if total_per_request == 0.0:
            costs["cost_level"] = "FREE"
        elif total_per_request < 0.001:
            costs["cost_level"] = "LOW"
        elif total_per_request < 0.01:
            costs["cost_level"] = "MEDIUM"
        else:
            costs["cost_level"] = "HIGH"
        
        return costs
    
    def update_preference(self, config: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
        """Update a specific preference and return updated config"""
        try:
            # Handle nested preference keys
            if key in config:
                config[key] = value
            elif key in config.get("preferences", {}):
                config["preferences"][key] = value
            else:
                logger.warning(f"Unknown preference key: {key}")
            
            return config
            
        except Exception as e:
            logger.error(f"Failed to update preference {key}: {e}")
            return config

# Singleton instance for global use
config_manager = ConfigManager()

def load_user_config() -> Dict[str, Any]:
    """Load user configuration (convenience function)"""
    return config_manager.load_config()

def save_user_config(config: Dict[str, Any]) -> bool:
    """Save user configuration (convenience function)"""
    return config_manager.save_config(config)

def get_cost_info(llm_provider: str, vector_provider: str) -> Dict[str, Any]:
    """Get cost information for provider combination (convenience function)"""
    return config_manager.get_provider_costs(llm_provider, vector_provider)

if __name__ == "__main__":
    # Demo the configuration system
    print("💾 Testing Configuration Management System")
    
    # Load default config
    config = load_user_config()
    print(f"Loaded config: {json.dumps(config, indent=2)}")
    
    # Test cost calculation
    cost_info = get_cost_info("Ollama (Local)", "ChromaDB (Local)")
    print(f"\nCost info (Ollama + ChromaDB): {cost_info}")
    
    cost_info = get_cost_info("Gemini Pro (Cloud)", "Pinecone (Cloud)")
    print(f"Cost info (Gemini + Pinecone): {cost_info}")
    
    # Test saving config
    config["llm_provider"] = "Ollama (Local)"
    if save_user_config(config):
        print("✅ Configuration saved successfully!")
    else:
        print("❌ Configuration save failed!")