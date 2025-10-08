#!/usr/bin/env python3
"""
🔓 Open Source LLM Integration via Ollama
Simple integration with local Ollama for demo purposes

Features:
1. Ollama API integration for local LLM inference
2. Fallback to existing Gemini if Ollama unavailable
3. Drop-in replacement for cloud LLM calls
4. Cost tracking and performance metrics

Author: GitHub Copilot Assistant
Date: October 9, 2025
Purpose: Open source LLM demonstration
"""

import logging
import time
import json
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    """Response from LLM with metadata"""
    content: str
    processing_time_ms: float
    model_used: str
    tokens_used: Optional[int] = None
    cost_estimate: float = 0.0
    source: str = "ollama"  # "ollama" or "fallback"

class OpenSourceLLM:
    """
    Open Source LLM client using Ollama
    
    Provides local, private LLM inference with fallback to cloud services
    """
    
    def __init__(self, 
                 model_name: str = "llama3.2:3b",
                 ollama_url: str = "http://localhost:11434",
                 fallback_handler=None):
        """
        Initialize OpenSourceLLM client
        
        Args:
            model_name: Ollama model to use (e.g., "llama3.2:3b", "mistral:7b")
            ollama_url: Ollama server URL
            fallback_handler: Fallback LLM handler if Ollama unavailable
        """
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.fallback_handler = fallback_handler
        self.available = self._check_ollama_availability()
        
        if self.available:
            logger.info(f"✅ Ollama available - using {model_name}")
        else:
            logger.warning(f"⚠️ Ollama not available - will use fallback if provided")
    
    def _check_ollama_availability(self) -> bool:
        """Check if Ollama server is running and model is available"""
        try:
            # Check server status
            response = requests.get(f"{self.ollama_url}/api/version", timeout=5)
            if response.status_code != 200:
                return False
            
            # Check if model is available
            models_response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if models_response.status_code != 200:
                return False
                
            models = models_response.json().get("models", [])
            available_models = [model["name"] for model in models]
            
            if self.model_name not in available_models:
                logger.warning(f"Model {self.model_name} not found. Available: {available_models}")
                return False
                
            return True
            
        except Exception as e:
            logger.debug(f"Ollama availability check failed: {e}")
            return False
    
    def generate_text(self, 
                     prompt: str, 
                     max_tokens: int = 500,
                     temperature: float = 0.1) -> LLMResponse:
        """
        Generate text using Ollama or fallback
        
        Args:
            prompt: Input prompt for the LLM
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 = deterministic)
            
        Returns:
            LLMResponse with generated text and metadata
        """
        start_time = time.time()
        
        if self.available:
            try:
                return self._ollama_generate(prompt, max_tokens, temperature, start_time)
            except Exception as e:
                logger.error(f"Ollama generation failed: {e}")
                # Fall through to fallback
        
        # Use fallback if Ollama unavailable or failed
        if self.fallback_handler:
            logger.info("Using fallback LLM handler")
            try:
                fallback_response = self.fallback_handler.generate_text(prompt)
                processing_time = (time.time() - start_time) * 1000
                
                return LLMResponse(
                    content=fallback_response,
                    processing_time_ms=processing_time,
                    model_used="fallback",
                    source="fallback"
                )
            except Exception as e:
                logger.error(f"Fallback also failed: {e}")
        
        # Last resort - return error message
        processing_time = (time.time() - start_time) * 1000
        return LLMResponse(
            content="Error: No LLM available for text generation",
            processing_time_ms=processing_time,
            model_used="none",
            source="error"
        )
    
    def _ollama_generate(self, prompt: str, max_tokens: int, temperature: float, start_time: float) -> LLMResponse:
        """Generate text using Ollama API"""
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "stop": ["\n\n", "Human:", "Assistant:"]
            },
            "stream": False
        }
        
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json=payload,
            timeout=60  # Generous timeout for local inference
        )
        
        response.raise_for_status()
        result = response.json()
        
        processing_time = (time.time() - start_time) * 1000
        
        return LLMResponse(
            content=result.get("response", ""),
            processing_time_ms=processing_time,
            model_used=self.model_name,
            tokens_used=result.get("eval_count", 0),
            cost_estimate=0.0,  # Open source = free!
            source="ollama"
        )
    
    def classify_ticket(self, ticket_text: str) -> Tuple[str, str, float, Dict]:
        """
        Classify customer service ticket using local LLM
        
        Args:
            ticket_text: Customer service ticket description
            
        Returns:
            Tuple of (department, reasoning, confidence, metadata)
        """
        
        prompt = f"""You are a customer service ticket classifier for a telecommunications company.

Analyze this customer ticket and classify it into ONE of these departments:
- billing_and_payments
- technical_support_l1  
- technical_support_l2
- sales_and_upgrades
- network_outages
- account_management
- complaints_and_escalations

Customer Ticket:
"{ticket_text}"

Respond in this EXACT format:
DEPARTMENT: [department_name]
CONFIDENCE: [0.0-1.0]
REASONING: [brief explanation of why this department was chosen]

Response:"""

        response = self.generate_text(prompt, max_tokens=200, temperature=0.1)
        
        # Parse the structured response
        try:
            lines = response.content.strip().split('\n')
            department = ""
            confidence = 0.0
            reasoning = "Classification completed"
            
            for line in lines:
                line = line.strip()
                if line.startswith("DEPARTMENT:"):
                    department = line.replace("DEPARTMENT:", "").strip()
                elif line.startswith("CONFIDENCE:"):
                    confidence = float(line.replace("CONFIDENCE:", "").strip())
                elif line.startswith("REASONING:"):
                    reasoning = line.replace("REASONING:", "").strip()
            
            # Validate department
            valid_departments = [
                "billing_and_payments", "technical_support_l1", "technical_support_l2",
                "sales_and_upgrades", "network_outages", "account_management", 
                "complaints_and_escalations"
            ]
            
            if department not in valid_departments:
                department = "technical_support_l1"  # Default fallback
                confidence = 0.5
                reasoning = "Defaulted due to parsing error"
            
            metadata = {
                "model_used": response.model_used,
                "processing_time_ms": response.processing_time_ms,
                "tokens_used": response.tokens_used,
                "cost_estimate": response.cost_estimate,
                "source": response.source
            }
            
            return department, reasoning, confidence, metadata
            
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.debug(f"Raw response: {response.content}")
            
            return "technical_support_l1", "Classification parsing failed", 0.3, {
                "error": str(e),
                "source": response.source,
                "processing_time_ms": response.processing_time_ms
            }

def install_ollama_instructions():
    """Print instructions for installing Ollama"""
    return """
🔓 Quick Ollama Setup for Open Source LLM Demo

1. Install Ollama:
   Windows: Download from https://ollama.com/download
   macOS: brew install ollama
   Linux: curl -fsSL https://ollama.com/install.sh | sh

2. Start Ollama service:
   ollama serve

3. Pull recommended model:
   ollama pull llama3.2:3b     # Fast, efficient (3GB)
   # or
   ollama pull mistral:7b      # Larger, more capable (4GB)

4. Verify installation:
   ollama list
   ollama run llama3.2:3b "Hello, how are you?"

5. Ready to use! The demo will automatically detect Ollama.

💡 Benefits:
- 100% private and offline
- No API costs or rate limits  
- ~2-5 second response time
- Perfect for demos and development
"""

if __name__ == "__main__":
    # Demo the open source LLM
    print("🔓 Testing Open Source LLM Integration...")
    
    llm = OpenSourceLLM()
    
    if not llm.available:
        print("\n" + install_ollama_instructions())
    else:
        # Test classification
        test_ticket = "My internet connection is very slow and I can't stream videos"
        dept, reasoning, conf, meta = llm.classify_ticket(test_ticket)
        
        print(f"\n📋 Test Classification:")
        print(f"Ticket: {test_ticket}")
        print(f"Department: {dept}")
        print(f"Confidence: {conf:.1%}")
        print(f"Reasoning: {reasoning}")
        print(f"Model: {meta.get('model_used', 'unknown')}")
        print(f"Time: {meta.get('processing_time_ms', 0):.1f}ms")
        print(f"Cost: ${meta.get('cost_estimate', 0):.4f}")