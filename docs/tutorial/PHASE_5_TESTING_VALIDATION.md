# Phase 5: Testing & Validation Strategy

**Estimated Time**: 6-8 hours  
**Prerequisites**: Phases 1-4 completed, working end-to-end system  
**File References**: 
- `tests/test_enhanced_classifier.py` (210 lines)
- `tests/test_departmental_routing.py` (125 lines)
- `tests/test_html_cleaning.py` (69 lines)

---

## Overview

Phase 5 covers **production-grade testing strategies** for ML systems. This isn't about basic "does it run?" testing—it's comprehensive validation covering unit tests, integration tests, ML-specific testing patterns, performance benchmarking, and continuous quality monitoring.

### What You'll Learn

- pytest framework architecture and advanced features
- ML model testing patterns (accuracy, drift, bias)
- Integration testing for multi-component systems
- Mock/stub strategies for external APIs (Gemini)
- Test data generation and synthetic ticket creation
- Performance benchmarking and regression detection
- CI/CD pipeline integration
- Production monitoring strategies

---

## Why Testing ML Systems Is Different

### Traditional Software vs ML Systems

**Traditional Software Testing:**
```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5  # Deterministic, always true
```

**ML System Testing:**
```python
def classify_ticket(text):
    return model.predict(text)

def test_classify():
    result = classify_ticket("My bill is too high")
    # NOT deterministic!
    # Could be BILLING, COMPLAINTS, ACCOUNT_MGMT
    # Depends on: model version, training data, random seeds
    assert result in VALID_CATEGORIES  # Can only test properties
```

### Key Differences

1. **Non-Deterministic Outputs**: ML models don't return the same result every time
2. **Confidence Thresholds**: Must test probabilistic outputs, not exact matches
3. **Data Distribution Sensitivity**: Performance depends on input data distribution
4. **Model Drift**: Models degrade over time as real-world data changes
5. **External Dependencies**: LLM APIs (Gemini) add latency and failure modes
6. **Performance Variability**: Response times vary (network, API load, model size)

---

## Testing Architecture

### Test Organization

```
tests/
├── unit/                           # Fast, isolated component tests
│   ├── test_text_preprocessing.py
│   ├── test_feature_extraction.py
│   └── test_model_loading.py
│
├── integration/                    # Multi-component tests
│   ├── test_enhanced_classifier.py  # Full classification pipeline
│   ├── test_departmental_routing.py # Routing + dispute detection
│   └── test_html_cleaning.py       # Sanitization pipeline
│
├── performance/                    # Benchmark tests
│   ├── test_latency.py
│   ├── test_throughput.py
│   └── test_memory_usage.py
│
├── fixtures/                       # Shared test data
│   ├── sample_tickets.json
│   ├── mock_responses.py
│   └── test_datasets.py
│
└── conftest.py                     # pytest configuration
```

### Test Pyramid for ML Systems

```
         ┌─────────────────┐
         │  E2E/UI Tests   │  10% - Slow, brittle, high-value
         │   (Selenium)    │
         └─────────────────┘
        ┌───────────────────┐
        │ Integration Tests │  30% - Medium speed, validate workflows
        │  (API + Model)    │
        └───────────────────┘
       ┌──────────────────────┐
       │    Unit Tests        │  60% - Fast, isolated, low-level
       │  (Functions/Classes) │
       └──────────────────────┘
```

---

## Test Suite Deep Dive

### 1. Enhanced Classifier Integration Test

**File**: `tests/test_enhanced_classifier.py` (210 lines)

#### Test Structure

```python
#!/usr/bin/env python3
"""
Enhanced Classifier Test Suite
Comprehensive testing for Google Gemini LLM integration
"""

import os
import sys
import logging
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

**Path Management Pattern:**

Every test file starts with path manipulation. **Why?**

- Tests run from different directories: `pytest`, `python -m pytest`, IDE test runners
- Import paths must work regardless of execution context
- `Path(__file__).parent.parent` gets project root dynamically
- Alternative: Use `pytest` fixture for project root (more complex but cleaner)

#### Test Function: Classifier Initialization

**Lines 20-42**:
```python
def test_enhanced_classifier():
    """Test the enhanced classifier with mock API key."""
    print("🧪 Enhanced Classifier Test Suite")
    print("=" * 50)
    
    try:
        from src.models.enhanced_classifier import GeminiEnhancedClassifier
        print("✅ Enhanced classifier module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import enhanced classifier: {e}")
        return False
```

**Testing Pattern: Import Validation**

**Why Test Imports?**
- Catches circular dependencies early
- Validates project structure and PYTHONPATH
- Ensures all dependencies are installed
- Common failure point in production environments

**Better Pattern** (production tests):
```python
def test_classifier_import():
    """Test that classifier module can be imported."""
    try:
        from src.models.enhanced_classifier import GeminiEnhancedClassifier
        assert GeminiEnhancedClassifier is not None
    except ImportError as e:
        pytest.fail(f"Failed to import classifier: {e}")
```

Using `pytest.fail()` provides better error reporting than `return False`.

#### Test Function: Mock API Key Handling

**Lines 45-54**:
```python
try:
    # This will fail without real API key, but tests import structure
    classifier = GeminiEnhancedClassifier(api_key="test_key_mock")
    print("❌ Expected: Should fail with mock API key")
    return False
except Exception as e:
    print(f"✅ Expected error with mock API key: {type(e).__name__}")
```

**Testing Pattern: Negative Testing**

**What This Tests:**
- API key validation logic exists
- System fails gracefully with invalid credentials
- Error messages are informative

**Better Pattern** (specific exception):
```python
def test_invalid_api_key():
    """Test that invalid API key raises appropriate error."""
    with pytest.raises(ValueError, match="Invalid API key"):
        GeminiEnhancedClassifier(api_key="invalid_key")
```

**Why `pytest.raises`?**
- Validates specific exception type
- Can match error message with regex
- Clearer test intent
- Better failure messages

#### Test Data Structure

**Lines 63-71**:
```python
test_tickets = [
    "My internet bill is too high this month, please help me understand the charges",
    "WiFi keeps disconnecting every few minutes, very frustrating", 
    "I want to upgrade to a faster internet package for my home office",
    "The customer service agent was very rude and unhelpful",
    "No mobile signal in Sandton area since yesterday",
    "I need to update my billing address as I'm moving next month",
    "Hello, I just wanted to say thank you for your service"
]

expected_categories = ["BILLING", "TECHNICAL", "SALES", "COMPLAINTS", "NETWORK", "ACCOUNT", "OTHER"]
```

**Test Data Design Principles:**

1. **Coverage**: Each category represented
2. **Ambiguity**: Some tickets have multiple valid categories
3. **Edge Cases**: Polite/positive ticket (last one) tests OTHER category
4. **Real-World**: Actual customer language patterns
5. **Diversity**: Different lengths, sentiments, complexity levels

**Better Pattern** (parameterized tests):
```python
import pytest

@pytest.mark.parametrize("ticket,expected_category", [
    ("My internet bill is too high", "BILLING"),
    ("WiFi keeps disconnecting", "TECHNICAL"),
    ("I want to upgrade to fibre", "SALES"),
])
def test_classification_accuracy(ticket, expected_category):
    """Test classification for known tickets."""
    classifier = GeminiEnhancedClassifier()
    result = classifier.classify_ticket(ticket)
    assert result.predicted_category == expected_category
```

**Benefits:**
- Each test case runs independently
- Failures show which specific ticket failed
- Easy to add new test cases
- Better test reporting

---

### 2. Departmental Routing Test

**File**: `tests/test_departmental_routing.py` (125 lines)

This test validates the **business logic layer**—departmental routing, dispute detection, and HITL requirements.

#### Test Case Structure

**Lines 25-52**:
```python
test_cases = [
    {
        'ticket': 'I dispute this R500 charge on my bill - I never authorized this premium service',
        'expected_dept': 'CREDIT_MGMT',
        'expected_dispute': True,
        'description': 'Clear billing dispute'
    },
    {
        'ticket': 'Can you please explain why my bill is R200 higher than last month?',
        'expected_dept': 'BILLING', 
        'expected_dispute': False,
        'description': 'General billing inquiry'
    },
    # ... more cases
]
```

**Test Design: Expected vs Actual**

Each test case specifies:
- **Input**: Customer ticket text
- **Expected Output**: Department, dispute flag
- **Description**: Human-readable test intent

**Why This Structure?**

1. **Readability**: Non-programmers (PO, BA) can understand test cases
2. **Maintainability**: Easy to add new scenarios
3. **Debugging**: Description shows what test is validating
4. **Regression**: Prevents breaking existing routing logic

#### Assertion Logic

**Lines 77-83**:
```python
# Check accuracy
dept_correct = result.department_allocation == case['expected_dept']
dispute_correct = result.dispute_detected == case['expected_dispute']

print(f"✅ Department Correct: {dept_correct}")
print(f"✅ Dispute Detection Correct: {dispute_correct}")
```

**Testing Pattern: Property Validation**

Not testing exact outputs (non-deterministic), but **properties**:
- Department is one of valid departments
- Dispute detection is boolean
- Routing confidence is 0.0-1.0
- Priority level matches department + sentiment logic

#### Accuracy Metrics

**Lines 91-95**:
```python
# Summary
dept_accuracy = sum(r['dept_correct'] for r in results) / len(results)
dispute_accuracy = sum(r['dispute_correct'] for r in results) / len(results)

print(f"Department Routing Accuracy: {dept_accuracy:.1%}")
print(f"Dispute Detection Accuracy: {dispute_accuracy:.1%}")
```

**ML Testing Pattern: Aggregate Metrics**

Individual predictions may vary, but **aggregate accuracy** must meet thresholds:
```python
def test_routing_accuracy_threshold():
    """Test that routing accuracy exceeds minimum threshold."""
    classifier = GeminiEnhancedClassifier()
    results = [classifier.classify_ticket(t) for t in test_tickets]
    accuracy = calculate_accuracy(results, expected_labels)
    
    # Production SLA: 85% minimum accuracy
    assert accuracy >= 0.85, f"Accuracy {accuracy:.1%} below threshold"
```

**Why Thresholds?**
- ML models aren't 100% accurate
- Some tickets are genuinely ambiguous
- Acceptable error rate depends on business impact
- Track accuracy over time (drift detection)

---

### 3. HTML Sanitization Test

**File**: `tests/test_html_cleaning.py` (69 lines)

This test validates **security-critical** sanitization logic.

#### Test Execution

**Lines 17-28**:
```python
# Create classifier
classifier = GeminiEnhancedClassifier()

# Test the problematic ticket
ticket_text = '''Customer called to complain about slow internet connection...'''

# Classify the ticket
result = classifier.classify_ticket(ticket_text)

print(f'First 300 characters: {repr(result.sentiment_reasoning[:300])}')
```

**Testing Pattern: Observational Testing**

This test **observes** output rather than asserting. **Why?**

- HTML from Gemini is non-deterministic (sometimes appears, sometimes doesn't)
- Cleaning pipeline should handle HTML **if present**
- Test validates: no HTML in output, regardless of input

**Better Pattern** (with assertions):
```python
def test_html_cleaning():
    """Test that HTML is removed from sentiment reasoning."""
    classifier = GeminiEnhancedClassifier()
    result = classifier.classify_ticket("Test ticket")
    
    reasoning = result.sentiment_reasoning
    
    # Assert no HTML tags present
    assert '<' not in reasoning, f"Found < in: {repr(reasoning)}"
    assert '>' not in reasoning, f"Found > in: {repr(reasoning)}"
    assert '&lt;' not in reasoning, f"Found &lt; in: {repr(reasoning)}"
    assert '&gt;' not in reasoning, f"Found &gt; in: {repr(reasoning)}"
    
    # Assert no common HTML tags
    assert '<p>' not in reasoning.lower()
    assert '<strong>' not in reasoning.lower()
    assert '</p>' not in reasoning.lower()
```

#### Security Testing Checklist

**Lines 37-47**:
```python
# Check for HTML tags
has_p_tag = '<p>' in result.sentiment_reasoning
has_strong_tag = '<strong>' in result.sentiment_reasoning
has_closing_p = '</p>' in result.sentiment_reasoning
has_closing_strong = '</strong>' in result.sentiment_reasoning
has_any_html = '<' in result.sentiment_reasoning or '>' in result.sentiment_reasoning

print(f'Contains <p>: {has_p_tag}')
print(f'Contains <strong>: {has_strong_tag}')
```

**Testing Pattern: Multi-Level Validation**

Checks multiple HTML patterns:
1. **Opening tags**: `<p>`, `<strong>`
2. **Closing tags**: `</p>`, `</strong>`
3. **Any angle brackets**: `<`, `>`

**Why Multiple Checks?**
- Defense in depth (multiple sanitization layers)
- Catch partial cleaning failures
- Validate each layer of pipeline

**Security Test Extension**:
```python
@pytest.mark.parametrize("malicious_input", [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "&#x3C;script&#x3E;",  # HTML entity encoded
    "<p><strong>Bold text</strong></p>",
    "Text with <tag> in middle",
])
def test_xss_prevention(malicious_input):
    """Test that potential XSS inputs are sanitized."""
    classifier = GeminiEnhancedClassifier()
    # Inject malicious content into reasoning (simulated)
    result = classifier.classify_ticket(malicious_input)
    
    reasoning = result.sentiment_reasoning
    
    # Verify no script tags survive
    assert '<script>' not in reasoning.lower()
    assert 'onerror=' not in reasoning.lower()
    assert '<' not in reasoning
```

---

## Advanced Testing Patterns

### 1. Mocking External APIs

**Problem**: Tests calling real Gemini API are:
- Slow (1-3 seconds per call)
- Expensive (API costs money)
- Flaky (network issues, rate limits)
- Non-deterministic (responses vary)

**Solution**: Mock the API for unit tests

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_gemini_response():
    """Fixture providing mock Gemini API response."""
    return {
        'category': 'BILLING',
        'confidence': 0.89,
        'reasoning': 'Customer is asking about billing charges.',
        'sentiment': 'NEGATIVE',
        'sentiment_score': -0.6
    }

@patch('google.generativeai.GenerativeModel')
def test_classification_with_mock(mock_model, mock_gemini_response):
    """Test classification logic without calling real API."""
    # Setup mock
    mock_instance = Mock()
    mock_instance.generate_content.return_value.text = json.dumps(mock_gemini_response)
    mock_model.return_value = mock_instance
    
    # Test
    classifier = GeminiEnhancedClassifier()
    result = classifier.classify_ticket("My bill is too high")
    
    # Validate
    assert result.predicted_category == 'BILLING'
    assert result.confidence == 0.89
    assert mock_instance.generate_content.called
```

**Benefits:**
- Tests run in milliseconds (not seconds)
- No API costs
- Deterministic results
- Validate error handling (mock failures)

**When to Mock vs Real API:**
- **Unit tests**: Always mock
- **Integration tests**: Mix (mock for speed, real for validation)
- **E2E tests**: Real API (validate full pipeline)

---

### 2. Test Fixtures and Data Management

**Problem**: Test data management becomes complex with many tests.

**Solution**: pytest fixtures

```python
# conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture(scope="session")
def test_tickets():
    """Load test tickets from JSON file."""
    fixture_path = Path(__file__).parent / "fixtures" / "sample_tickets.json"
    with open(fixture_path) as f:
        return json.load(f)

@pytest.fixture(scope="session")
def classifier():
    """Create classifier instance once per test session."""
    return GeminiEnhancedClassifier()

@pytest.fixture
def temp_output_dir(tmp_path):
    """Provide temporary directory for test outputs."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    return output_dir

# Usage in tests
def test_batch_classification(classifier, test_tickets, temp_output_dir):
    """Test classifying multiple tickets."""
    results = []
    for ticket in test_tickets[:10]:  # First 10 tickets
        result = classifier.classify_ticket(ticket['text'])
        results.append(result)
    
    # Save results for analysis
    output_file = temp_output_dir / "batch_results.json"
    output_file.write_text(json.dumps(results))
    
    assert len(results) == 10
```

**Fixture Scopes:**
- `function` (default): New fixture per test function
- `class`: New fixture per test class
- `module`: New fixture per test file
- `session`: One fixture for entire test run

**When to Use Each:**
- `function`: Unique test data, mutable state
- `session`: Expensive setup (model loading, DB connections)

---

### 3. Property-Based Testing

**Problem**: Hard to test all edge cases with example-based tests.

**Solution**: Property-based testing with `hypothesis`

```python
from hypothesis import given, strategies as st
import pytest

@given(st.text(min_size=10, max_size=500))
def test_classification_never_crashes(ticket_text):
    """Test that classifier handles any text input without crashing."""
    classifier = GeminiEnhancedClassifier()
    
    try:
        result = classifier.classify_ticket(ticket_text)
        
        # Verify result has expected properties
        assert result.predicted_category in VALID_CATEGORIES
        assert 0.0 <= result.confidence <= 1.0
        assert result.processing_time_ms > 0
    except Exception as e:
        pytest.fail(f"Classifier crashed on input {repr(ticket_text)}: {e}")

@given(st.lists(st.text(), min_size=1, max_size=100))
def test_batch_classification_consistency(tickets):
    """Test that batch classification is consistent."""
    classifier = GeminiEnhancedClassifier()
    
    # Classify same tickets twice
    results1 = [classifier.classify_ticket(t) for t in tickets]
    results2 = [classifier.classify_ticket(t) for t in tickets]
    
    # Results should be similar (allowing for LLM variability)
    for r1, r2 in zip(results1, results2):
        # Category might differ slightly due to LLM, but confidence should be similar
        assert abs(r1.confidence - r2.confidence) < 0.2
```

**Hypothesis Benefits:**
- Generates hundreds of test cases automatically
- Finds edge cases you wouldn't think of
- Shrinks failing examples to minimal reproducible case

---

### 4. Performance Regression Testing

**Problem**: Code changes might slow down classification.

**Solution**: Benchmark tests with thresholds

```python
import pytest
import time

def test_classification_latency():
    """Test that classification completes within acceptable time."""
    classifier = GeminiEnhancedClassifier()
    ticket = "My internet is not working properly"
    
    start_time = time.time()
    result = classifier.classify_ticket(ticket)
    elapsed_ms = (time.time() - start_time) * 1000
    
    # SLA: 95th percentile should be under 3 seconds
    assert elapsed_ms < 3000, f"Classification took {elapsed_ms:.0f}ms (exceeds 3000ms SLA)"
    
    # Verify result metadata matches
    assert abs(result.processing_time_ms - elapsed_ms) < 100  # Within 100ms

@pytest.mark.benchmark
def test_throughput(benchmark):
    """Benchmark classification throughput."""
    classifier = GeminiEnhancedClassifier()
    ticket = "Sample ticket for benchmarking"
    
    # pytest-benchmark plugin
    result = benchmark(classifier.classify_ticket, ticket)
    
    # Verify minimum throughput
    # Should handle at least 10 requests per minute (allowing for API latency)
    assert benchmark.stats['mean'] < 6.0  # 6 seconds max per request

def test_memory_usage():
    """Test that classifier doesn't leak memory."""
    import tracemalloc
    
    tracemalloc.start()
    
    classifier = GeminiEnhancedClassifier()
    
    # Classify many tickets
    for _ in range(100):
        classifier.classify_ticket("Test ticket")
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Memory should stay under 500MB for 100 classifications
    assert peak < 500 * 1024 * 1024, f"Peak memory usage: {peak / 1024 / 1024:.1f}MB"
```

---

## Test Data Generation

### Synthetic Ticket Generation

**Problem**: Need diverse test data at scale.

**Solution**: Generate synthetic tickets programmatically

```python
import random
from typing import List, Dict

class TicketGenerator:
    """Generate synthetic customer support tickets."""
    
    TEMPLATES = {
        'BILLING': [
            "My bill is {amount} higher than usual, why is this?",
            "I was charged {amount} for {service} that I didn't order",
            "Please explain the {charge_type} charge on my account",
            "I dispute the {amount} charge from {date}",
        ],
        'TECHNICAL': [
            "My {service} has been {issue} for {duration}",
            "{service} keeps {problem} every few minutes",
            "I'm experiencing {issue} with my {service}",
            "Can't {action} because of {problem}",
        ],
        'SALES': [
            "I want to upgrade to {product}",
            "What are the pricing options for {service}?",
            "I'd like to add {feature} to my plan",
            "How much does {product} cost?",
        ],
    }
    
    VARIABLES = {
        'amount': ['R500', 'R200', 'R1000', '50 rand'],
        'service': ['internet', 'WiFi', 'mobile data', 'landline'],
        'issue': ['not working', 'disconnecting', 'slow', 'down'],
        'duration': ['2 days', '3 hours', 'a week', 'since yesterday'],
        'problem': ['disconnecting', 'buffering', 'dropping calls'],
        'action': ['connect', 'stream videos', 'make calls'],
        'product': ['fibre', '5G', 'premium package'],
        'feature': ['international calling', 'more data'],
        'charge_type': ['service', 'installation', 'premium'],
        'date': ['last month', 'yesterday', 'last week'],
    }
    
    def generate_ticket(self, category: str, sentiment: str = 'NEUTRAL') -> Dict:
        """Generate a single synthetic ticket."""
        template = random.choice(self.TEMPLATES[category])
        
        # Replace variables
        ticket_text = template
        for var, options in self.VARIABLES.items():
            if f'{{{var}}}' in ticket_text:
                ticket_text = ticket_text.replace(f'{{{var}}}', random.choice(options))
        
        # Add sentiment modifiers
        if sentiment == 'NEGATIVE':
            ticket_text = self._add_negative_sentiment(ticket_text)
        elif sentiment == 'CRITICAL':
            ticket_text = self._add_critical_sentiment(ticket_text)
        
        return {
            'text': ticket_text,
            'expected_category': category,
            'expected_sentiment': sentiment,
        }
    
    def _add_negative_sentiment(self, text: str) -> str:
        """Add negative sentiment to ticket."""
        prefixes = [
            "This is very frustrating - ",
            "I'm not happy about this: ",
            "This is unacceptable: ",
        ]
        suffixes = [
            " This is causing me problems.",
            " Please fix this ASAP.",
            " I'm very disappointed.",
        ]
        return random.choice(prefixes) + text + random.choice(suffixes)
    
    def _add_critical_sentiment(self, text: str) -> str:
        """Add critical sentiment to ticket."""
        prefixes = [
            "This is ABSOLUTELY TERRIBLE! ",
            "I am FURIOUS! ",
            "This is completely unacceptable - ",
        ]
        suffixes = [
            " I want a refund immediately!",
            " I'm cancelling my account!",
            " This is the worst service I've ever experienced!",
        ]
        return random.choice(prefixes) + text + random.choice(suffixes)
    
    def generate_dataset(self, size: int) -> List[Dict]:
        """Generate a full test dataset."""
        categories = list(self.TEMPLATES.keys())
        sentiments = ['NEUTRAL', 'NEGATIVE', 'CRITICAL']
        
        dataset = []
        for _ in range(size):
            category = random.choice(categories)
            sentiment = random.choice(sentiments)
            ticket = self.generate_ticket(category, sentiment)
            dataset.append(ticket)
        
        return dataset

# Usage
def test_with_synthetic_data():
    """Test classifier on large synthetic dataset."""
    generator = TicketGenerator()
    test_data = generator.generate_dataset(100)
    
    classifier = GeminiEnhancedClassifier()
    
    correct_categories = 0
    correct_sentiments = 0
    
    for ticket in test_data:
        result = classifier.classify_ticket(ticket['text'])
        
        if result.predicted_category == ticket['expected_category']:
            correct_categories += 1
        
        if result.sentiment_label == ticket['expected_sentiment']:
            correct_sentiments += 1
    
    category_accuracy = correct_categories / len(test_data)
    sentiment_accuracy = correct_sentiments / len(test_data)
    
    print(f"Category Accuracy: {category_accuracy:.1%}")
    print(f"Sentiment Accuracy: {sentiment_accuracy:.1%}")
    
    # Minimum acceptable accuracy
    assert category_accuracy >= 0.75
    assert sentiment_accuracy >= 0.70
```

---

## CI/CD Integration

### GitHub Actions Workflow

**File**: `.github/workflows/test.yml`

```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
        pip install pytest pytest-cov pytest-benchmark
    
    - name: Run unit tests
      run: |
        pytest tests/unit -v --cov=src --cov-report=xml
    
    - name: Run integration tests
      env:
        GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
      run: |
        pytest tests/integration -v --cov=src --cov-append
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
    
    - name: Run benchmarks
      run: |
        pytest tests/performance --benchmark-only
```

**Key Features:**
- **Matrix testing**: Test on multiple Python versions
- **Code coverage**: Track test coverage over time
- **Secrets management**: API keys stored securely
- **Performance tracking**: Benchmark results on every commit

---

## ML-Specific Testing Patterns

### 1. Model Accuracy Monitoring

```python
def test_model_accuracy_threshold():
    """Test that model maintains minimum accuracy on validation set."""
    import pandas as pd
    
    # Load labeled validation data
    validation_data = pd.read_csv('tests/fixtures/validation_set.csv')
    
    classifier = GeminiEnhancedClassifier()
    
    predictions = []
    actuals = []
    
    for _, row in validation_data.iterrows():
        result = classifier.classify_ticket(row['ticket_text'])
        predictions.append(result.predicted_category)
        actuals.append(row['actual_category'])
    
    # Calculate accuracy
    from sklearn.metrics import accuracy_score, classification_report
    accuracy = accuracy_score(actuals, predictions)
    
    print(classification_report(actuals, predictions))
    
    # Production SLA: Minimum 85% accuracy
    assert accuracy >= 0.85, f"Model accuracy {accuracy:.1%} below 85% threshold"
```

### 2. Bias Detection

```python
def test_sentiment_bias():
    """Test that sentiment analysis isn't biased by specific words."""
    classifier = GeminiEnhancedClassifier()
    
    # Test tickets with same content but different styling
    tickets = [
        "My internet bill is too high",  # Neutral
        "My internet bill is WAY TOO HIGH",  # Emphasis
        "My internet bill is too high!!!",  # Punctuation
    ]
    
    results = [classifier.classify_ticket(t) for t in tickets]
    
    # All should have similar sentiment (not swayed by styling)
    sentiments = [r.sentiment_label for r in results]
    assert len(set(sentiments)) <= 2, f"Inconsistent sentiments: {sentiments}"
```

### 3. Drift Detection

```python
def test_no_model_drift():
    """Test that model predictions haven't drifted from baseline."""
    import json
    
    # Load baseline predictions (from previous model version)
    with open('tests/fixtures/baseline_predictions.json') as f:
        baseline = json.load(f)
    
    classifier = GeminiEnhancedClassifier()
    
    # Re-classify same tickets
    drift_count = 0
    for ticket_id, baseline_pred in baseline.items():
        result = classifier.classify_ticket(baseline_pred['ticket'])
        
        # Allow small confidence changes, but category should be stable
        if result.predicted_category != baseline_pred['category']:
            drift_count += 1
    
    drift_rate = drift_count / len(baseline)
    
    # Maximum 10% drift acceptable (some variation expected from LLM)
    assert drift_rate <= 0.10, f"Model drift: {drift_rate:.1%} (exceeds 10% threshold)"
```

---

## Validation Checkpoint

Before proceeding to Phase 6, verify:

- [ ] All existing tests pass: `pytest tests/ -v`
- [ ] Test coverage above 80%: `pytest --cov=src --cov-report=html`
- [ ] No performance regressions detected
- [ ] Mock tests run without API calls
- [ ] Integration tests validate full pipeline
- [ ] HTML sanitization tests catch XSS attempts
- [ ] Departmental routing accuracy above 85%
- [ ] Synthetic test data generates correctly
- [ ] CI/CD pipeline executes all test stages
- [ ] Benchmark results within acceptable ranges

**Test Execution Commands:**

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_enhanced_classifier.py -v

# Run tests matching pattern
pytest -k "test_routing" -v

# Run benchmarks only
pytest tests/performance --benchmark-only

# Generate HTML report
pytest --html=report.html --self-contained-html
```

---

## Key Takeaways

1. **ML testing is property-based**, not exact-match testing
2. **Mock external APIs** for fast, deterministic unit tests
3. **Use fixtures** for reusable test data and setup
4. **Test security** (HTML sanitization, XSS prevention)
5. **Monitor performance** (latency, throughput, memory)
6. **Generate synthetic data** for scalable test coverage
7. **Track accuracy metrics** to detect model drift
8. **Integrate with CI/CD** for continuous quality assurance
9. **Test at multiple levels**: unit, integration, E2E
10. **Document test intent** with clear descriptions

Testing ML systems requires different patterns than traditional software. Focus on statistical properties, aggregate metrics, and continuous monitoring rather than deterministic outputs.

**Next Phase**: Production Deployment (Phase 6) - containerization, cloud deployment, monitoring, and operational procedures.
