#!/usr/bin/env python3
"""
🤖 Enhanced Ticket Classifier with Google Gemini LLM Integration
Advanced classification system with reasoning and OTHER category support

Features:
1. Google Gemini API integration for enhanced accuracy
2. Reasoning paragraphs explaining classification decisions
3. OTHER category for low-confidence predictions
4. Hybrid approach: Traditional ML + LLM ensemble

Author: Data Scientist AI Assistant  
Date: September 27, 2025
Purpose: Enhanced classification with LLM reasoning
"""

import os
import sys
import logging
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# External libraries
import google.generativeai as genai
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to Python path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

try:
    from models.ticket_classifier import TicketClassificationPipeline
except ImportError:
    logging.error("Could not import base classifier. Please ensure it's available.")
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class EnhancedClassificationResult:
    """Enhanced classification result with reasoning."""
    predicted_category: str
    confidence: float
    reasoning: str
    traditional_prediction: str
    traditional_confidence: float
    gemini_prediction: str
    gemini_confidence: float
    all_probabilities: Dict[str, float]
    processing_time_ms: float
    is_other_category: bool = False

class GeminiEnhancedClassifier:
    """Enhanced ticket classifier using Google Gemini LLM."""
    
    def __init__(self, api_key: Optional[str] = None, traditional_model_path: str = "models/telkom_ticket_classifier.pkl"):
        """Initialize the enhanced classifier."""
        # Get API key from parameter, environment variable, or fail
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Google API key required. Either:\n"
                "1. Set GOOGLE_API_KEY in .env file\n"
                "2. Set GOOGLE_API_KEY environment variable\n"
                "3. Pass api_key parameter\n"
                "Get your key from: https://aistudio.google.com/"
            )
        
        # Initialize Gemini with latest available model
        genai.configure(api_key=self.api_key)
        # Use the latest stable Gemini model
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Load traditional model
        self.traditional_classifier = TicketClassificationPipeline()
        self._load_traditional_model(traditional_model_path)
        
        # Enhanced categories (including OTHER)
        self.categories = ["BILLING", "TECHNICAL", "SALES", "COMPLAINTS", "NETWORK", "ACCOUNT", "OTHER"]
        self.base_categories = ["BILLING", "TECHNICAL", "SALES", "COMPLAINTS", "NETWORK", "ACCOUNT"]
        
        # Confidence thresholds from environment or defaults
        self.other_threshold = float(os.getenv('OTHER_CATEGORY_THRESHOLD', 0.6))
        self.ensemble_weight = float(os.getenv('ENSEMBLE_WEIGHT', 0.7))
        
        logger.info("✅ Enhanced Gemini classifier initialized successfully")
        logger.info(f"   🎯 OTHER threshold: {self.other_threshold:.1%}")
        logger.info(f"   ⚖️ Ensemble weight: {self.ensemble_weight:.1%} Gemini")
    
    def _load_traditional_model(self, model_path: str):
        """Load the traditional ML model."""
        try:
            import pickle
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.traditional_classifier.models = model_data['models']
            self.traditional_classifier.ensemble_weights = model_data['ensemble_weights']
            self.traditional_classifier.training_history = model_data['training_history']
            
            logger.info(f"✅ Traditional model loaded from {model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load traditional model: {e}")
            raise
    
    def _create_gemini_prompt(self, ticket_text: str) -> str:
        """Create optimized prompt for Gemini classification."""
        prompt = f"""
You are an expert customer service ticket classifier for Telkom, a South African telecommunications company.

TASK: Classify the customer ticket and provide detailed reasoning.

CATEGORIES:
1. BILLING - Bills, payments, charges, account balances, billing disputes
2. TECHNICAL - Internet connectivity, speed issues, equipment problems, outages
3. SALES - New services, upgrades, packages, promotions, product inquiries  
4. COMPLAINTS - Service dissatisfaction, poor customer service, escalations
5. NETWORK - Coverage issues, signal problems, infrastructure outages
6. ACCOUNT - Profile updates, password resets, personal information changes
7. OTHER - Tickets that don't clearly fit into the above categories

CUSTOMER TICKET:
"{ticket_text}"

INSTRUCTIONS:
1. Classify into ONE category from the list above
2. Provide a confidence score (0.0 to 1.0)
3. Give detailed reasoning explaining your classification decision
4. Consider South African telecommunications context
5. If the ticket doesn't clearly fit any category (confidence < 0.6), classify as OTHER

RESPONSE FORMAT (JSON):
{{
    "category": "CATEGORY_NAME",
    "confidence": 0.95,
    "reasoning": "Detailed explanation of why this ticket belongs to this category, mentioning specific keywords or context that influenced the decision."
}}
"""
        return prompt
    
    def _query_gemini(self, ticket_text: str) -> Tuple[str, float, str]:
        """Query Gemini for classification with error handling."""
        try:
            prompt = self._create_gemini_prompt(ticket_text)
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            result = json.loads(response_text)
            
            category = result.get('category', 'OTHER')
            confidence = float(result.get('confidence', 0.0))
            reasoning = result.get('reasoning', 'No reasoning provided')
            
            # Validate category
            if category not in self.categories:
                category = 'OTHER'
                confidence = 0.3
                reasoning = f"Original category '{result.get('category')}' not recognized. Classified as OTHER."
            
            return category, confidence, reasoning
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Gemini response as JSON: {e}")
            return "OTHER", 0.2, f"Failed to parse LLM response: {str(e)}"
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return "OTHER", 0.1, f"API error occurred: {str(e)}"
    
    def _ensemble_prediction(self, traditional_pred: str, traditional_conf: float, 
                           gemini_pred: str, gemini_conf: float) -> Tuple[str, float]:
        """Combine traditional and Gemini predictions using weighted ensemble.
        
        Supports full range:
        - 0.0 = Pure Traditional ML
        - 0.5 = Balanced Ensemble  
        - 1.0 = Pure Gemini LLM
        """
        
        # Pure Traditional ML mode (0% Gemini)
        if self.ensemble_weight == 0.0:
            return traditional_pred, traditional_conf
        
        # Pure Gemini LLM mode (100% Gemini)
        if self.ensemble_weight == 1.0:
            return gemini_pred, gemini_conf
        
        # Ensemble modes (between 0% and 100%)
        
        # If Gemini is very confident and traditional is not, prefer Gemini
        if gemini_conf > 0.8 and traditional_conf < 0.7 and self.ensemble_weight > 0.5:
            return gemini_pred, gemini_conf
        
        # If traditional is very confident and Gemini is not, prefer traditional
        if traditional_conf > 0.9 and gemini_conf < 0.7 and self.ensemble_weight < 0.5:
            return traditional_pred, traditional_conf
        
        # If both models agree, use higher confidence
        if gemini_pred == traditional_pred:
            return gemini_pred, max(gemini_conf, traditional_conf)
        
        # Weighted ensemble based on confidence and weights
        gemini_weight = self.ensemble_weight * gemini_conf
        traditional_weight = (1 - self.ensemble_weight) * traditional_conf
        
        if gemini_weight > traditional_weight:
            final_confidence = (self.ensemble_weight * gemini_conf + 
                              (1 - self.ensemble_weight) * traditional_conf)
            return gemini_pred, final_confidence
        else:
            final_confidence = (self.ensemble_weight * gemini_conf + 
                              (1 - self.ensemble_weight) * traditional_conf)
            return traditional_pred, final_confidence
    
    def classify_ticket(self, ticket_text: str) -> EnhancedClassificationResult:
        """Enhanced ticket classification with reasoning."""
        start_time = time.time()
        
        # Get traditional model prediction
        traditional_pred = self.traditional_classifier.predict([ticket_text])[0]
        traditional_proba = self.traditional_classifier.predict_proba([ticket_text])[0]
        
        # Get probabilities for base categories
        base_categories = self.traditional_classifier.models['logistic_regression'].classes_
        traditional_prob_dict = {cat: prob for cat, prob in zip(base_categories, traditional_proba)}
        traditional_confidence = max(traditional_proba)
        
        # Get Gemini prediction
        gemini_pred, gemini_conf, reasoning = self._query_gemini(ticket_text)
        
        # Ensemble prediction
        final_pred, final_conf = self._ensemble_prediction(
            traditional_pred, traditional_confidence, gemini_pred, gemini_conf
        )
        
        # Check for OTHER category
        is_other = False
        if final_conf < self.other_threshold or final_pred == "OTHER":
            final_pred = "OTHER"
            is_other = True
            if reasoning == "No reasoning provided":
                reasoning = f"Classification confidence ({final_conf:.1%}) below threshold ({self.other_threshold:.1%}). Requires human review."
        
        # Build complete probability distribution reflecting ensemble weighting
        all_probabilities = traditional_prob_dict.copy()
        
        # Handle pure modes
        if self.ensemble_weight == 0.0:
            # Pure Traditional ML mode - use traditional probabilities only
            all_probabilities = traditional_prob_dict.copy()
        elif self.ensemble_weight == 1.0:
            # Pure Gemini LLM mode - create Gemini-only probability distribution
            gemini_prob_dict = {cat: 0.05 for cat in self.base_categories}  # Base probability
            if gemini_pred in self.base_categories:
                gemini_prob_dict[gemini_pred] = gemini_conf
            
            # Normalize to sum to 1
            total_gemini = sum(gemini_prob_dict.values())
            all_probabilities = {k: v/total_gemini for k, v in gemini_prob_dict.items()}
        else:
            # Ensemble mode - blend traditional and Gemini probabilities
            
            # Create more realistic Gemini-based probability distribution
            gemini_prob_dict = {}
            
            # Start with traditional probabilities as base, then adjust based on Gemini prediction
            for category in self.base_categories:
                if category == gemini_pred:
                    # Give Gemini's predicted category high confidence
                    gemini_prob_dict[category] = max(0.7, gemini_conf)
                else:
                    # Distribute remaining probability among other categories
                    # Use traditional model's assessment as guidance
                    base_prob = traditional_prob_dict.get(category, 0.1)
                    remaining_conf = max(0.3, 1 - max(0.7, gemini_conf))
                    total_other_traditional = sum(traditional_prob_dict.get(cat, 0.1) 
                                                for cat in self.base_categories if cat != gemini_pred)
                    if total_other_traditional > 0:
                        gemini_prob_dict[category] = base_prob * remaining_conf / total_other_traditional
                    else:
                        gemini_prob_dict[category] = remaining_conf / (len(self.base_categories) - 1)
            
            # Normalize Gemini probabilities to sum to 1
            total_gemini = sum(gemini_prob_dict.values())
            if total_gemini > 0:
                gemini_prob_dict = {k: v/total_gemini for k, v in gemini_prob_dict.items()}
            else:
                # Fallback to uniform distribution
                gemini_prob_dict = {cat: 1.0/len(self.base_categories) for cat in self.base_categories}
            
            # Blend probabilities using ensemble weights
            for category in self.base_categories:
                traditional_prob = traditional_prob_dict.get(category, 0.0)
                gemini_prob = gemini_prob_dict.get(category, 0.0)
                
                # Weighted combination: ensemble_weight for Gemini, (1-ensemble_weight) for traditional
                blended_prob = (self.ensemble_weight * gemini_prob + (1 - self.ensemble_weight) * traditional_prob)
                all_probabilities[category] = blended_prob
        
        # Ensure final prediction has appropriate confidence but don't override the blending
        if final_pred in all_probabilities and final_pred != "OTHER":
            all_probabilities[final_pred] = max(all_probabilities[final_pred], final_conf * 0.9)
        elif final_pred == "OTHER" or final_pred not in all_probabilities:
            # Handle OTHER category or new predictions from Gemini
            all_probabilities[final_pred] = final_conf
        
        # Add OTHER category probability
        if final_pred == "OTHER":
            all_probabilities["OTHER"] = final_conf
        else:
            all_probabilities["OTHER"] = max(0.05, 1.0 - final_conf) if is_other else 0.05
        
        # Normalize probabilities to sum to 1.0
        total_prob = sum(all_probabilities.values())
        all_probabilities = {k: v/total_prob for k, v in all_probabilities.items()}
        
        processing_time = (time.time() - start_time) * 1000
        
        return EnhancedClassificationResult(
            predicted_category=final_pred,
            confidence=final_conf,
            reasoning=reasoning,
            traditional_prediction=traditional_pred,
            traditional_confidence=traditional_confidence,
            gemini_prediction=gemini_pred,
            gemini_confidence=gemini_conf,
            all_probabilities=all_probabilities,
            processing_time_ms=processing_time,
            is_other_category=is_other
        )
    
    def batch_classify(self, ticket_texts: List[str]) -> List[EnhancedClassificationResult]:
        """Classify multiple tickets."""
        results = []
        for i, text in enumerate(ticket_texts):
            logger.info(f"Processing ticket {i+1}/{len(ticket_texts)}")
            result = self.classify_ticket(text)
            results.append(result)
        return results

def main():
    """Test the enhanced classifier."""
    logger.info("🤖 Testing Enhanced Gemini Classifier")
    
    # Test with sample API key (you'll need to set your real API key)
    try:
        classifier = GeminiEnhancedClassifier()
        
        test_tickets = [
            "My internet bill is too high this month, please help me understand the charges",
            "WiFi keeps disconnecting every few minutes, very frustrating",
            "I want to upgrade to a faster internet package for my home office",
            "The customer service agent was very rude and unhelpful",
            "No mobile signal in Sandton area since yesterday",
            "I need to update my billing address as I'm moving next month",
            "Hello, I just wanted to say thank you for your service"  # Should be OTHER
        ]
        
        for i, ticket in enumerate(test_tickets, 1):
            print(f"\n{'='*60}")
            print(f"TEST TICKET {i}: {ticket[:50]}...")
            
            result = classifier.classify_ticket(ticket)
            
            print(f"🎯 PREDICTION: {result.predicted_category}")
            print(f"📈 CONFIDENCE: {result.confidence:.1%}")
            print(f"💭 REASONING: {result.reasoning}")
            print(f"⚡ TIME: {result.processing_time_ms:.0f}ms")
            print(f"🔄 TRADITIONAL: {result.traditional_prediction} ({result.traditional_confidence:.1%})")
            print(f"🤖 GEMINI: {result.gemini_prediction} ({result.gemini_confidence:.1%})")
            
            if result.is_other_category:
                print("⚠️ OTHER CATEGORY - Needs human review")
        
        print(f"\n{'='*60}")
        print("✅ Enhanced classifier testing complete!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        logger.info("💡 Make sure to set your Google API key: export GOOGLE_API_KEY='your-api-key'")

if __name__ == "__main__":
    main()