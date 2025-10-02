# 🤖 Phase 3: AI Enhancement - Gemini LLM Integration

> **Estimated Time**: 4-6 hours
> **Difficulty**: Intermediate
> **Prerequisites**: Completed Phase 1-2, have Google API key

---

## 🎯 Learning Objectives

- Understand Large Language Models (LLMs) and their capabilities
- Integrate Google Gemini API for intelligent text analysis
- Implement prompt engineering for structured outputs
- Combine traditional ML with LLM predictions (ensemble approach)
- Handle API errors and rate limiting

---

## 🧠 Understanding Large Language Models

### What is an LLM?

**Simple Explanation**: An LLM is like having an extremely well-read assistant who:
- Understands natural language deeply
- Can reason about context and nuances
- Explains their thinking in human language
- Handles complex, ambiguous situations

**SQL Analogy**: 
- **Traditional ML** = `SELECT` with predefined `CASE WHEN` logic
- **LLM** = Having a senior analyst who reads the ticket and applies business intelligence

### Why Add LLM to Our System?

| Traditional ML | LLM (Gemini) | Combined Power |
|---------------|--------------|----------------|
| Fast (milliseconds) | Slower (seconds) | Best of both worlds |
| Works offline | Requires internet | Fallback options |
| Simple patterns | Deep understanding | Confidence-based routing |
| No explanations | Rich reasoning | Audit trails |
| Cheap/free | Costs per call | Smart usage |

### When to Use Which?

```
Simple ticket → Traditional ML → Fast response
   ↓
Complex/ambiguous ticket → LLM → Deep analysis
   ↓
Combine both → Ensemble → Highest confidence wins
```

---

## 📝 Step 1: Understanding the Gemini API

### API Basics

**Gemini Models Available**:
- `gemini-pro` - Best for text analysis (we'll use this)
- `gemini-pro-vision` - For images (not needed for our project)

**Key Concepts**:
- **Prompt**: Your question/instruction to the AI
- **Response**: AI's generated text
- **Temperature**: Creativity level (0 = focused, 1 = creative)
- **Tokens**: Units of text (words/parts of words)

### Your First Gemini API Call

Create `scripts/test_gemini.py`:

```python
"""
Test Google Gemini API Connection
Learn how to make basic LLM API calls
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file!")

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Simple test prompt
test_prompt = """
You are a helpful assistant. Please analyze this customer ticket:

"My internet has been down for 3 days and I've called support twice with no resolution."

What department should handle this? Reply with just the department name.
"""

print("Sending request to Gemini...")
response = model.generate_content(test_prompt)

print("\nGemini Response:")
print(response.text)

print("\nAPI call successful! ✅")
```

**Run the test**:

```powershell
python scripts\test_gemini.py
```

**Expected Output**:
```
Sending request to Gemini...

Gemini Response:
Technical Support

API call successful! ✅
```

### Troubleshooting API Issues

**Error: "API key not valid"**
- Check your .env file has the correct key
- Verify no extra spaces in the key
- Try generating a new key

**Error: "Quota exceeded"**
- Free tier: 60 requests/minute
- Wait a minute and retry
- For production, upgrade to paid tier

**Error: "Connection timeout"**
- Check internet connection
- Try again (temporary network issue)
- Gemini might be experiencing high load

---

## 📝 Step 2: Prompt Engineering for Classification

### The Art of Prompting

**Bad Prompt** (vague):
```
Classify this ticket: "Bill is wrong"
```

**Good Prompt** (structured):
```
You are a Telco call centre AI. Analyze this ticket and respond in JSON format:

Ticket: "Bill is wrong"

Return:
{
  "department": "Billing",
  "sentiment": "Negative",
  "urgency": "Medium",
  "reasoning": "Customer disputes charges..."
}
```

### Creating Our Classification Prompt

Create `src/models/prompts.py`:

```python
"""
LLM Prompts for Ticket Classification
Structured prompts for consistent AI responses
"""


class ClassificationPrompts:
    """
    Collection of prompts for ticket analysis
    
    Think of these like SQL templates with parameters
    """
    
    @staticmethod
    def get_classification_prompt(ticket_text: str) -> str:
        """
        Generate structured classification prompt
        
        Args:
            ticket_text (str): Customer ticket description
            
        Returns:
            str: Formatted prompt for Gemini
        """
        prompt = f"""You are an expert Telco call centre AI assistant with deep knowledge of telecommunications billing, technical support, and customer service.

Analyze the following customer support ticket and classify it according to these categories:

**TICKET TEXT:**
{ticket_text}

**CLASSIFICATION CATEGORIES:**

1. DEPARTMENT (choose ONE):
   - "Technical Support": Network issues, connectivity problems, device troubleshooting, service outages
   - "Billing": Invoice queries, payment issues, charge disputes, account balance
   - "Sales": New services, upgrades, product information, plan changes
   - "Customer Service": Account management, general inquiries, password resets
   - "Retention": Cancellation requests, service complaints, dissatisfaction

2. SENTIMENT (choose ONE):
   - "Positive": Customer is satisfied, grateful, or complimentary
   - "Neutral": Factual inquiry, no strong emotion
   - "Negative": Frustrated, angry, disappointed, or dissatisfied

3. URGENCY (choose ONE):
   - "Low": General inquiry, no immediate impact
   - "Medium": Service affecting one customer, non-critical
   - "High": Service impacting customer significantly, financial concern, multiple issues
   - "Critical": Complete service outage, legal/regulatory issue, severe financial impact, escalated complaint

**RESPONSE FORMAT:**
Return your analysis as a JSON object with this exact structure:

{{
  "department": "<department name>",
  "sentiment": "<sentiment>",
  "urgency": "<urgency level>",
  "reasoning": "<brief explanation of your classification decisions>"
}}

**IMPORTANT GUIDELINES:**
- Consider keywords but also context and tone
- Billing issues mentioning "urgent" or financial impact are HIGH urgency
- Technical outages affecting business are CRITICAL
- Multiple complaints or escalations increase urgency
- Be consistent in your classifications
- Provide clear, concise reasoning

Respond ONLY with the JSON object, no additional text.
"""
        return prompt
    
    @staticmethod
    def get_sentiment_prompt(ticket_text: str) -> str:
        """
        Focused prompt for sentiment analysis only
        
        Args:
            ticket_text (str): Customer ticket description
            
        Returns:
            str: Sentiment-focused prompt
        """
        prompt = f"""Analyze the sentiment of this customer support ticket.

Ticket: "{ticket_text}"

Classify as: Positive, Neutral, or Negative

Consider:
- Emotional tone (anger, gratitude, frustration)
- Word choice (strong negative words, positive language)
- Context (problem severity, impact on customer)

Respond with just the sentiment and a brief reason.

Format:
Sentiment: <Positive|Neutral|Negative>
Reason: <1-2 sentence explanation>
"""
        return prompt
    
    @staticmethod
    def get_urgency_prompt(ticket_text: str) -> str:
        """
        Focused prompt for urgency assessment
        
        Args:
            ticket_text (str): Customer ticket description
            
        Returns:
            str: Urgency-focused prompt
        """
        prompt = f"""Assess the urgency level of this support ticket.

Ticket: "{ticket_text}"

Classify as: Low, Medium, High, or Critical

Consider:
- Service impact (complete outage vs minor issue)
- Business impact (revenue loss, productivity impact)
- Duration (ongoing days vs just started)
- Customer tone (escalation, legal threats)
- Financial implications

Urgency Guidelines:
- LOW: General inquiry, no service impact
- MEDIUM: Single customer affected, service degraded
- HIGH: Significant impact, financial concern, escalated
- CRITICAL: Complete outage, legal issue, severe financial impact

Respond with just the urgency level and reason.

Format:
Urgency: <Low|Medium|High|Critical>
Reason: <1-2 sentence explanation>
"""
        return prompt


# Test the prompts
if __name__ == "__main__":
    test_ticket = "Internet has been down for 3 days. Called twice, no resolution. Business severely impacted."
    
    prompt = ClassificationPrompts.get_classification_prompt(test_ticket)
    
    print("Generated Prompt:")
    print("=" * 80)
    print(prompt)
    print("=" * 80)
    
    print("\nPrompt length:", len(prompt), "characters")
    print("Estimated tokens:", len(prompt) // 4)  # Rough estimate: 1 token ≈ 4 chars
```

**Run the test**:

```powershell
python src\models\prompts.py
```

---

## 📝 Step 3: Building the Enhanced Classifier

### Architecture Overview

```
Customer Ticket
    ↓
┌─────────────────────────────────────┐
│   Enhanced Classifier (Orchestrator) │
└───────────┬─────────────────────────┘
            │
    ┌───────┴────────┐
    ↓                ↓
┌─────────────┐  ┌──────────────┐
│ Traditional │  │  Gemini LLM  │
│     ML      │  │              │
└──────┬──────┘  └──────┬───────┘
       │                │
       └────────┬────────┘
                ↓
        Ensemble Decision
        (highest confidence)
                ↓
          Final Result
```

### Complete Enhanced Classifier Implementation

Create `src/models/enhanced_classifier.py`:

```python
"""
Enhanced Classifier with Gemini LLM Integration
Combines traditional ML with advanced LLM reasoning
"""

import os
import json
import re
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv

import google.generativeai as genai
from src.models.traditional_classifier import TraditionalClassifier
from src.models.prompts import ClassificationPrompts


@dataclass
class ClassificationResult:
    """
    Structured result from classification
    
    Like a result set from a complex SQL query with multiple columns
    """
    department: str
    sentiment: str
    urgency: str
    confidence: str  # 'high', 'medium', 'low'
    method: str  # 'traditional_ml', 'llm', 'ensemble'
    department_reasoning: Optional[str] = None
    sentiment_reasoning: Optional[str] = None
    urgency_reasoning: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for easy serialization"""
        return {
            'department': self.department,
            'sentiment': self.sentiment,
            'urgency': self.urgency,
            'confidence': self.confidence,
            'method': self.method,
            'department_reasoning': self.department_reasoning,
            'sentiment_reasoning': self.sentiment_reasoning,
            'urgency_reasoning': self.urgency_reasoning
        }


class GeminiEnhancedClassifier:
    """
    Intelligent ticket classifier combining ML + LLM
    
    Strategy:
    1. Try traditional ML first (fast, offline)
    2. If uncertain OR LLM enabled, get Gemini analysis
    3. Combine predictions using ensemble logic
    4. Return result with reasoning
    """
    
    def __init__(self, use_llm: bool = True, llm_model: str = 'gemini-pro'):
        """
        Initialize the enhanced classifier
        
        Args:
            use_llm (bool): Whether to use Gemini LLM
            llm_model (str): Which Gemini model to use
        """
        # Load environment variables
        load_dotenv()
        
        # Initialize traditional ML model
        self.traditional_classifier = TraditionalClassifier()
        
        try:
            # Load pre-trained traditional model
            self.traditional_classifier.load()
            print("✅ Traditional ML model loaded")
        except Exception as e:
            print(f"⚠️  Could not load traditional model: {e}")
            print("   Traditional classification will not be available")
        
        # Initialize Gemini LLM if enabled
        self.use_llm = use_llm
        self.llm_available = False
        
        if self.use_llm:
            try:
                api_key = os.getenv('GOOGLE_API_KEY')
                if not api_key:
                    print("⚠️  GOOGLE_API_KEY not found in environment")
                    print("   LLM analysis will not be available")
                else:
                    genai.configure(api_key=api_key)
                    self.llm_model = genai.GenerativeModel(llm_model)
                    self.llm_available = True
                    print(f"✅ Gemini LLM ({llm_model}) initialized")
            except Exception as e:
                print(f"⚠️  Could not initialize Gemini: {e}")
                print("   LLM analysis will not be available")
    
    def classify_ticket(self, ticket_text: str, force_llm: bool = False) -> ClassificationResult:
        """
        Main classification method - orchestrates all prediction sources
        
        Args:
            ticket_text (str): Customer ticket description
            force_llm (bool): Force use of LLM even if traditional ML available
            
        Returns:
            ClassificationResult: Complete classification with reasoning
        """
        # Strategy 1: Try traditional ML first (if not forced to use LLM)
        traditional_prediction = None
        if not force_llm and self.traditional_classifier.is_trained:
            try:
                traditional_prediction = self.traditional_classifier.predict(ticket_text)
                print(f"📊 Traditional ML prediction: {traditional_prediction}")
            except Exception as e:
                print(f"⚠️  Traditional ML failed: {e}")
        
        # Strategy 2: Get LLM analysis if available
        llm_analysis = None
        if self.llm_available and (force_llm or self.use_llm):
            try:
                llm_analysis = self._get_llm_classification(ticket_text)
                print(f"🤖 LLM analysis complete")
            except Exception as e:
                print(f"⚠️  LLM analysis failed: {e}")
        
        # Strategy 3: Ensemble - combine predictions
        return self._ensemble_predictions(
            ticket_text=ticket_text,
            traditional_prediction=traditional_prediction,
            llm_analysis=llm_analysis
        )
    
    def _get_llm_classification(self, ticket_text: str) -> Dict:
        """
        Get classification from Gemini LLM
        
        Args:
            ticket_text (str): Ticket description
            
        Returns:
            dict: Parsed LLM response with classifications
        """
        # Generate prompt
        prompt = ClassificationPrompts.get_classification_prompt(ticket_text)
        
        # Call Gemini API
        response = self.llm_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,  # Low temperature for consistent classifications
                max_output_tokens=500
            )
        )
        
        # Parse JSON response
        response_text = response.text.strip()
        
        # Extract JSON (handle cases where LLM adds extra text)
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group()
            analysis = json.loads(json_text)
            return analysis
        else:
            raise ValueError(f"Could not parse JSON from LLM response: {response_text}")
    
    def _ensemble_predictions(
        self, 
        ticket_text: str,
        traditional_prediction: Optional[str],
        llm_analysis: Optional[Dict]
    ) -> ClassificationResult:
        """
        Combine predictions from different sources
        
        Decision Logic:
        1. If only one source available, use it
        2. If both agree, high confidence
        3. If disagree, prefer LLM (deeper understanding)
        4. Include reasoning from LLM
        
        Args:
            ticket_text (str): Original ticket
            traditional_prediction (str|None): ML prediction
            llm_analysis (dict|None): LLM analysis
            
        Returns:
            ClassificationResult: Final ensemble prediction
        """
        # Case 1: Only traditional ML available
        if traditional_prediction and not llm_analysis:
            return ClassificationResult(
                department=traditional_prediction,
                sentiment="Neutral",  # Default
                urgency="Medium",     # Default
                confidence='medium',
                method='traditional_ml',
                department_reasoning="Classification based on traditional ML model"
            )
        
        # Case 2: Only LLM available
        if llm_analysis and not traditional_prediction:
            return ClassificationResult(
                department=llm_analysis.get('department', 'Customer Service'),
                sentiment=llm_analysis.get('sentiment', 'Neutral'),
                urgency=llm_analysis.get('urgency', 'Medium'),
                confidence='high',
                method='llm',
                department_reasoning=llm_analysis.get('reasoning'),
                sentiment_reasoning=llm_analysis.get('reasoning'),
                urgency_reasoning=llm_analysis.get('reasoning')
            )
        
        # Case 3: Both available - ensemble decision
        if traditional_prediction and llm_analysis:
            llm_department = llm_analysis.get('department', 'Customer Service')
            
            # Check agreement
            agreement = (traditional_prediction == llm_department)
            
            if agreement:
                # Both agree - high confidence
                confidence = 'high'
                method = 'ensemble_agreement'
            else:
                # Disagree - prefer LLM, medium confidence
                confidence = 'medium'
                method = 'ensemble_llm_preferred'
            
            return ClassificationResult(
                department=llm_department,  # Prefer LLM department
                sentiment=llm_analysis.get('sentiment', 'Neutral'),
                urgency=llm_analysis.get('urgency', 'Medium'),
                confidence=confidence,
                method=method,
                department_reasoning=llm_analysis.get('reasoning'),
                sentiment_reasoning=llm_analysis.get('reasoning'),
                urgency_reasoning=llm_analysis.get('reasoning')
            )
        
        # Case 4: No predictions available (error fallback)
        return ClassificationResult(
            department='Customer Service',  # Safe default
            sentiment='Neutral',
            urgency='Medium',
            confidence='low',
            method='fallback',
            department_reasoning="No classification models available, using default routing"
        )


# Test the enhanced classifier
if __name__ == "__main__":
    print("=" * 80)
    print("ENHANCED CLASSIFIER TEST")
    print("=" * 80)
    
    # Initialize classifier
    classifier = GeminiEnhancedClassifier(use_llm=True)
    
    # Test tickets
    test_tickets = [
        "Internet has been down for 3 days. Multiple calls, no resolution. Business severely impacted.",
        "Please explain charges on last month's invoice.",
        "Interested in upgrading to fiber. What packages are available?",
        "Cancelling service due to poor quality and high costs. Very disappointed.",
    ]
    
    for i, ticket in enumerate(test_tickets, 1):
        print(f"\n{'=' * 80}")
        print(f"TEST {i}: {ticket}")
        print('=' * 80)
        
        result = classifier.classify_ticket(ticket)
        
        print(f"\n🎯 RESULTS:")
        print(f"  Department: {result.department}")
        print(f"  Sentiment: {result.sentiment}")
        print(f"  Urgency: {result.urgency}")
        print(f"  Confidence: {result.confidence}")
        print(f"  Method: {result.method}")
        
        if result.department_reasoning:
            print(f"\n💡 REASONING:")
            print(f"  {result.department_reasoning}")
```

**Run the test**:

```powershell
python src\models\enhanced_classifier.py
```

### Understanding Ensemble Logic

**SQL Analogy**: Like having two analysts review a case:

```sql
SELECT 
    CASE 
        WHEN analyst1_opinion = analyst2_opinion THEN 'HIGH_CONFIDENCE'
        WHEN analyst2_is_senior THEN analyst2_opinion
        ELSE analyst1_opinion
    END as final_decision,
    CASE
        WHEN analyst1_opinion = analyst2_opinion THEN 'AGREEMENT'
        ELSE 'ANALYST2_PREFERRED'
    END as decision_method
FROM ticket_analysis
```

---

## ✅ Phase 3 Checkpoint

**Verify you can:**
- [ ] Make successful Gemini API calls
- [ ] Create structured prompts for classification
- [ ] Parse JSON responses from LLM
- [ ] Combine traditional ML + LLM predictions
- [ ] Handle API errors gracefully

**Test your understanding:**
1. What happens if the Gemini API is down?
2. Why do we prefer LLM when predictions disagree?
3. When would you use traditional ML only?
4. How does temperature affect LLM responses?

**Common Issues:**
- **"API quota exceeded"**: Free tier limits, wait or upgrade
- **"JSON parse error"**: LLM response format changed, update regex
- **"Model not found"**: Check model name is 'gemini-pro'
- **"Poor classifications"**: Refine prompts, add more examples

---

## 🎓 Key Learnings

1. **LLMs are powerful but expensive** - Use strategically
2. **Prompts are crucial** - Good prompts = good results
3. **Ensemble improves reliability** - Multiple sources better than one
4. **Always have fallbacks** - System must work when LLM fails
5. **Structured outputs** - JSON format enables programmatic use

---

**Next**: Phase 4 - Building the Interactive Web UI with Streamlit

---

*Phase 3 Tutorial - Created by Technical Writer Agent + Data Scientist Agent*
*Part of the Agentic AI Framework Comprehensive Tutorial Series*
