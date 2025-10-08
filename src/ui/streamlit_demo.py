#!/usr/bin/env python3
"""
🚀 Enhanced Streamlit Demo with Google Gemini LLM Integration
Interactive demonstration of advanced ticket classification with reasoning

Features:
1. Google Gemini LLM integration for enhanced accuracy  
2. Reasoning paragraphs explaining classification decisions
3. OTHER category for low-confidence predictions
4. Side-by-side comparison: Traditional ML vs Enhanced LLM
5. Professional UI with accessibility improvements

Author: Data Scientist AI Assistant
Date: September 27, 2025
Purpose: Product Owner validation of enhanced LLM features
"""

import os
import sys
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import time
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.models.enhanced_classifier import GeminiEnhancedClassifier, EnhancedClassificationResult
    from src.ui.pipeline_visualization import (
        display_pipeline_visualization,
        create_real_pipeline_visualization
    )
except ImportError as e:
    st.error(f"❌ Import error: {e}")
    st.error("Please ensure all required modules are available.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Telco Ticket Classifier - Gemini LLM",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling with accessibility improvements
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #e31837, #4ECDC4);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
        
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4ECDC4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .prediction-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #4ECDC4;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #1a1a1a;
        font-weight: 600;
    }
    
    .reasoning-box {
        background: #f8fffe;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
        color: #1a1a1a;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    .other-category {
        background: #fffbf0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
        color: #1a1a1a;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    .comparison-table {
        margin: 1rem 0;
    }
    
    .comparison-table table {
        width: 100%;
        border-collapse: collapse;
        background: white;
    }
    
    .comparison-table th {
        background: #4ECDC4;
        color: white;
        padding: 0.8rem;
        font-weight: 600;
        border: 1px solid #ddd;
    }
    
    .comparison-table td {
        padding: 0.8rem;
        border: 1px solid #ddd;
        color: #333;
        font-weight: 500;
    }
    
    .confidence-high { background: #d4edda; color: #155724; }
    .confidence-medium { background: #fff3cd; color: #856404; }
    .confidence-low { background: #f8d7da; color: #721c24; }
    
    .sample-ticket {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 3px solid #4ECDC4;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #333;
        font-weight: 500;
    }
    
    .sample-ticket:hover {
        background: #e8f0fe;
        transform: translateX(5px);
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Sentiment Analysis Styles */
    .sentiment-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid #2196F3;
    }
    
    .sentiment-positive {
        background: #e8f5e8;
        border-left-color: #4CAF50 !important;
        color: #1b5e20;
    }
    
    .sentiment-neutral {
        background: #f5f5f5;
        border-left-color: #9E9E9E !important;
        color: #424242;
    }
    
    .sentiment-negative {
        background: #fff3e0;
        border-left-color: #FF9800 !important;
        color: #e65100;
    }
    
    .sentiment-critical {
        background: #ffebee;
        border-left-color: #f44336 !important;
        color: #c62828;
    }
    
    .priority-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .priority-p0 {
        background: #ffcdd2;
        color: #c62828;
    }
    
    .priority-p1 {
        background: #ffe0b2;
        color: #ef6c00;
    }
    
    .priority-p2 {
        background: #fff9c4;
        color: #f57f17;
    }
    
    .priority-p3 {
        background: #e8f5e8;
        color: #388e3c;
    }
    
    .escalation-required {
        background: #ffcdd2;
        color: #c62828;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .sentiment-emoji {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'classifier' not in st.session_state:
    st.session_state.classifier = None
if 'classification_history' not in st.session_state:
    st.session_state.classification_history = []
if 'initialization_attempted' not in st.session_state:
    st.session_state.initialization_attempted = False
if 'last_ensemble_weight' not in st.session_state:
    st.session_state.last_ensemble_weight = 0.7
if 'last_other_threshold' not in st.session_state:
    st.session_state.last_other_threshold = 0.6

# Sentiment analysis helper functions
def get_sentiment_emoji(sentiment_label: str) -> str:
    """Get appropriate emoji for sentiment."""
    emoji_map = {
        "POSITIVE": "😊",
        "NEUTRAL": "😐", 
        "NEGATIVE": "😠",
        "CRITICAL": "🚨"
    }
    return emoji_map.get(sentiment_label, "😐")

def get_sentiment_color_class(sentiment_label: str) -> str:
    """Get CSS class for sentiment styling."""
    return f"sentiment-{sentiment_label.lower()}"

def get_priority_badge_class(priority_level: str) -> str:
    """Get CSS class for priority badge."""
    priority_map = {
        "P0_IMMEDIATE": "priority-p0",
        "P1_HIGH": "priority-p1", 
        "P2_MEDIUM": "priority-p2",
        "P3_STANDARD": "priority-p3"
    }
    return priority_map.get(priority_level, "priority-p3")

def display_sentiment_analysis(result: EnhancedClassificationResult):
    """Display sentiment analysis results with visual indicators."""
    sentiment_emoji = get_sentiment_emoji(result.sentiment_label)
    sentiment_class = get_sentiment_color_class(result.sentiment_label)
    priority_class = get_priority_badge_class(result.priority_level)
    
    # NUCLEAR OPTION: Ultimate HTML cleaning - clean at display time regardless of source
    import re
    import html
    
    # Get original reasoning
    original_reasoning = result.sentiment_reasoning
    
    # Debug: Always show what we received
    if st.session_state.get('debug_html', False):
        st.text(f"DEBUG - Original received: {repr(original_reasoning)}")
    
    # STEP 1: BeautifulSoup cleaning (handles all HTML structures)
    clean_reasoning = original_reasoning
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(clean_reasoning, 'html.parser')
        clean_reasoning = soup.get_text()
        if st.session_state.get('debug_html', False):
            st.text(f"DEBUG - After BeautifulSoup: {repr(clean_reasoning)}")
    except Exception as e:
        if st.session_state.get('debug_html', False):
            st.text(f"DEBUG - BeautifulSoup failed: {e}")
    
    # STEP 2: Decode HTML entities (like &#x27; &#39; &lt; &gt;)
    clean_reasoning = html.unescape(clean_reasoning)
    if st.session_state.get('debug_html', False):
        st.text(f"DEBUG - After HTML unescape: {repr(clean_reasoning)}")
    
    # STEP 3: Nuclear regex cleaning - remove ALL possible HTML patterns
    clean_reasoning = re.sub(r'<[^>]*>', '', clean_reasoning)      # Standard tags
    clean_reasoning = re.sub(r'<.*?>', '', clean_reasoning)        # Greedy tags  
    clean_reasoning = re.sub(r'&[a-zA-Z0-9#]+;', '', clean_reasoning)  # HTML entities
    clean_reasoning = re.sub(r'<[^<>]*>', '', clean_reasoning)     # Alternative pattern
    
    # STEP 4: Remove specific problematic patterns
    clean_reasoning = re.sub(r'^(Reasoning:\s*|reasoning:\s*)', '', clean_reasoning, flags=re.IGNORECASE)
    
    # STEP 5: Character-by-character nuclear cleaning
    if '<' in clean_reasoning or '>' in clean_reasoning or '&' in clean_reasoning:
        clean_reasoning = ''.join(c for c in clean_reasoning if c not in '<>&')
        if st.session_state.get('debug_html', False):
            st.text(f"DEBUG - Applied nuclear cleaning")
    
    # STEP 6: Whitespace normalization
    clean_reasoning = ' '.join(clean_reasoning.split())
    
    # STEP 6.5: Remove Markdown code fences/backticks and blockquotes that can break Markdown rendering
    # Rationale: If Markdown sees ``` or leading >, it may render our wrapper HTML as literal text.
    clean_reasoning = re.sub(r"```[\s\S]*?```", " ", clean_reasoning)  # remove fenced code blocks
    clean_reasoning = clean_reasoning.replace("```", "").replace("`", "")  # remove stray backticks
    clean_reasoning = re.sub(r"^\s*>\s*", "", clean_reasoning, flags=re.MULTILINE)  # remove blockquote markers

    # STEP 7: Safety fallback
    if not clean_reasoning.strip() or len(clean_reasoning) < 5:
        clean_reasoning = "Sentiment analysis completed successfully."
    
    if st.session_state.get('debug_html', False):
        st.text(f"DEBUG - Final clean result: {repr(clean_reasoning)}")
    
    # STEP 8: Optimized dynamic height calculation similar to departmental routing
    # Calculate height based on actual content length
    reasoning_length = len(clean_reasoning) if clean_reasoning else 0
    base_height = 200  # Base height for headers, sentiment info, etc.
    
    # More efficient height calculation (25px per 70 characters)
    additional_height = max(50, (reasoning_length // 70) * 25)
    
    # Set reasonable bounds for the panel
    total_height = min(base_height + additional_height, 450)
    
    # Calculate max height for reasoning text area (reserve space for headers/info)
    reasoning_max_height = max(100, total_height - 140)
    
    # Use safe HTML component with proper escaping
    safe_reasoning_js = json.dumps(clean_reasoning)
    
    # Simple styling with proper text wrapping and scrollbars
    html_block = f"""
    <div style="
        background: #f0f0f0; 
        padding: 1.5rem; 
        border-radius: 10px; 
        margin: 0; 
        border-left: 5px solid #2196F3; 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        height: {total_height}px;
        overflow-y: auto;
    ">
        <h4><span style="font-size:1.5rem; margin-right:0.5rem;">{sentiment_emoji}</span>Sentiment Analysis</h4>
        <p><strong>Sentiment:</strong> <span style="color: {get_sentiment_color_for_text(result.sentiment_label)};">{result.sentiment_label}</span> (Score: {result.sentiment_score:+.1f})</p>
        <p><strong>Priority Level:</strong> <span style="background: {get_priority_bg(result.priority_level)}; color: {get_priority_text(result.priority_level)}; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase;">{result.priority_level.replace('_', ' ')}</span></p>
        {f'<div style="background: #ffcdd2; color: #c62828; padding: 0.5rem 1rem; border-radius: 5px; font-weight: 600; display: inline-block; margin: 0.5rem 0;">⚠️ IMMEDIATE ESCALATION REQUIRED</div>' if result.escalation_required else ''}
        <p><strong>Reasoning:</strong></p>
        <div id="sentiment-reasoning-text" style="
            word-wrap: break-word; 
            white-space: pre-wrap; 
            line-height: 1.6; 
            margin-top: 0.5rem;
            max-height: {reasoning_max_height}px;
            overflow-y: auto;
            padding: 0.8rem;
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
        "></div>
        <script>
            (function() {{
                const txt = {safe_reasoning_js};
                const el = document.getElementById('sentiment-reasoning-text');
                if (el) {{ el.textContent = txt; }}
            }})();
        </script>
    </div>
    """
    
    # Use optimized height with scrolling enabled
    components.html(html_block, height=total_height, scrolling=True)

def get_sentiment_color_for_text(sentiment_label: str) -> str:
    """Get text color for sentiment."""
    colors = {
        "POSITIVE": "#1b5e20",
        "NEUTRAL": "#424242", 
        "NEGATIVE": "#e65100",
        "CRITICAL": "#c62828"
    }
    return colors.get(sentiment_label, "#424242")

def get_priority_bg(priority_level: str) -> str:
    """Get background color for priority badge."""
    colors = {
        "P0_IMMEDIATE": "#ffcdd2",
        "P1_HIGH": "#ffe0b2", 
        "P2_MEDIUM": "#fff9c4",
        "P3_STANDARD": "#e8f5e8"
    }
    return colors.get(priority_level, "#e8f5e8")

def get_priority_text(priority_level: str) -> str:
    """Get text color for priority badge."""
    colors = {
        "P0_IMMEDIATE": "#c62828",
        "P1_HIGH": "#ef6c00",
        "P2_MEDIUM": "#f57f17", 
        "P3_STANDARD": "#388e3c"
    }
    return colors.get(priority_level, "#388e3c")

def display_departmental_routing(result: EnhancedClassificationResult):
    """Display departmental routing and team allocation information."""
    # Department emoji mapping
    dept_emojis = {
        "CREDIT_MGMT": "💰",
        "ORDER_MGMT": "📋", 
        "CRM": "🤝",
        "BILLING": "🧾"
    }
    
    dept_names = {
        "CREDIT_MGMT": "Credit Management",
        "ORDER_MGMT": "Order Management",
        "CRM": "Customer Relationship Management", 
        "BILLING": "Billing Support"
    }
    
    # Get department color based on type
    dept_colors = {
        "CREDIT_MGMT": "#d32f2f",  # Red - high priority disputes
        "ORDER_MGMT": "#1976d2",   # Blue - service orders
        "CRM": "#388e3c",          # Green - customer relations
        "BILLING": "#f57c00"       # Orange - billing support
    }
    
    dept_emoji = dept_emojis.get(result.department_allocation, "🏢")
    dept_name = dept_names.get(result.department_allocation, result.department_allocation)
    dept_color = dept_colors.get(result.department_allocation, "#666666")
    
    # SLA response time display
    sla_hours = result.sla_response_time_hours
    if sla_hours == 1:
        sla_text = "1 Hour"
    elif sla_hours < 24:
        sla_text = f"{sla_hours} Hours"
    else:
        sla_text = f"{sla_hours//24} Day{'s' if sla_hours > 24 else ''}"
    
    html_content = f"""
    <div style="
        background: #f8f9fa;
        border: 2px solid {dept_color};
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        overflow-y: auto;
        max-height: 600px;
    ">
        <h3 style="margin: 0 0 15px 0; color: #2c3e50; border-bottom: 2px solid {dept_color}; padding-bottom: 8px;">
            🏛️ Departmental Routing & Team Assignment
        </h3>
        
        <div style="
            background: #e8f4fd; 
            border-left: 4px solid #2196f3; 
            padding: 12px; 
            margin-bottom: 20px; 
            border-radius: 4px;
            max-height: 200px;
            overflow-y: auto;
            overflow-x: hidden;
        ">
            <h4 style="margin: 0 0 8px 0; color: #1565c0; font-size: 14px;">🧠 AI Routing Reasoning</h4>
            <div style="
                margin: 0; 
                color: #424242; 
                font-size: 13px; 
                line-height: 1.5;
                word-wrap: break-word;
                overflow-wrap: break-word;
            ">
                {result.routing_reasoning}
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
            <div style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #dee2e6;">
                <h4 style="margin: 0 0 8px 0; color: #495057; font-size: 14px;">🏢 Assigned Department</h4>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 20px;">{dept_emoji}</span>
                    <div>
                        <div style="font-weight: bold; color: {dept_color}; font-size: 16px;">{dept_name}</div>
                        <div style="color: #666; font-size: 12px;">Confidence: {result.routing_confidence:.1%}</div>
                    </div>
                </div>
            </div>
            
            <div style="background: white; padding: 12px; border-radius: 8px; border: 1px solid #dee2e6;">
                <h4 style="margin: 0 0 8px 0; color: #495057; font-size: 14px;">👥 Specific Team</h4>
                <div style="font-weight: bold; color: #2c3e50; font-size: 16px;">{result.assigned_team}</div>
                <div style="color: #666; font-size: 12px;">Service Desk: {result.service_desk_agent}</div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 15px;">
            <div style="background: {'#ffebee' if result.dispute_detected else '#e8f5e8'}; padding: 10px; border-radius: 6px; text-align: center;">
                <div style="font-size: 18px; margin-bottom: 4px;">{'⚠️' if result.dispute_detected else '✅'}</div>
                <div style="font-size: 12px; color: #666;">Dispute Status</div>
                <div style="font-weight: bold; color: {'#d32f2f' if result.dispute_detected else '#388e3c'};">
                    {'DETECTED' if result.dispute_detected else 'NONE'}
                </div>
                {f'<div style="font-size: 10px; color: #666;">{result.dispute_confidence:.0%} confidence</div>' if result.dispute_detected else ''}
            </div>
            
            <div style="background: #e3f2fd; padding: 10px; border-radius: 6px; text-align: center;">
                <div style="font-size: 18px; margin-bottom: 4px;">⏰</div>
                <div style="font-size: 12px; color: #666;">SLA Response</div>
                <div style="font-weight: bold; color: #1976d2;">{sla_text}</div>
                <div style="font-size: 10px; color: #666;">{result.priority_level.replace('_', ' ')}</div>
            </div>
            
            <div style="background: {'#fff3e0' if result.requires_hitl else '#e8f5e8'}; padding: 10px; border-radius: 6px; text-align: center;">
                <div style="font-size: 18px; margin-bottom: 4px;">{'👨‍💼' if result.requires_hitl else '🤖'}</div>
                <div style="font-size: 12px; color: #666;">Validation</div>
                <div style="font-weight: bold; color: {'#f57c00' if result.requires_hitl else '#388e3c'};">
                    {'HITL REQUIRED' if result.requires_hitl else 'AUTO-APPROVED'}
                </div>
            </div>
        </div>
    </div>
    """
    
    # Use fixed height since we now have scrollbars for overflow content
    total_height = 450  # Fixed height with scrollbars handling overflow
    
    # Display using components.html with dynamic height
    components.html(html_content, height=total_height)

def initialize_classifier():
    """Initialize the enhanced classifier automatically."""
    try:
        st.session_state.classifier = GeminiEnhancedClassifier()
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize classifier: {e}")
        st.error("💡 Please ensure your Google API key is set in the .env file")
        return False

def format_confidence(confidence: float) -> str:
    """Format confidence with color coding."""
    if confidence >= 0.8:
        return f"<span class='confidence-high'>{confidence:.1%}</span>"
    elif confidence >= 0.6:
        return f"<span class='confidence-medium'>{confidence:.1%}</span>"
    else:
        return f"<span class='confidence-low'>{confidence:.1%}</span>"

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
    
    fig.update_layout(
        title=title,
        xaxis_title="Confidence",
        yaxis_title="Category",
        height=300,
        margin={"l": 20, "r": 20, "t": 40, "b": 20}
    )
    
    return fig

def main():
    """Main Streamlit application."""
    
    # Header with Telco branding
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
            <div>
                <h1 style="margin: 0; font-size: 3.6rem;">Telco Ticket Classifier</h1>
                <h3 style="margin: 0.5rem 0 0 0; font-size: 1.44rem;">Powered by Google Gemini LLM + Traditional ML Ensemble</h3>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem;">Advanced ticket classification with AI reasoning and explainable decisions</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
        # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Pipeline visualization toggle
        show_pipeline_viz = st.checkbox(
            "🔍 Show Routing Pipeline",
            value=True,
            help="Display step-by-step routing decision process"
        )
        
        # Sample tickets guide
        st.markdown("---")
        st.subheader("🎯 Sample Ticket Guide")
        st.markdown("""
        **Test Different Routing Paths:**
        
        🔧 **[RULES]** - High-confidence pattern matches
        - Instant routing (<1ms) 
        - 85-99% confidence
        - Bypasses Vector DB & LLM
        
        🔍 **[VECTOR]** - Similarity search scenarios  
        - Historical pattern matching (~45ms)
        - Medium confidence (70-84%)
        - Uses cached routing intelligence
        
        🤖 **[RAG]** - Complex LLM reasoning
        - Multi-intent or ambiguous tickets
        - Full AI analysis (~850ms)
        - Detailed reasoning provided
        
        ⚡ **[FAST]** vs 🧠 **[COMPLEX]** - Speed comparison
        """)
        
        st.info("💡 Enable pipeline visualization above to see the complete routing flow!")        # Automatic initialization status
        env_api_key = os.getenv('GOOGLE_API_KEY')
        if env_api_key:
            st.success("✅ API key loaded from .env file")
            
            # Auto-initialize if not done yet
            if not st.session_state.classifier and not st.session_state.initialization_attempted:
                with st.spinner("🤖 Initializing Enhanced Classifier..."):
                    if initialize_classifier():
                        st.success("🚀 Enhanced classifier ready!")
                        st.session_state.initialization_attempted = True
                        st.rerun()
                    else:
                        st.session_state.initialization_attempted = True
        else:
            st.error("❌ No API key found in .env file")
            st.markdown("""
            **Setup Required:**
            1. Add `GOOGLE_API_KEY=your_key` to `.env` file
            2. Get your key from: [Google AI Studio](https://aistudio.google.com/)
            3. Refresh this page
            """)
        
        st.markdown("---")
        
        # Debug settings (temporary)
        st.subheader("🐛 Debug")
        debug_html = st.checkbox("Show raw HTML from API", value=False, help="Enable to see raw API responses")
        st.session_state.debug_html = debug_html
        
        if st.button("🔄 Clear Cache & Restart Classifier", help="Force restart classifier to clear any cached results"):
            st.session_state.classifier = None
            st.session_state.initialization_attempted = False
            st.session_state.classification_history = []
            st.success("Cache cleared! Page will reload.")
            st.rerun()
        
        st.markdown("---")
        
        # Model settings
        if st.session_state.classifier:
            st.subheader("⚙️ Model Settings")
            
            other_threshold = st.slider(
                "OTHER Category Threshold",
                min_value=0.1,
                max_value=0.9,
                value=0.6,
                step=0.1,
                help="Minimum confidence for base categories"
            )
            
            ensemble_weight = st.slider(
                "Gemini Weight in Prediction",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="0% = Pure Traditional ML | 50% = Balanced Ensemble | 100% = Pure Gemini LLM"
            )
            
            # Check if settings changed - if so, reinitialize classifier
            settings_changed = (
                abs(ensemble_weight - st.session_state.last_ensemble_weight) > 0.05 or
                abs(other_threshold - st.session_state.last_other_threshold) > 0.05
            )
            
            if settings_changed and st.session_state.classifier is not None:
                # Update environment variables for new classifier instance
                os.environ['ENSEMBLE_WEIGHT'] = str(ensemble_weight)
                os.environ['OTHER_CATEGORY_THRESHOLD'] = str(other_threshold)
                
                # Clear any cached results that might interfere
                if 'classification_history' in st.session_state:
                    st.session_state.classification_history = []
                
                # Reinitialize classifier with new settings
                with st.spinner("🔄 Updating model settings..."):
                    try:
                        st.session_state.classifier = GeminiEnhancedClassifier()
                        st.session_state.last_ensemble_weight = ensemble_weight
                        st.session_state.last_other_threshold = other_threshold
                        
                        # Show mode-specific success message
                        if ensemble_weight == 0.0:
                            st.success("✅ Settings updated! Mode: **PURE TRADITIONAL ML** (Classic ML only)")
                        elif ensemble_weight == 1.0:
                            st.success("✅ Settings updated! Mode: **PURE GEMINI LLM** (AI only)")
                        else:
                            st.success(f"✅ Settings updated! Mode: **ENSEMBLE** ({ensemble_weight:.0%} Gemini, {(1-ensemble_weight):.0%} Traditional ML)")
                        
                        st.info("🔄 Please re-run your classification to see the updated probabilities")
                    except Exception as e:
                        st.error(f"❌ Error reinitializing classifier: {e}")
            else:
                # Update classifier settings for current instance
                if st.session_state.classifier:
                    st.session_state.classifier.other_threshold = other_threshold
                    st.session_state.classifier.ensemble_weight = ensemble_weight
            
            st.markdown("---")
            
            # Sentiment Analysis Configuration
            st.subheader("💭 Sentiment Analysis")
            
            st.markdown("""
            **Sentiment Levels:**
            - 😊 **POSITIVE** (+0.7): Happy, satisfied customers
            - 😐 **NEUTRAL** (0.0): Standard inquiries  
            - 😠 **NEGATIVE** (-0.7): Frustrated customers
            - 🚨 **CRITICAL** (-1.0): Extremely upset, requires escalation
            
            **Priority Mapping:**
            - 🔴 **P0 IMMEDIATE**: COMPLAINTS + CRITICAL sentiment
            - 🟠 **P1 HIGH**: High-risk categories + NEGATIVE/CRITICAL sentiment
            - 🟡 **P2 MEDIUM**: Standard categories + NEGATIVE sentiment
            - 🟢 **P3 STANDARD**: All other combinations
            """)
            
        # Debug info to show current settings and mode
        if st.session_state.classifier:
            weight = st.session_state.classifier.ensemble_weight
            if weight == 0.0:
                mode_info = "🔥 **PURE TRADITIONAL ML** - Using only classic ML models"
            elif weight == 1.0:
                mode_info = "🤖 **PURE GEMINI LLM** - Using only Google Gemini AI"
            else:
                mode_info = f"⚖️ **ENSEMBLE MODE** - {weight:.0%} Gemini | {(1-weight):.0%} Traditional ML"
            
            st.info(f"🔧 Current Mode: {mode_info} | OTHER threshold: {st.session_state.classifier.other_threshold:.0%}")
        
        st.markdown("---")
        
        # Enhanced features info
        st.markdown("""
        <div class="feature-highlight">
        <h4>🌟 Enhanced Features</h4>
        <ul>
        <li>🤖 Google Gemini LLM integration</li>
        <li>💭 AI reasoning explanations</li>
        <li>🏛️ <strong>Departmental routing & team assignment</strong></li>
        <li>⚖️ <strong>Dispute detection for Credit Management</strong></li>
        <li>👨‍💼 <strong>Human-in-the-loop (HITL) validation</strong></li>
        <li>⏰ <strong>Priority-based SLA response times</strong></li>
        <li>⚠️ OTHER category for edge cases</li>
        <li>📊 Model comparison views</li>
        <li>⚡ Real-time ensemble predictions</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    if not st.session_state.classifier:
        if not os.getenv('GOOGLE_API_KEY'):
            st.warning("⚠️ Please set up your Google Gemini API key in the .env file to get started.")
        else:
            st.info("🤖 Initializing enhanced classifier... Please wait.")
        
        st.markdown("### 📋 Setup Instructions:")
        st.markdown("""
        1. **Get API Key**: Visit [Google AI Studio](https://aistudio.google.com/)
        2. **Create .env file**: Add `GOOGLE_API_KEY=your_key_here`
        3. **Refresh page**: The classifier will initialize automatically
        """)
        
        return
    
    # Ticket input section
    st.header("📝 Ticket Classification")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input with clear functionality
        if 'ticket_text' not in st.session_state:
            st.session_state.ticket_text = ""
        
        ticket_text = st.text_area(
            "📝 Enter Customer Ticket Text:",
            value=st.session_state.ticket_text,
            height=150,
            placeholder="Type or paste a customer support ticket here, or select from dropdown →",
            help="Enter the customer's message or complaint for automatic classification",
            key="ticket_input"
        )
        
        # Update session state with any manual changes
        st.session_state.ticket_text = ticket_text
        
        # Buttons row
        col1a, col1b, col1c = st.columns([1, 1, 2])
        
        with col1a:
            classify_button = st.button("🎯 Classify Ticket", type="primary")
        
        with col1b:
            if st.button("🗑️ Clear Text"):
                st.session_state.ticket_text = ""
                st.rerun()
    
    with col2:
        st.subheader("📚 Sample Tickets")
        
        sample_tickets = [
            "Select a sample ticket...",
            
            # 🔧 RULES ENGINE MATCHES (High-Confidence, Sub-millisecond Routing)
            "🔧 [RULES] I dispute this R500 charge - I never authorized this premium service subscription",
            "🔧 [RULES] My account is locked and I cannot login to the customer portal to pay my bill",
            "🔧 [RULES] The internet service is down in my area - no connection for the past 3 hours",
            "🔧 [RULES] I was charged twice for my monthly data package - please investigate this duplicate charge",
            "🔧 [RULES] My payment failed when trying to pay online - card was declined but should work fine",
            "🔧 [RULES] I forgot my password and need to reset it to access my online account",
            "🔧 [RULES] URGENT: I think there's been unauthorized access to my account - possible security breach",
            "🔧 [RULES] I'm thinking of leaving your service - the quality has been poor lately",
            "� [RULES] I want to setup a new internet service at my home - please schedule installation",
            "� [RULES] My internet connection is extremely slow - speed test shows only 2 Mbps instead of 50 Mbps",
            
            # 🔍 VECTOR DB SCENARIOS (Similarity Search with Historical Patterns)
            "🔍 [VECTOR] My WiFi router keeps disconnecting every few minutes during work calls",
            "� [VECTOR] I'm getting weird charges on my bill that I don't recognize from last month",
            "🔍 [VECTOR] The mobile signal strength is very weak in my office building",
            "🔍 [VECTOR] I need help setting up parental controls on my internet connection",
            "🔍 [VECTOR] My data usage seems much higher than normal this month",
            
            # 🤖 RAG/LLM COMPLEX SCENARIOS (Requiring AI Reasoning)
            "� [RAG] Hi, I have several issues: my bill seems wrong, I want to upgrade my service, and the internet has been slow. Can you help with all of these? Also, I'm not happy with the customer service I received last week.",
            "� [RAG] There's something strange going on with my account. The numbers don't seem right and I'm concerned about what I'm seeing. Could you look into this please?",
            "� [RAG] Our business depends on reliable internet for video conferences with clients. The connection keeps dropping during important meetings, which is affecting our revenue. We need a technical solution and possibly compensation for lost business.",
            "🤖 [RAG] I AM EXTREMELY FRUSTRATED!!! This is the THIRD TIME I'm calling about this issue and nobody seems to understand what I need. The billing department told me one thing, technical support said something else, and now I don't know what to believe.",
            "🤖 [RAG] I love my current internet service and I'm wondering what other products you offer. My neighbor mentioned something about mobile plans and TV packages. Could you tell me about bundle deals that might save me money?",
            
            # � PERFORMANCE COMPARISON EXAMPLES
            "⚡ [FAST] Thank you for the excellent customer service - your technician was very helpful",
            "⚡ [FAST] Can you please explain my bill - I don't understand some of the charges listed",
            "🧠 [COMPLEX] The latency on my fiber connection is terrible - I'm getting 150ms ping times to local servers when it should be under 20ms. My VPN keeps timing out and my remote work is being impacted."
        ]
        
        selected_ticket = st.selectbox(
            "Choose a sample ticket:",
            sample_tickets,
            key="sample_dropdown",
            help="Selecting a ticket will automatically copy it to the text area"
        )
        
        # Auto-populate text area when dropdown selection changes
        if selected_ticket != "Select a sample ticket...":
            if st.session_state.get('last_selected') != selected_ticket:
                st.session_state.ticket_text = selected_ticket
                st.session_state.last_selected = selected_ticket
                st.success("✅ Sample ticket copied to text area!")
                st.rerun()
    
    # Classification results
    if classify_button and ticket_text:
        with st.spinner("🤖 Enhanced AI Classification in Progress..."):
            try:
                result = st.session_state.classifier.classify_ticket(ticket_text)
                
                # Store in history
                st.session_state.classification_history.append({
                    'ticket': ticket_text[:100] + '...' if len(ticket_text) > 100 else ticket_text,
                    'result': result,
                    'timestamp': time.time()
                })
                
                # Display results
                st.success("✅ Classification Complete!")
                
                # Main prediction
                if result.is_other_category:
                    st.markdown(f"""
                    <div class="other-category">
                        <h3>⚠️ OTHER Category Classification</h3>
                        <p><strong>Category:</strong> {result.predicted_category}</p>
                        <p><strong>Confidence:</strong> {format_confidence(result.confidence)}</p>
                        <p><strong>Status:</strong> Requires human review</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="prediction-box">
                        <h3>🎯 Final Prediction</h3>
                        <p><strong>Category:</strong> {result.predicted_category}</p>
                        <p><strong>Confidence:</strong> {format_confidence(result.confidence)}</p>
                        <p><strong>Processing Time:</strong> {result.processing_time_ms:.0f}ms</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # AI Reasoning
                st.markdown(f"""
                <div class="reasoning-box">
                    <h4>💭 AI Reasoning</h4>
                    <p>{result.reasoning}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Sentiment Analysis Display
                display_sentiment_analysis(result)
                
                # NEW: Departmental Routing Display
                display_departmental_routing(result)
                
                # Pipeline visualization
                if show_pipeline_viz:
                    pipeline_viz = create_real_pipeline_visualization(ticket_text, result)
                    display_pipeline_visualization(pipeline_viz)
                
                # Model comparison
                st.subheader("🔍 Model Comparison")
                
                comparison_df = pd.DataFrame({
                    'Model': ['Traditional ML', 'Gemini LLM', 'Enhanced Ensemble'],
                    'Prediction': [result.traditional_prediction, result.gemini_prediction, result.predicted_category],
                    'Confidence': [f"{result.traditional_confidence:.1%}", f"{result.gemini_confidence:.1%}", f"{result.confidence:.1%}"],
                    'Method': ['Hybrid ML (LogReg+RF)', 'Google Gemini 1.5', 'Weighted Ensemble']
                })
                
                st.markdown('<div class="comparison-table">', unsafe_allow_html=True)
                st.table(comparison_df)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Probability distribution
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = create_probability_chart(result.all_probabilities, "📊 Category Probabilities")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Performance metrics
                    st.subheader("⚡ Performance Metrics")
                    
                    metrics = [
                        ("Processing Time", f"{result.processing_time_ms:.0f}ms"),
                        ("Ensemble Weight", f"{st.session_state.classifier.ensemble_weight:.1%} Gemini"),
                        ("OTHER Threshold", f"{st.session_state.classifier.other_threshold:.1%}"),
                        ("Categories", f"{len(st.session_state.classifier.categories)} total")
                    ]
                    
                    for metric, value in metrics:
                        st.metric(metric, value)
                
            except Exception as e:
                st.error(f"❌ Classification failed: {e}")
    
    # Classification history
    if st.session_state.classification_history:
        st.header("📈 Classification History")
        
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
        
        if st.button("🗑️ Clear History"):
            st.session_state.classification_history = []
            st.rerun()

if __name__ == "__main__":
    main()