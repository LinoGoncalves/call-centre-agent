# Phase 4: Production Streamlit UI Implementation

**Estimated Time**: 4-6 hours  
**Prerequisites**: Phases 1-3 completed, working enhanced classifier  
**File Reference**: `src/ui/streamlit_demo.py` (983 lines, production-ready)

---

## Overview

Phase 4 covers the **production Streamlit web interface** that provides an interactive demonstration of your AI classification system. This is not a toy demo—it's a fully-featured, production-grade UI with advanced features including real-time classification, sentiment analysis visualization, departmental routing displays, and comprehensive model comparison views.

### What You'll Learn

- Streamlit architecture and component patterns
- Session state management for stateful web apps
- Dynamic HTML rendering with security considerations
- Real-time data visualization with Plotly
- Production UI patterns (error handling, loading states, user feedback)
- CSS-in-Python styling for professional interfaces

---

## Architecture Overview

### Application Structure

The Streamlit app follows a modular architecture:

```
streamlit_demo.py (983 lines)
├── Configuration & Setup (lines 1-50)
│   ├── Imports and environment loading
│   ├── Path configuration
│   └── Page configuration
│
├── Styling Layer (lines 51-240)
│   ├── CSS definitions for all UI components
│   ├── Responsive design patterns
│   └── Accessibility improvements
│
├── Session State Management (lines 241-260)
│   ├── Classifier instance
│   ├── Classification history
│   ├── Model settings (ensemble weight, thresholds)
│   └── Debug flags
│
├── Helper Functions (lines 261-500)
│   ├── Sentiment display functions
│   ├── Departmental routing visualization
│   ├── HTML security/sanitization
│   └── Chart generation
│
└── Main Application (lines 501-983)
    ├── Header and branding
    ├── Sidebar configuration
    ├── Ticket input interface
    ├── Classification results display
    └── History management
```

### Key Design Patterns

1. **Session State for Persistence**: All user data persists across reruns
2. **Lazy Initialization**: Classifier only loads when needed
3. **Component Isolation**: Each UI element is self-contained
4. **Security-First**: Multiple layers of HTML sanitization
5. **Performance Optimization**: Dynamic height calculation, minimal reruns

---

## Core Components Deep Dive

### 1. Environment Setup and Configuration

**Lines 1-42**: Application bootstrap

```python
# Load environment variables from .env file
load_dotenv()

# Add src to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
```

**Why This Matters:**
- `load_dotenv()` loads your `GOOGLE_API_KEY` from `.env` automatically
- Path manipulation ensures imports work regardless of where you run the script
- This is production-ready path handling, not hardcoded paths

**Lines 44-50**: Page configuration

```python
st.set_page_config(
    page_title="Telco Ticket Classifier - Gemini LLM",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**Configuration Impact:**
- `layout="wide"` uses full browser width (critical for comparison views)
- `initial_sidebar_state="expanded"` shows controls immediately
- Page metadata affects browser tabs and bookmarks

---

### 2. CSS Styling System

**Lines 51-240**: Complete CSS styling embedded in Python

The app uses Streamlit's `st.markdown()` with `unsafe_allow_html=True` to inject custom CSS. This provides full control over appearance while maintaining security.

#### Key CSS Classes

**Sentiment Styling** (lines 160-200):
```css
.sentiment-positive {
    background: #e8f5e8;
    border-left-color: #4CAF50 !important;
    color: #1b5e20;
}
```

**Why This Pattern:**
- Color-coded backgrounds for instant visual recognition
- Border colors match sentiment severity
- Accessibility-compliant contrast ratios
- Professional telco industry aesthetic

**Priority Badges** (lines 201-230):
```css
.priority-p0 {
    background: #ffcdd2;
    color: #c62828;
}
```

**Design Decision:**
- P0 (red) → P1 (orange) → P2 (yellow) → P3 (green)
- Universal color language for urgency
- Matches industry standard priority systems

---

### 3. Session State Management

**Lines 241-260**: Persistent state across user interactions

```python
if 'classifier' not in st.session_state:
    st.session_state.classifier = None
if 'classification_history' not in st.session_state:
    st.session_state.classification_history = []
```

**Session State Pattern:**

Streamlit reruns your entire script on **every interaction** (button click, text input, slider change). Session state persists data across these reruns.

**Critical Variables:**
- `classifier`: Your `GeminiEnhancedClassifier` instance (expensive to recreate)
- `classification_history`: List of past classifications (for history table)
- `last_ensemble_weight`: Tracks model setting changes
- `last_other_threshold`: Triggers classifier reinitialization when changed

**Performance Impact:**
Without session state, you'd recreate the classifier (loading models, connecting to Gemini API) on **every** button click. This would make the app unusable.

---

### 4. HTML Sanitization: Multi-Layer Defense

**Lines 310-380**: `display_sentiment_analysis()` function

This function demonstrates **production-grade security** for handling LLM outputs that might contain HTML.

#### The Problem

Google Gemini sometimes returns HTML-formatted text:
```
<p><strong>Reasoning:</strong> Customer is frustrated</p>
```

If displayed directly in Streamlit, this can:
1. Break the UI rendering
2. Create XSS vulnerabilities
3. Look unprofessional with visible HTML tags

#### The Solution: 6-Step Sanitization Pipeline

**Step 1: BeautifulSoup Parsing** (lines 335-342)
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(clean_reasoning, 'html.parser')
clean_reasoning = soup.get_text()
```

**What It Does:** Parses HTML structure and extracts only text content. Handles complex nested tags.

**Step 2: HTML Entity Decoding** (line 345)
```python
clean_reasoning = html.unescape(clean_reasoning)
```

**What It Does:** Converts `&lt;` → `<`, `&#39;` → `'`, etc. Handles 250+ HTML entities.

**Step 3: Regex HTML Tag Removal** (lines 348-351)
```python
clean_reasoning = re.sub(r'<[^>]*>', '', clean_reasoning)      # Standard tags
clean_reasoning = re.sub(r'<.*?>', '', clean_reasoning)        # Greedy tags  
clean_reasoning = re.sub(r'&[a-zA-Z0-9#]+;', '', clean_reasoning)  # Entities
```

**Why Multiple Patterns:** Different regex patterns catch edge cases. Defense in depth.

**Step 4: Markdown Fence Removal** (lines 366-369)
```python
clean_reasoning = re.sub(r"```[\s\S]*?```", " ", clean_reasoning)
clean_reasoning = clean_reasoning.replace("```", "").replace("`", "")
```

**Why This Matters:** If Markdown code fences remain, Streamlit's Markdown renderer might treat your HTML wrapper as literal text instead of rendering it.

**Step 5: Character-Level Nuclear Cleaning** (lines 354-357)
```python
if '<' in clean_reasoning or '>' in clean_reasoning or '&' in clean_reasoning:
    clean_reasoning = ''.join(c for c in clean_reasoning if c not in '<>&')
```

**Last Resort:** If previous steps failed, just remove all potentially dangerous characters.

**Step 6: Whitespace Normalization** (line 361)
```python
clean_reasoning = ' '.join(clean_reasoning.split())
```

**What It Does:** Collapses multiple spaces/newlines into single spaces. Removes leading/trailing whitespace.

#### Why This Approach?

Each layer catches different edge cases:
- BeautifulSoup: Well-formed HTML
- Regex: Malformed HTML fragments
- Entity decoding: HTML-encoded characters
- Character filtering: Anything that slipped through

This is **production-grade defensive programming**. You can't trust LLM outputs to be clean.

---

### 5. Dynamic Height Calculation

**Lines 374-395**: Intelligent component sizing

```python
reasoning_length = len(clean_reasoning) if clean_reasoning else 0
base_height = 200  # Headers, sentiment info, priority badge
additional_height = max(50, (reasoning_length // 70) * 25)
total_height = min(base_height + additional_height, 450)
```

**Algorithm Breakdown:**
- **Base height (200px)**: Fixed space for headers, labels, badges
- **Additional height**: 25px per 70 characters of reasoning text
- **Maximum cap (450px)**: Prevents giant panels for very long responses
- **Minimum additional (50px)**: Ensures even short text looks good

**Why Not Fixed Height?**

Different classification results have vastly different reasoning lengths:
- Short: "Customer wants billing information." (35 chars)
- Long: "Customer is disputing charges due to unauthorized premium service activation..." (200+ chars)

Fixed height either wastes space or clips content. Dynamic sizing adapts.

---

### 6. Secure HTML Component Rendering

**Lines 396-425**: Safe HTML injection using `components.html()`

```python
safe_reasoning_js = json.dumps(clean_reasoning)

html_block = f"""
<div style="...">
    <h4>{sentiment_emoji} Sentiment Analysis</h4>
    <div id="sentiment-reasoning-text"></div>
    <script>
        (function() {{
            const txt = {safe_reasoning_js};
            const el = document.getElementById('sentiment-reasoning-text');
            if (el) {{ el.textContent = txt; }}
        }})();
    </script>
</div>
"""

components.html(html_block, height=total_height, scrolling=True)
```

**Security Pattern: JavaScript Text Injection**

**Why Not Direct HTML Insertion?**
```python
# DON'T DO THIS:
html_block = f"<div>{clean_reasoning}</div>"  # Vulnerable if cleaning failed
```

**The Safe Way:**
1. **JSON serialization**: `json.dumps(clean_reasoning)` escapes all special characters
2. **JavaScript assignment**: `el.textContent = txt` uses browser's safe text API
3. **IIFE (Immediately Invoked Function Expression)**: `(function() { ... })()` prevents scope pollution

**Browser Security:**
- `.textContent` API **never** interprets content as HTML
- Even if cleaning failed and `<script>` tags remain, they're rendered as text
- Double-encoded protection: JSON escaping + textContent sanitization

**Production Benefit:** This pattern is used by security-conscious web frameworks. You can safely display **any** LLM output without XSS risk.

---

### 7. Departmental Routing Visualization

**Lines 460-620**: `display_departmental_routing()` function

This component displays complex routing logic in an intuitive visual format.

#### Component Structure

**Department Display** (lines 500-520):
```python
dept_emojis = {
    "CREDIT_MGMT": "💰",
    "ORDER_MGMT": "📋", 
    "CRM": "🤝",
    "BILLING": "🧾"
}
```

**Design Pattern:** Emoji + Name + Confidence creates instant recognition:
```
💰 Credit Management
   Confidence: 95.3%
```

**Color Coding** (lines 530-545):
```python
dept_colors = {
    "CREDIT_MGMT": "#d32f2f",  # Red - high priority disputes
    "ORDER_MGMT": "#1976d2",   # Blue - service orders
    "CRM": "#388e3c",          # Green - customer relations
    "BILLING": "#f57c00"       # Orange - billing support
}
```

**Color Psychology:**
- Red (Credit): Urgency, money-related disputes
- Blue (Orders): Stability, service management
- Green (CRM): Growth, positive relations
- Orange (Billing): Attention, financial matters

#### Grid Layout System

**Lines 580-615**: CSS Grid for responsive information display

```python
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
    <div>Assigned Department</div>
    <div>Specific Team</div>
</div>
```

**Grid Advantages:**
- Automatically responsive (2 columns on wide screens, stacks on mobile)
- Equal-width columns regardless of content
- Professional alignment without manual calculations

#### Scrollable Reasoning Panel

**Lines 550-570**: Routing reasoning with overflow handling

```python
<div style="max-height: 200px; overflow-y: auto; overflow-x: hidden;">
    {result.routing_reasoning}
</div>
```

**Why Scrollbars:**

Routing reasoning can be verbose:
> "Ticket classified as CREDIT_MGMT due to explicit dispute keywords ('I dispute this charge'). Customer is contesting a R500 premium service charge they claim was unauthorized. This matches Credit Management dispute patterns. Confidence 95.3% based on strong dispute language and specific monetary amount mentioned. Requires HITL validation due to financial implications."

Fixed height + scrolling = predictable layout + full content access.

---

### 8. Model Comparison Display

**Lines 850-880**: Side-by-side model performance comparison

```python
comparison_df = pd.DataFrame({
    'Model': ['Traditional ML', 'Gemini LLM', 'Enhanced Ensemble'],
    'Prediction': [result.traditional_prediction, result.gemini_prediction, result.predicted_category],
    'Confidence': [f"{result.traditional_confidence:.1%}", f"{result.gemini_confidence:.1%}", f"{result.confidence:.1%}"],
    'Method': ['Hybrid ML (LogReg+RF)', 'Google Gemini 1.5', 'Weighted Ensemble']
})

st.table(comparison_df)
```

**Educational Value:**

Users can see **exactly how** ensemble logic combines predictions:

| Model | Prediction | Confidence | Method |
|-------|------------|-----------|--------|
| Traditional ML | BILLING | 78.3% | Hybrid ML (LogReg+RF) |
| Gemini LLM | CREDIT_MGMT | 95.7% | Google Gemini 1.5 |
| Enhanced Ensemble | CREDIT_MGMT | 89.2% | Weighted Ensemble |

**Insight:** Gemini's high confidence in CREDIT_MGMT (due to dispute keywords) overrode Traditional ML's BILLING prediction in the ensemble.

---

### 9. Interactive Model Settings

**Lines 700-780**: Real-time model reconfiguration

```python
ensemble_weight = st.slider(
    "Gemini Weight in Prediction",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="0% = Pure Traditional ML | 50% = Balanced Ensemble | 100% = Pure Gemini LLM"
)
```

**Interactivity Pattern:**

When slider changes:
1. **Detect change** (lines 765-770): Compare current value to `st.session_state.last_ensemble_weight`
2. **Update environment** (lines 773-775): Set `ENSEMBLE_WEIGHT` environment variable
3. **Reinitialize classifier** (lines 780-785): Create new `GeminiEnhancedClassifier` instance with new settings
4. **Update UI** (lines 788-795): Show success message with mode description
5. **Preserve history** (line 772): Clear cached results to prevent confusion

**Why Reinitialize?**

The classifier's ensemble logic is set during `__init__()`. Changing the weight requires a new instance to apply the new calculation.

**User Experience:**
```
✅ Settings updated! Mode: ENSEMBLE (70% Gemini, 30% Traditional ML)
🔄 Please re-run your classification to see the updated probabilities
```

Clear feedback prevents confusion about when changes take effect.

---

### 10. Probability Visualization

**Lines 625-660**: `create_probability_chart()` function

```python
def create_probability_chart(probabilities: dict, title: str):
    """Create a horizontal bar chart for probabilities."""
    categories = list(probabilities.keys())
    probs = list(probabilities.values())
    
    # Sort by probability
    sorted_data = sorted(zip(categories, probs, strict=True), key=lambda x: x[1], reverse=True)
    categories = [cat for cat, _ in sorted_data]
    probs = [p for _, p in sorted_data]
    
    fig = go.Figure(go.Bar(
        x=probs,
        y=categories,
        orientation='h',
        marker_color=['#4ECDC4' if cat == categories[0] else '#95A5A6' for cat in categories],
        text=[f'{p:.1%}' for p in probs],
        textposition='inside'
    ))
```

**Visualization Choices:**

1. **Horizontal bars**: Easier to read category names (no rotated text)
2. **Sorted by probability**: Top prediction always at top
3. **Color coding**: Winner highlighted in teal (#4ECDC4), others in gray
4. **In-bar labels**: Percentage values inside bars for space efficiency
5. **Plotly over Matplotlib**: Interactive (hover, zoom, pan)

**Chart Output:**
```
CREDIT_MGMT     [████████████████████] 89.2%
BILLING         [███████████          ] 65.4%
ORDER_MGMT      [████                 ] 23.1%
CRM             [██                   ] 12.7%
COMPLAINTS      [█                    ] 8.3%
OTHER           [                     ] 2.1%
```

---

### 11. Sample Ticket Management

**Lines 815-850**: Intelligent sample ticket system

```python
sample_tickets = [
    "Select a sample ticket...",
    # CREDIT MANAGEMENT - Disputes
    "💰 I dispute this R500 charge on my bill - I never authorized this premium service",
    # BILLING - General Inquiries  
    "🧾 Can you please explain why my bill is R200 higher than usual this month?",
    # ... more samples
]

selected_ticket = st.selectbox("Choose a sample ticket:", sample_tickets)

# Auto-populate text area when dropdown selection changes
if selected_ticket != "Select a sample ticket...":
    if st.session_state.get('last_selected') != selected_ticket:
        st.session_state.ticket_text = selected_ticket
        st.session_state.last_selected = selected_ticket
        st.success("✅ Sample ticket copied to text area!")
        st.rerun()
```

**User Experience Pattern:**

1. User selects ticket from dropdown
2. Check if selection is new (prevent infinite rerun loop)
3. Update text area session state
4. Show success message
5. **Trigger rerun**: Updates UI with new text

**Why `st.rerun()`?**

Streamlit doesn't automatically update `st.text_area()` value from session state changes in the same run. `st.rerun()` triggers a fresh render with updated values.

**Sample Organization:**

Samples are categorized by department with emoji prefixes:
- 💰 Credit disputes (high-confidence CREDIT_MGMT examples)
- 🧾 Billing inquiries (standard BILLING examples)
- 📋 Service orders (ORDER_MGMT examples)
- 🤝 Customer complaints (CRM examples)
- Mixed sentiment examples (testing edge cases)

**Educational Purpose:** Users can test classifier accuracy on known-category tickets.

---

### 12. Classification History Table

**Lines 920-950**: Persistent classification log

```python
if st.session_state.classification_history:
    history_df = pd.DataFrame([
        {
            'Ticket': item['ticket'],
            'Predicted Category': item['result'].predicted_category,
            'Confidence': f"{item['result'].confidence:.1%}",
            'Is OTHER': item['result'].is_other_category,
            'Processing Time (ms)': f"{item['result'].processing_time_ms:.0f}"
        }
        for item in st.session_state.classification_history[-10:]  # Last 10
    ])
    
    st.dataframe(history_df, use_container_width=True)
```

**Data Structure:**

Each history entry stores:
```python
{
    'ticket': "I dispute this charge...",  # Truncated to 100 chars
    'result': EnhancedClassificationResult(...),  # Full result object
    'timestamp': 1696234567.89  # Unix timestamp
}
```

**Display Logic:**
- Shows last 10 classifications only (prevent UI clutter)
- Truncates long tickets with `...` (lines 870-872)
- Full result objects preserved for re-display if needed

**Performance Monitoring:**

History table shows processing times:
```
Ticket                                    | Processing Time (ms)
------------------------------------------|--------------------
I dispute this R500 charge...            | 1234
Can you explain my bill?                 | 987
I want to upgrade my internet...         | 1156
```

Helps identify slow classifications (usually due to Gemini API latency).

---

## Running the Application

### Launch Script: `launch_demo.py`

**File Location**: Project root  
**Purpose**: Automated demo launcher with error handling

```python
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit demo with proper error handling."""
    demo_path = Path("src/ui/streamlit_demo.py")
    
    if not demo_path.exists():
        print(f"❌ Error: Demo file not found at {demo_path}")
        sys.exit(1)
    
    # Check for .env file
    if not Path(".env").exists():
        print("⚠️  Warning: No .env file found")
        print("Please create .env with: GOOGLE_API_KEY=your_key_here")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(demo_path),
            "--server.port=8501",
            "--server.address=localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error launching demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Launch Methods:**

**Option 1: Launch Script (Recommended)**
```bash
python launch_demo.py
```

**Option 2: Direct Streamlit Command**
```bash
streamlit run src/ui/streamlit_demo.py --server.port 8501
```

**Option 3: Python Module Execution**
```bash
python -m streamlit run src/ui/streamlit_demo.py
```

---

## Common Issues and Solutions

### Issue 1: Port Already in Use

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Solution 1: Kill existing Streamlit process**
```bash
# Windows
taskkill /F /IM python.exe /T

# Linux/Mac
pkill -f streamlit
```

**Solution 2: Use different port**
```bash
streamlit run src/ui/streamlit_demo.py --server.port 8502
```

---

### Issue 2: Module Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'src.models.enhanced_classifier'
```

**Root Cause:** Python path not configured correctly

**Solution:** The app handles this (lines 34-37):
```python
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
```

Ensure you're running from project root, not from `src/ui/` directory.

---

### Issue 3: API Key Not Found

**Error:**
```
❌ No API key found in .env file
```

**Solution:**

1. Create `.env` file in project root:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

2. Verify file exists:
```bash
# Windows
dir .env

# Linux/Mac
ls -la .env
```

3. Restart Streamlit (environment variables load on startup)

---

### Issue 4: HTML Rendering Issues

**Symptom:** Seeing raw HTML tags in sentiment reasoning:
```
<p><strong>Reasoning:</strong> Customer is frustrated</p>
```

**Root Cause:** Sanitization failure (very rare with 6-layer defense)

**Debug Mode:**

Enable in sidebar:
```python
st.session_state.debug_html = True
```

Shows cleaning pipeline steps:
```
DEBUG - Original received: '<p><strong>Reasoning:</strong> Customer is frustrated</p>'
DEBUG - After BeautifulSoup: 'Reasoning: Customer is frustrated'
DEBUG - After HTML unescape: 'Reasoning: Customer is frustrated'
DEBUG - Final clean result: 'Customer is frustrated'
```

---

### Issue 5: Slow Performance

**Symptom:** Classifications take 3-5+ seconds

**Diagnosis:**

Check processing times in results:
```python
st.markdown(f"<p><strong>Processing Time:</strong> {result.processing_time_ms:.0f}ms</p>")
```

**Common Causes:**

1. **Gemini API Latency** (1000-2000ms normal)
   - Solution: Geographic - use closest Google Cloud region
   - Workaround: Increase `ensemble_weight` toward 0.0 (more traditional ML)

2. **Model Loading** (first request slow)
   - Solution: Classifier initialization cached in session state
   - First classification: ~3000ms
   - Subsequent: ~1200ms

3. **Network Issues**
   - Solution: Check internet connection
   - Test: `curl https://generativelanguage.googleapis.com/`

---

## Production Deployment Considerations

### Environment Variables

**Required:**
```bash
GOOGLE_API_KEY=your_api_key
```

**Optional:**
```bash
ENSEMBLE_WEIGHT=0.7           # Default Gemini weight
OTHER_CATEGORY_THRESHOLD=0.6  # Default OTHER threshold
STREAMLIT_SERVER_PORT=8501    # Server port
STREAMLIT_SERVER_ADDRESS=0.0.0.0  # Bind address (0.0.0.0 for external access)
```

---

### Security Hardening

**1. API Key Protection:**

Never commit `.env` to git:
```bash
# .gitignore
.env
*.env
```

**2. Network Security:**

Restrict access in production:
```bash
streamlit run src/ui/streamlit_demo.py \
    --server.address=127.0.0.1 \  # Localhost only
    --server.enableCORS=false \    # Disable CORS
    --server.enableXsrfProtection=true
```

**3. HTML Sanitization:**

The 6-layer sanitization pipeline (lines 310-370) is production-grade, but always:
- Test with malicious inputs
- Monitor for XSS attempts in logs
- Keep BeautifulSoup updated

---

### Performance Optimization

**1. Caching Strategy:**

Streamlit's `@st.cache_data` and `@st.cache_resource` decorators can cache expensive operations:

```python
@st.cache_resource
def get_classifier():
    """Cache classifier instance across all users."""
    return GeminiEnhancedClassifier()
```

**Trade-off:** Single shared instance vs per-session instances (current approach). Current approach is safer for concurrent users.

**2. Lazy Loading:**

Classifier only initializes when needed (lines 700-715):
```python
if not st.session_state.classifier and not st.session_state.initialization_attempted:
    initialize_classifier()
```

Prevents wasting resources for users just browsing.

**3. History Limiting:**

Only keep last 10 classifications (line 941):
```python
for item in st.session_state.classification_history[-10:]
```

Prevents memory bloat during long sessions.

---

### Monitoring and Logging

**Add Application Logging:**

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('streamlit_app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

**Log Critical Events:**
- Classifier initialization failures
- API errors from Gemini
- Unexpected classification results
- Performance issues (processing time > threshold)

---

## Validation Checkpoint

Before proceeding to Phase 5, verify:

- [ ] Streamlit app launches without errors
- [ ] API key loads from `.env` file
- [ ] Classifier initializes successfully
- [ ] Sample tickets classify correctly
- [ ] Sentiment analysis displays properly (no HTML visible)
- [ ] Departmental routing shows all fields
- [ ] Model comparison table populates
- [ ] Probability charts render correctly
- [ ] Classification history updates
- [ ] Slider changes reinitialize classifier
- [ ] No console errors in terminal
- [ ] Processing times under 3 seconds
- [ ] Multiple classifications work without issues

**Test Sequence:**

1. Launch app: `python launch_demo.py`
2. Select sample ticket: "💰 I dispute this R500 charge..."
3. Click "🎯 Classify Ticket"
4. Verify all 4 result panels display:
   - Final Prediction
   - AI Reasoning
   - Sentiment Analysis (with emoji)
   - Departmental Routing
5. Check Model Comparison table has 3 rows
6. Adjust "Gemini Weight" slider to 1.0
7. Re-classify same ticket
8. Verify prediction might change (pure Gemini now)
9. Check history table shows 2 entries
10. Click "🗑️ Clear History" and verify table disappears

**Expected Results:**

All checkpoints pass with no errors. If any fail, review the "Common Issues and Solutions" section.

---

## Extension Challenges

Want to enhance the UI? Try these:

### Challenge 1: Export Classification Results

**Goal:** Add "📥 Download Results" button that exports classification to JSON/CSV

**Hint:** Use `st.download_button()` with JSON serialization:
```python
import json

if st.button("📥 Download Results"):
    export_data = {
        'ticket': ticket_text,
        'category': result.predicted_category,
        'confidence': result.confidence,
        'timestamp': time.time()
    }
    st.download_button(
        label="Download JSON",
        data=json.dumps(export_data, indent=2),
        file_name="classification_result.json",
        mime="application/json"
    )
```

---

### Challenge 2: Batch Upload Feature

**Goal:** Allow CSV upload of multiple tickets, classify all, show results table

**Hint:** Use `st.file_uploader()` + pandas:
```python
uploaded_file = st.file_uploader("Upload CSV with 'ticket' column", type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    results = []
    for ticket in df['ticket']:
        result = classifier.classify_ticket(ticket)
        results.append(result.predicted_category)
    df['prediction'] = results
    st.dataframe(df)
```

---

### Challenge 3: Real-Time Confidence Threshold Adjustment

**Goal:** Add slider to filter history table by minimum confidence

**Hint:** Filter dataframe before display:
```python
min_confidence = st.slider("Minimum Confidence", 0.0, 1.0, 0.5)
filtered_history = [
    item for item in st.session_state.classification_history 
    if item['result'].confidence >= min_confidence
]
```

---

## Next Steps

✅ **Phase 4 Complete!** You now have a production-grade web interface for your AI classifier.

**Phase 5 Preview**: Testing & Validation
- Unit tests for all components
- Integration tests for end-to-end workflows
- Performance benchmarking
- Test data generation
- Continuous integration setup

The UI is production-ready, but Phase 5 ensures **reliability** through comprehensive testing.

---

## Key Takeaways

1. **Streamlit session state** enables stateful web apps despite script reruns
2. **Multi-layer HTML sanitization** is critical for LLM output security
3. **Dynamic sizing** creates professional UIs that adapt to content
4. **Component isolation** makes code maintainable (each function = one UI element)
5. **JavaScript text injection** (`textContent` API) is safest for untrusted content
6. **CSS-in-Python** provides full styling control without external files
7. **Plotly over Matplotlib** for interactive, professional visualizations
8. **Sample ticket system** improves UX by providing test cases
9. **History tracking** helps users understand classifier behavior over time
10. **Real-time model reconfiguration** enables experimentation without code changes

This is **production-grade UI engineering** - not a toy demo. Every pattern shown (sanitization, caching, error handling, responsive design) is used in enterprise applications.
