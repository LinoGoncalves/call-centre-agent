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
    """Enhanced classification result with reasoning, sentiment analysis, and departmental routing."""
    # Original classification fields
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
    
    # Sentiment analysis fields
    sentiment_score: float = 0.0
    sentiment_label: str = "NEUTRAL"
    priority_level: str = "P3_STANDARD"
    escalation_required: bool = False
    sentiment_reasoning: str = ""
    
    # NEW: Departmental routing fields
    department_allocation: str = "BILLING"  # CREDIT_MGMT, ORDER_MGMT, CRM, BILLING
    assigned_team: str = "General Support"  # Specific team within department
    routing_confidence: float = 0.0  # Confidence in department allocation
    routing_reasoning: str = ""  # Why this department was chosen
    
    # NEW: Service Desk & Escalation fields
    service_desk_agent: str = "AI_CLASSIFIER"  # Agent responsible for routing
    requires_hitl: bool = False  # Human-in-the-loop validation needed
    dispute_detected: bool = False  # Specific dispute flag for Credit Management
    dispute_confidence: float = 0.0  # Confidence in dispute detection
    
    # NEW: Age analysis and escalation tracking
    ticket_age_days: int = 0  # Age of ticket in days
    escalation_level: str = "INITIAL"  # INITIAL, TEAM_LEAD, PRODUCTION_SUPPORT
    escalation_triggered: bool = False  # Whether escalation is needed
    
    # NEW: SLA and priority response times
    sla_response_time_hours: int = 36  # P0=1, P1=6, P2=24, P3=36
    sla_warning_triggered: bool = False  # Approaching SLA deadline
    
    # NEW: Quality assurance fields
    routing_override_history: List[str] = None  # Track manual overrides
    confidence_threshold_met: bool = True  # Met required confidence levels
    
    def __post_init__(self):
        """Post-initialization processing for derived fields."""
        if self.routing_override_history is None:
            self.routing_override_history = []
        
        # Set SLA response times based on priority
        sla_times = {
            "P0_IMMEDIATE": 1,
            "P1_HIGH": 6, 
            "P2_MEDIUM": 24,
            "P3_STANDARD": 36
        }
        self.sla_response_time_hours = sla_times.get(self.priority_level, 36)
        
        # Determine if HITL is required based on confidence thresholds
        if self.dispute_detected and self.dispute_confidence < 0.95:
            self.requires_hitl = True
        elif not self.dispute_detected and self.routing_confidence < 0.80:
            self.requires_hitl = True
            
        # Check if confidence thresholds are met
        if self.dispute_detected:
            self.confidence_threshold_met = self.dispute_confidence >= 0.95
        else:
            self.confidence_threshold_met = self.routing_confidence >= 0.80

class GeminiEnhancedClassifier:
    """Enhanced ticket classifier using Google Gemini LLM."""
    
    def __init__(self, api_key: Optional[str] = None, traditional_model_path: str = "models/telco_ticket_classifier.pkl"):
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
        
        # Sentiment analysis configuration
        self.sentiment_categories = {
            "POSITIVE": 0.7,      # Happy, satisfied customers
            "NEUTRAL": 0.0,       # Standard inquiries  
            "NEGATIVE": -0.7,     # Frustrated, angry customers
            "CRITICAL": -1.0      # Extremely upset, escalation required
        }
        
        # Priority mapping based on category + sentiment
        self.priority_map = {
            ("COMPLAINTS", "CRITICAL"): "P0_IMMEDIATE",
            ("COMPLAINTS", "NEGATIVE"): "P1_HIGH",
            ("BILLING", "CRITICAL"): "P1_HIGH", 
            ("BILLING", "NEGATIVE"): "P2_MEDIUM",
            ("TECHNICAL", "CRITICAL"): "P1_HIGH",
            ("TECHNICAL", "NEGATIVE"): "P2_MEDIUM",
            # Default priorities
            ("ANY", "CRITICAL"): "P1_HIGH",
            ("ANY", "NEGATIVE"): "P2_MEDIUM", 
            ("ANY", "NEUTRAL"): "P3_STANDARD",
            ("ANY", "POSITIVE"): "P3_STANDARD"
        }
        
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
        """Create optimized prompt for Gemini classification with sentiment analysis and departmental routing."""
        prompt = f"""
You are an expert customer service ticket classifier and routing specialist for a telecommunications company.

TASK: Classify the customer ticket, analyze sentiment, detect disputes, and determine departmental routing.

TICKET CATEGORIES:
1. BILLING - Bills, payments, charges, account balances, billing inquiries
2. TECHNICAL - Internet connectivity, speed issues, equipment problems, outages
3. SALES - New services, upgrades, packages, promotions, product inquiries  
4. COMPLAINTS - Service dissatisfaction, poor customer service, escalations
5. NETWORK - Coverage issues, signal problems, infrastructure outages
6. ACCOUNT - Profile updates, password resets, personal information changes
7. OTHER - Tickets that don't clearly fit into the above categories

DEPARTMENTAL ROUTING (Priority Order):
1. CREDIT_MGMT - ALL disputes regardless of category (100% priority)
2. ORDER_MGMT - New orders, plan changes, installations, equipment requests
3. CRM - General complaints, retention issues, customer relationship problems
4. BILLING - Non-disputed billing inquiries, payment questions, account balances

DISPUTE vs GENERAL BILLING INQUIRY:
**DISPUTE** (Route to Credit Management):
- Customer explicitly contests validity of charges
- Claims charges are incorrect, unauthorized, or wrong
- Requires investigation (not just explanation)
- Keywords: "dispute", "disagree with charges", "unauthorized", "never ordered", "double charged", "incorrect billing", "contest", "challenge", "refund", "credit", "overcharged", "billing error"

**GENERAL INQUIRY** (Route to Billing):
- Seeking explanation or clarification of charges
- Can be resolved with itemized explanation
- Keywords: "explain my bill", "why is my bill", "payment options", "account balance", "billing cycle"

SENTIMENT LEVELS:
1. POSITIVE (0.7) - Happy, satisfied, appreciative customers
2. NEUTRAL (0.0) - Standard inquiries, factual requests
3. NEGATIVE (-0.7) - Frustrated, dissatisfied, annoyed customers
4. CRITICAL (-1.0) - Extremely upset, angry, threatening to leave

PRIORITY LEVELS:
- P0_IMMEDIATE: Critical outages, security breaches, escalated disputes
- P1_HIGH: Service affecting issues, billing disputes, urgent complaints
- P2_MEDIUM: Standard technical issues, general complaints, account changes
- P3_STANDARD: Routine inquiries, information requests, minor issues

CUSTOMER TICKET:
"{ticket_text}"

INSTRUCTIONS:
1. Classify into ONE category from the ticket categories
2. Determine appropriate department routing based on content analysis
3. **CRITICAL**: Detect if this is a billing dispute (requires Credit Management)
4. Analyze customer sentiment and assign sentiment score
5. Determine priority level based on urgency and impact
6. Provide confidence scores for classification and departmental routing
7. Give detailed reasoning for all decisions
8. Consider South African telecommunications context
9. If ticket doesn't clearly fit any category (confidence < 0.6), classify as OTHER
10. **CRITICAL: Use plain text only. Do NOT use HTML tags, markdown formatting, or any special formatting in your reasoning.**

RESPONSE FORMAT (JSON):
{{
    "category": "CATEGORY_NAME",
    "confidence": 0.95,
    "reasoning": "Detailed explanation of category classification decision.",
    "department_allocation": "CREDIT_MGMT",
    "routing_confidence": 0.98,
    "routing_reasoning": "Detailed explanation of why this department was chosen.",
    "dispute_detected": true,
    "dispute_confidence": 0.95,
    "sentiment_score": -0.7,
    "sentiment_label": "NEGATIVE",
    "sentiment_reasoning": "Customer shows frustration with repeated use of words like terrible and fed up indicating negative emotional state.",
    "priority_level": "P1_HIGH",
    "escalation_required": false
}}
"""
        return prompt
    
    def _query_gemini(self, ticket_text: str) -> Tuple[str, float, str, str, float, str, bool, float, float, str, str, str, bool]:
        """Query Gemini for classification, sentiment analysis, and departmental routing.
        
        Returns:
            Tuple of (category, confidence, reasoning, department_allocation, routing_confidence, 
                     routing_reasoning, dispute_detected, dispute_confidence, sentiment_score, 
                     sentiment_label, sentiment_reasoning, priority_level, escalation_required)
        """
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
            
            # Category classification
            category = result.get('category', 'OTHER')
            confidence = float(result.get('confidence', 0.0))
            reasoning = result.get('reasoning', 'No reasoning provided')
            
            # Departmental routing
            department_allocation = result.get('department_allocation', 'BILLING')
            routing_confidence = float(result.get('routing_confidence', 0.0))
            routing_reasoning = result.get('routing_reasoning', 'Standard routing applied')
            
            # Dispute detection
            dispute_detected = bool(result.get('dispute_detected', False))
            dispute_confidence = float(result.get('dispute_confidence', 0.0))
            
            # Sentiment analysis
            sentiment_score = float(result.get('sentiment_score', 0.0))
            sentiment_label = result.get('sentiment_label', 'NEUTRAL')
            sentiment_reasoning = result.get('sentiment_reasoning', 'No sentiment analysis provided')
            
            # Priority and escalation
            priority_level = result.get('priority_level', 'P3_STANDARD')
            escalation_required = bool(result.get('escalation_required', False))
            
            # Clean HTML from all reasoning fields at the source
            import re
            import html
            
            for field_name, field_value in [
                ('reasoning', reasoning),
                ('routing_reasoning', routing_reasoning), 
                ('sentiment_reasoning', sentiment_reasoning)
            ]:
                if field_value:
                    # Decode HTML entities
                    cleaned = html.unescape(field_value)
                    
                    # Remove all HTML tags
                    cleaned = re.sub(r'<[^>]*?>', '', cleaned)
                    cleaned = re.sub(r'<.*?>', '', cleaned)
                    
                    # Remove common prefixes
                    cleaned = re.sub(r'^(Reasoning:\s*|reasoning:\s*|Analysis:\s*)', '', cleaned, flags=re.IGNORECASE)
                    
                    # Clean whitespace
                    cleaned = ' '.join(cleaned.split())
                    
                    # Validation: Check if HTML tags are still present
                    if '<' in cleaned or '>' in cleaned:
                        # Aggressive cleaning for persistent HTML
                        cleaned = re.sub(r'[<>]', '', cleaned)
                        logger.warning(f"🚨 HTML tags detected in {field_name}, cleaned aggressively")
                    
                    # Update the variable
                    if field_name == 'reasoning':
                        reasoning = cleaned if cleaned.strip() else 'Classification completed successfully.'
                    elif field_name == 'routing_reasoning':
                        routing_reasoning = cleaned if cleaned.strip() else 'Standard routing applied.'
                    elif field_name == 'sentiment_reasoning':
                        sentiment_reasoning = cleaned if cleaned.strip() else 'Sentiment analysis completed successfully.'
            
            # Validate category
            if category not in self.categories:
                category = 'OTHER'
                confidence = 0.3
                reasoning = f"Original category '{result.get('category')}' not recognized. Classified as OTHER."
            
            # Validate department allocation
            valid_departments = ['CREDIT_MGMT', 'ORDER_MGMT', 'CRM', 'BILLING']
            if department_allocation not in valid_departments:
                department_allocation = 'BILLING'
                routing_confidence = 0.5
                routing_reasoning = f"Original department '{result.get('department_allocation')}' not recognized. Routed to BILLING."
            
            # Validate sentiment label
            if sentiment_label not in self.sentiment_categories:
                sentiment_label = 'NEUTRAL'
                sentiment_score = 0.0
                sentiment_reasoning = f"Original sentiment '{result.get('sentiment_label')}' not recognized. Set to NEUTRAL."
            
            # Validate priority level
            valid_priorities = ['P0_IMMEDIATE', 'P1_HIGH', 'P2_MEDIUM', 'P3_STANDARD']
            if priority_level not in valid_priorities:
                priority_level = 'P3_STANDARD'
                escalation_required = False
            
            return (category, confidence, reasoning, department_allocation, routing_confidence, 
                   routing_reasoning, dispute_detected, dispute_confidence, sentiment_score, 
                   sentiment_label, sentiment_reasoning, priority_level, escalation_required)
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Gemini response as JSON: {e}")
            return ("OTHER", 0.2, f"Failed to parse LLM response: {str(e)}", "BILLING", 0.3, 
                   "Error in routing analysis", False, 0.0, 0.0, "NEUTRAL", "Error in sentiment analysis", 
                   "P3_STANDARD", False)
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return ("OTHER", 0.1, f"API error occurred: {str(e)}", "BILLING", 0.2, 
                   "Error in routing analysis", False, 0.0, 0.0, "NEUTRAL", "Error in sentiment analysis", 
                   "P3_STANDARD", False)
    
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
    
    def _calculate_priority_level(self, category: str, sentiment_label: str) -> str:
        """Calculate priority level based on category and sentiment."""
        # Direct mapping first
        key = (category, sentiment_label)
        if key in self.priority_map:
            return self.priority_map[key]
            
        # Fallback to ANY category mapping
        fallback_key = ("ANY", sentiment_label)
        return self.priority_map.get(fallback_key, "P3_STANDARD")
    
    def _requires_escalation(self, category: str, sentiment_label: str, sentiment_score: float) -> bool:
        """Determine if ticket requires immediate escalation."""
        # Critical sentiment always requires escalation
        if sentiment_label == "CRITICAL":
            return True
            
        # COMPLAINTS with negative sentiment need escalation
        if category == "COMPLAINTS" and sentiment_label == "NEGATIVE":
            return True
            
        # High-priority categories with very low sentiment scores
        if category in ["BILLING", "TECHNICAL"] and sentiment_score <= -0.8:
            return True
            
        return False
    
    def _determine_assigned_team(self, department: str, category: str) -> str:
        """Determine the specific team within a department based on category and routing rules."""
        team_mapping = {
            "CREDIT_MGMT": {
                "default": "Credit Management Team",
                "BILLING": "Billing Disputes Team",
                "COMPLAINTS": "Credit Management Team",
                "ACCOUNT": "Account Recovery Team"
            },
            "ORDER_MGMT": {
                "default": "Order Processing Team", 
                "SALES": "Sales Support Team",
                "TECHNICAL": "Installation Team",
                "ACCOUNT": "Service Activation Team"
            },
            "CRM": {
                "default": "Customer Success Team",
                "COMPLAINTS": "Customer Relations Team",
                "ACCOUNT": "Account Management Team",
                "SALES": "Retention Team"
            },
            "BILLING": {
                "default": "Billing Support Team",
                "BILLING": "Billing Inquiries Team",
                "ACCOUNT": "Account Billing Team",
                "TECHNICAL": "Billing Systems Team"
            }
        }
        
        dept_teams = team_mapping.get(department, {"default": "General Support"})
        return dept_teams.get(category, dept_teams.get("default", "General Support"))
    
    def classify_ticket(self, ticket_text: str) -> EnhancedClassificationResult:
        """Enhanced ticket classification with reasoning and sentiment analysis."""
        start_time = time.time()
        
        # Get traditional model prediction
        traditional_pred = self.traditional_classifier.predict([ticket_text])[0]
        traditional_proba = self.traditional_classifier.predict_proba([ticket_text])[0]
        
        # Get probabilities for base categories
        base_categories = self.traditional_classifier.models['logistic_regression'].classes_
        traditional_prob_dict = {cat: prob for cat, prob in zip(base_categories, traditional_proba)}
        traditional_confidence = max(traditional_proba)
        
        # Get Gemini prediction with sentiment analysis and departmental routing
        (gemini_pred, gemini_conf, reasoning, department_allocation, routing_confidence, 
         routing_reasoning, dispute_detected, dispute_confidence, sentiment_score, 
         sentiment_label, sentiment_reasoning, priority_level, escalation_required) = self._query_gemini(ticket_text)
        
        # Ensemble prediction
        final_pred, final_conf = self._ensemble_prediction(
            traditional_pred, traditional_confidence, gemini_pred, gemini_conf
        )
        
        # Calculate priority and escalation based on final prediction and sentiment
        priority_level = self._calculate_priority_level(final_pred, sentiment_label)
        escalation_required = self._requires_escalation(final_pred, sentiment_label, sentiment_score)
        
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
        
        # FINAL NUCLEAR HTML CLEANING - Last safety check before return
        import re
        import html
        
        # Clean the sentiment_reasoning one more time to be absolutely sure
        original_reasoning = sentiment_reasoning
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(sentiment_reasoning, 'html.parser')
            sentiment_reasoning = soup.get_text()
        except Exception:
            # BeautifulSoup failed, continue with other cleaning methods
            pass
        
        # Decode HTML entities and remove tags
        sentiment_reasoning = html.unescape(sentiment_reasoning)
        sentiment_reasoning = re.sub(r'<[^>]*>', '', sentiment_reasoning)
        sentiment_reasoning = re.sub(r'&[a-zA-Z0-9#]+;', '', sentiment_reasoning)
        
        # Nuclear option - remove any angle brackets
        if '<' in sentiment_reasoning or '>' in sentiment_reasoning:
            sentiment_reasoning = ''.join(c for c in sentiment_reasoning if c not in '<>')
            logger.warning(f"🚨🚨🚨 FINAL HTML DETECTED - Removed at return stage")
            logger.warning(f"Original: {repr(original_reasoning[:100])}")
            logger.warning(f"Cleaned: {repr(sentiment_reasoning[:100])}")
        
        # Clean whitespace
        sentiment_reasoning = ' '.join(sentiment_reasoning.split())
        
        # Ensure we have content
        if not sentiment_reasoning.strip():
            sentiment_reasoning = 'Sentiment analysis completed successfully.'
        
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
            is_other_category=is_other,
            # Sentiment analysis fields
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            priority_level=priority_level,
            escalation_required=escalation_required,
            sentiment_reasoning=sentiment_reasoning,
            # Departmental routing fields
            department_allocation=department_allocation,
            assigned_team=self._determine_assigned_team(department_allocation, final_pred),
            routing_confidence=routing_confidence,
            routing_reasoning=routing_reasoning,
            # Service Desk & Escalation fields
            service_desk_agent="AI_CLASSIFIER",
            dispute_detected=dispute_detected,
            dispute_confidence=dispute_confidence,
            # Age analysis fields (will be populated by external systems)
            ticket_age_days=0,
            escalation_level="INITIAL",
            escalation_triggered=False,
            # SLA fields (calculated in __post_init__)
            sla_response_time_hours=36,  # Will be updated by priority
            sla_warning_triggered=False
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