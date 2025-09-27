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
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import time
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

try:
    from enhanced_classifier import GeminiEnhancedClassifier, EnhancedClassificationResult
except ImportError:
    st.error("❌ Enhanced classifier not found. Please ensure enhanced_classifier.py is available.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="🤖 Enhanced Telkom Ticket Classifier - Gemini LLM",
    page_icon="🤖",
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
    
    .telkom-logo {
        width: 50px;
        height: 50px;
        background: white;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        color: #e31837;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
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
    sorted_data = sorted(zip(categories, probs), key=lambda x: x[1], reverse=True)
    categories, probs = zip(*sorted_data)
    
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
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def main():
    """Main Streamlit application."""
    
    # Header with Telkom branding
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
            <div class="telkom-logo">T</div>
            <div>
                <h1 style="margin: 0;">🤖 Enhanced Telkom Ticket Classifier</h1>
                <h3 style="margin: 0.5rem 0 0 0;">Powered by Google Gemini LLM + Traditional ML Ensemble</h3>
                <p style="margin: 0.5rem 0 0 0;">Advanced ticket classification with AI reasoning and explainable decisions</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Automatic initialization status
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
            "My monthly bill shows extra charges I didn't authorize",
            "Internet connection drops every 10 minutes",
            "Want to upgrade to fiber package with higher speed",
            "The technician never showed up for my appointment",
            "No cellular coverage in Johannesburg CBD area",
            "Need to change my contact details urgently",
            "Just wanted to compliment your excellent service",
            "Computer making strange noises, please advise"
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