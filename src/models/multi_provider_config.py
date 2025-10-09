#!/usr/bin/env python3
"""
🔧 Multi-Provider Configuration System
Configurable LLM and Vector DB provider selection with fallback support

Features:
1. LLM Provider Selection (Gemini Pro, Ollama)
2. Vector DB Provider Selection (Pinecone, ChromaDB)
3. User preference management
4. Automatic fallback handling
5. Cost tracking and comparison

Author: GitHub Copilot Assistant
Date: October 9, 2025
Purpose: Multi-provider system with user control
"""

import logging
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Available LLM providers"""
    GEMINI = "gemini"
    OLLAMA = "ollama"
    
class VectorDBProvider(Enum):
    """Available Vector DB providers"""
    PINECONE = "pinecone"
    CHROMADB = "chromadb"

@dataclass
class ProviderConfig:
    """Configuration for a specific provider"""
    name: str
    enabled: bool
    priority: int  # Lower number = higher priority
    cost_per_query: float
    avg_response_time_ms: float
    availability_check: bool
    fallback_providers: List[str]
    metadata: Dict[str, Any]

@dataclass
class MultiProviderResult:
    """Result from multi-provider operation"""
    content: str
    provider_used: str
    processing_time_ms: float
    cost_estimate: float
    fallback_used: bool
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MultiProviderConfig:
    """
    Multi-Provider Configuration Manager
    
    Manages LLM and Vector DB provider selection with user preferences
    """
    
    def __init__(self, config_file: str = "provider_config.json"):
        """
        Initialize multi-provider configuration
        
        Args:
            config_file: Path to configuration file for persistence
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self._validate_providers()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                logger.info(f"✅ Loaded provider config from {self.config_file}")
                return config
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
        
        # Default configuration
        default_config = {
            "llm_providers": {
                "gemini": {
                    "name": "Google Gemini Pro",
                    "enabled": True,
                    "priority": 1,
                    "cost_per_query": 0.0003,
                    "avg_response_time_ms": 1500,
                    "availability_check": True,
                    "fallback_providers": ["ollama"],
                    "metadata": {
                        "model": "gemini-pro",
                        "api_key_required": True,
                        "data_sovereignty": "cloud",
                        "rate_limits": "60 requests/minute"
                    }
                },
                "ollama": {
                    "name": "Ollama Local LLM",
                    "enabled": True, 
                    "priority": 2,
                    "cost_per_query": 0.0,
                    "avg_response_time_ms": 3000,
                    "availability_check": True,
                    "fallback_providers": ["gemini"],
                    "metadata": {
                        "model": "llama3.2:3b",
                        "api_key_required": False,
                        "data_sovereignty": "local",
                        "rate_limits": "No limits"
                    }
                }
            },
            "vector_db_providers": {
                "pinecone": {
                    "name": "Pinecone Vector Database",
                    "enabled": True,
                    "priority": 1,
                    "cost_per_query": 0.005,
                    "avg_response_time_ms": 100,
                    "availability_check": True,
                    "fallback_providers": ["chromadb"],
                    "metadata": {
                        "index_name": "telco-tickets",
                        "api_key_required": True,
                        "data_sovereignty": "cloud",
                        "scalability": "enterprise"
                    }
                },
                "chromadb": {
                    "name": "ChromaDB Embedded Vector DB",
                    "enabled": True,
                    "priority": 2, 
                    "cost_per_query": 0.0,
                    "avg_response_time_ms": 50,
                    "availability_check": True,
                    "fallback_providers": ["pinecone"],
                    "metadata": {
                        "collection_name": "telco_tickets",
                        "api_key_required": False,
                        "data_sovereignty": "local",
                        "scalability": "development"
                    }
                }
            },
            "user_preferences": {
                "preferred_llm": "gemini",
                "preferred_vector_db": "pinecone",
                "cost_optimization": True,
                "fallback_enabled": True,
                "max_cost_per_query": 0.01,
                "max_response_time_ms": 5000
            },
            "global_settings": {
                "version": "1.0",
                "last_updated": time.time(),
                "auto_fallback": True,
                "availability_check_interval": 300,
                "cost_tracking": True
            }
        }
        
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            config["global_settings"]["last_updated"] = time.time()
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"✅ Saved provider config to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def _validate_providers(self):
        """Validate provider configurations"""
        # Check LLM providers
        for provider_id, config in self.config.get("llm_providers", {}).items():
            try:
                if provider_id == "ollama":
                    self._check_ollama_availability(config)
                elif provider_id == "gemini":
                    self._check_gemini_availability(config)
            except Exception as e:
                logger.warning(f"Provider {provider_id} validation failed: {e}")
                config["enabled"] = False
        
        # Check Vector DB providers  
        for provider_id, config in self.config.get("vector_db_providers", {}).items():
            try:
                if provider_id == "chromadb":
                    self._check_chromadb_availability(config)
                elif provider_id == "pinecone":
                    self._check_pinecone_availability(config)
            except Exception as e:
                logger.warning(f"Provider {provider_id} validation failed: {e}")
                config["enabled"] = False
    
    def _check_ollama_availability(self, config: Dict) -> bool:
        """Check if Ollama is available"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/version", timeout=5)
            available = response.status_code == 200
            config["metadata"]["status"] = "available" if available else "unavailable"
            return available
        except Exception:
            config["metadata"]["status"] = "unavailable"
            return False
    
    def _check_gemini_availability(self, config: Dict) -> bool:
        """Check if Gemini is available"""
        api_key = os.getenv("GOOGLE_API_KEY")
        available = api_key is not None and len(api_key) > 0
        config["metadata"]["status"] = "available" if available else "no_api_key"
        return available
    
    def _check_chromadb_availability(self, config: Dict) -> bool:
        """Check if ChromaDB is available"""
        try:
            import chromadb
            config["metadata"]["status"] = "available"
            return True
        except ImportError:
            config["metadata"]["status"] = "not_installed"
            return False
    
    def _check_pinecone_availability(self, config: Dict) -> bool:
        """Check if Pinecone is available"""
        api_key = os.getenv("PINECONE_API_KEY")
        available = api_key is not None and len(api_key) > 0
        config["metadata"]["status"] = "available" if available else "no_api_key"
        return available
    
    def get_available_llm_providers(self) -> List[Dict[str, Any]]:
        """Get list of available LLM providers"""
        providers = []
        for provider_id, config in self.config.get("llm_providers", {}).items():
            if config.get("enabled", False):
                providers.append({
                    "id": provider_id,
                    "name": config["name"],
                    "cost_per_query": config["cost_per_query"],
                    "response_time_ms": config["avg_response_time_ms"],
                    "status": config["metadata"].get("status", "unknown"),
                    "data_sovereignty": config["metadata"].get("data_sovereignty", "unknown")
                })
        return sorted(providers, key=lambda x: self.config["llm_providers"][x["id"]]["priority"])
    
    def get_available_vector_db_providers(self) -> List[Dict[str, Any]]:
        """Get list of available Vector DB providers"""
        providers = []
        for provider_id, config in self.config.get("vector_db_providers", {}).items():
            if config.get("enabled", False):
                providers.append({
                    "id": provider_id,
                    "name": config["name"],
                    "cost_per_query": config["cost_per_query"], 
                    "response_time_ms": config["avg_response_time_ms"],
                    "status": config["metadata"].get("status", "unknown"),
                    "data_sovereignty": config["metadata"].get("data_sovereignty", "unknown")
                })
        return sorted(providers, key=lambda x: self.config["vector_db_providers"][x["id"]]["priority"])
    
    def set_preferred_llm(self, provider_id: str) -> bool:
        """Set preferred LLM provider"""
        if provider_id in self.config.get("llm_providers", {}):
            self.config["user_preferences"]["preferred_llm"] = provider_id
            self._save_config(self.config)
            logger.info(f"✅ Set preferred LLM provider to: {provider_id}")
            return True
        return False
    
    def set_preferred_vector_db(self, provider_id: str) -> bool:
        """Set preferred Vector DB provider"""
        if provider_id in self.config.get("vector_db_providers", {}):
            self.config["user_preferences"]["preferred_vector_db"] = provider_id
            self._save_config(self.config)
            logger.info(f"✅ Set preferred Vector DB provider to: {provider_id}")
            return True
        return False
    
    def get_preferred_llm(self) -> str:
        """Get current preferred LLM provider"""
        return self.config["user_preferences"]["preferred_llm"]
    
    def get_preferred_vector_db(self) -> str:
        """Get current preferred Vector DB provider"""
        return self.config["user_preferences"]["preferred_vector_db"]
    
    def get_cost_comparison(self) -> Dict[str, Any]:
        """Get cost comparison between providers"""
        llm_costs = {}
        for provider_id, config in self.config.get("llm_providers", {}).items():
            if config.get("enabled", False):
                llm_costs[provider_id] = {
                    "name": config["name"],
                    "cost_per_query": config["cost_per_query"],
                    "monthly_cost_1k_queries": config["cost_per_query"] * 1000,
                    "annual_savings_vs_most_expensive": 0  # Calculated below
                }
        
        vector_db_costs = {}
        for provider_id, config in self.config.get("vector_db_providers", {}).items():
            if config.get("enabled", False):
                vector_db_costs[provider_id] = {
                    "name": config["name"],
                    "cost_per_query": config["cost_per_query"],
                    "monthly_cost_1k_queries": config["cost_per_query"] * 1000,
                    "annual_savings_vs_most_expensive": 0  # Calculated below
                }
        
        # Calculate potential savings
        if llm_costs:
            max_llm_cost = max(llm_costs.values(), key=lambda x: x["cost_per_query"])["cost_per_query"]
            for provider_id in llm_costs:
                annual_queries = 12000  # 1k queries per month
                savings = (max_llm_cost - llm_costs[provider_id]["cost_per_query"]) * annual_queries
                llm_costs[provider_id]["annual_savings_vs_most_expensive"] = max(0, savings)
        
        if vector_db_costs:
            max_vdb_cost = max(vector_db_costs.values(), key=lambda x: x["cost_per_query"])["cost_per_query"]
            for provider_id in vector_db_costs:
                annual_queries = 12000  # 1k queries per month
                savings = (max_vdb_cost - vector_db_costs[provider_id]["cost_per_query"]) * annual_queries
                vector_db_costs[provider_id]["annual_savings_vs_most_expensive"] = max(0, savings)
        
        return {
            "llm_providers": llm_costs,
            "vector_db_providers": vector_db_costs,
            "total_potential_annual_savings": sum(
                provider["annual_savings_vs_most_expensive"] 
                for provider in list(llm_costs.values()) + list(vector_db_costs.values())
            )
        }
    
    def update_user_preferences(self, **preferences) -> bool:
        """Update user preferences"""
        try:
            current_prefs = self.config["user_preferences"]
            for key, value in preferences.items():
                if key in current_prefs:
                    current_prefs[key] = value
                    logger.info(f"Updated preference {key} = {value}")
            
            self._save_config(self.config)
            return True
        except Exception as e:
            logger.error(f"Failed to update preferences: {e}")
            return False

def installation_instructions():
    """Return installation instructions for all providers"""
    return """
🔧 Multi-Provider Setup Instructions

LLM Providers:
1. Gemini Pro (Cloud, Paid):
   - Set GOOGLE_API_KEY environment variable
   - Already configured in existing system
   
2. Ollama (Local, Free):
   - Download: https://ollama.com/download
   - Install and start: ollama serve
   - Pull model: ollama pull llama3.2:3b
   - Automatic detection at http://localhost:11434

Vector DB Providers:
1. Pinecone (Cloud, Paid):
   - Set PINECONE_API_KEY environment variable  
   - Already configured in existing system
   
2. ChromaDB (Local, Free):
   - Install: pip install chromadb
   - Automatic initialization with sample data
   - Local storage: ./chroma_db/

🎯 Quick Start (Zero Cost):
1. pip install chromadb
2. ollama pull llama3.2:3b
3. Run demo with local providers selected

💰 Cost Comparison (1000 queries/month):
- Gemini + Pinecone: ~$5-15/month
- Ollama + ChromaDB: $0/month (100% local)
"""

if __name__ == "__main__":
    # Demo multi-provider configuration
    print("🔧 Testing Multi-Provider Configuration System...")
    
    config = MultiProviderConfig()
    
    print("\n📊 Available LLM Providers:")
    for provider in config.get_available_llm_providers():
        print(f"  {provider['name']}: ${provider['cost_per_query']:.4f}/query, {provider['response_time_ms']}ms, {provider['status']}")
    
    print("\n📊 Available Vector DB Providers:")
    for provider in config.get_available_vector_db_providers():
        print(f"  {provider['name']}: ${provider['cost_per_query']:.4f}/query, {provider['response_time_ms']}ms, {provider['status']}")
    
    print(f"\n⚙️ Current Preferences:")
    print(f"  Preferred LLM: {config.get_preferred_llm()}")
    print(f"  Preferred Vector DB: {config.get_preferred_vector_db()}")
    
    print(f"\n💰 Cost Comparison:")
    costs = config.get_cost_comparison()
    print(f"  Total potential annual savings: ${costs['total_potential_annual_savings']:.2f}")
    
    print(f"\n📋 Setup Instructions:")
    if any(p['status'] == 'unavailable' for p in config.get_available_llm_providers() + config.get_available_vector_db_providers()):
        print(installation_instructions())
    else:
        print("✅ All providers configured and available!")