#!/usr/bin/env python3
"""
🎯 Enhanced Multi-Provider Streamlit Demo
Advanced call centre agent demonstration with provider selection and cost optimization

Features:
1. Provider selection UI (LLM + Vector DB)
2. Real-time cost tracking and comparison
3. Live classification with provider switching
4. Enhanced pipeline visualization
5. Performance metrics and audit trail

Author: GitHub Copilot Assistant
Date: October 9, 2025
Purpose: Multi-provider demonstration and benchmarking interface
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json
from datetime import datetime
from typing import Dict, List, Any

# Custom styling and security
from markupsafe import escape
import logging

# Import multi-provider system
try:
    from src.models.multi_provider_manager import MultiProviderManager, ClassificationResult
    from src.models.multi_provider_config import MultiProviderConfig
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit configuration
st.set_page_config(
    page_title="Call Centre Agent - Multi-Provider Demo",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
.metric-container {
    background-color: #f0f2f6;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
}

.provider-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.cost-savings {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    font-weight: bold;
    margin: 10px 0;
}

.performance-metric {
    background-color: #ffffff;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0;
    text-align: center;
}

.alert-success {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 12px;
    border-radius: 6px;
    margin: 10px 0;
}

.alert-info {
    background-color: #d1ecf1;
    border: 1px solid #bee5eb;
    color: #0c5460;
    padding: 12px;
    border-radius: 6px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'manager' not in st.session_state:
        st.session_state.manager = MultiProviderManager()
    
    if 'classification_history' not in st.session_state:
        st.session_state.classification_history = []
    
    if 'cost_tracker' not in st.session_state:
        st.session_state.cost_tracker = {
            'total_queries': 0,
            'total_cost': 0.0,
            'provider_usage': {}
        }

def create_provider_status_cards():
    """Create provider status display cards"""
    status = st.session_state.manager.get_provider_status()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🤖 LLM Providers")
        for provider_id, info in status['llm_providers'].items():
            status_icon = "✅" if info['available'] else "❌"
            cost_color = "green" if info['cost_per_query'] == 0 else "blue"
            
            st.markdown(f"""
            <div class="provider-card">
                <h4>{status_icon} {info['name']}</h4>
                <p><strong>Cost:</strong> <span style="color: {cost_color};">${info['cost_per_query']:.4f}/query</span></p>
                <p><strong>Response Time:</strong> {info['response_time_ms']}ms</p>
                <p><strong>Status:</strong> {info['status']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🗂️ Vector DB Providers")
        for provider_id, info in status['vector_db_providers'].items():
            status_icon = "✅" if info['available'] else "❌"
            cost_color = "green" if info['cost_per_query'] == 0 else "blue"
            
            st.markdown(f"""
            <div class="provider-card">
                <h4>{status_icon} {info['name']}</h4>
                <p><strong>Cost:</strong> <span style="color: {cost_color};">${info['cost_per_query']:.4f}/query</span></p>
                <p><strong>Response Time:</strong> {info['response_time_ms']}ms</p>
                <p><strong>Status:</strong> {info['status']}</p>
            </div>
            """, unsafe_allow_html=True)

def create_cost_comparison_chart():
    """Create interactive cost comparison chart"""
    estimates = st.session_state.manager.get_cost_estimates(1000)
    
    if not estimates['combinations']:
        st.warning("No provider combinations available for cost analysis")
        return
    
    # Prepare data for visualization
    chart_data = []
    for combo in estimates['combinations']:
        chart_data.append({
            'Combination': f"{combo['llm_name']} + {combo['vector_db_name']}",
            'Monthly Cost ($)': combo['monthly_cost'],
            'Annual Cost ($)': combo['annual_cost'],
            'Data Sovereignty': combo['data_sovereignty'],
            'Cost per Query ($)': combo['cost_per_query']
        })
    
    df = pd.DataFrame(chart_data)
    
    # Create cost comparison chart
    fig = px.bar(
        df, 
        x='Combination', 
        y='Monthly Cost ($)',
        color='Data Sovereignty',
        title='Monthly Cost Comparison (1000 queries/month)',
        color_discrete_map={'local': '#4CAF50', 'cloud': '#2196F3'}
    )
    fig.update_layout(xaxis_tickangle=-45, height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display cost savings
    cheapest = estimates['cheapest']
    most_expensive = estimates['most_expensive']
    
    if cheapest and most_expensive:
        savings = most_expensive['annual_cost'] - cheapest['annual_cost']
        savings_percent = (savings / most_expensive['annual_cost']) * 100
        
        st.markdown(f"""
        <div class="cost-savings">
            💰 Maximum Annual Savings: ${savings:.2f} ({savings_percent:.1f}%)
            <br>
            🏆 Best Option: {cheapest['llm_name']} + {cheapest['vector_db_name']}
        </div>
        """, unsafe_allow_html=True)

def create_performance_dashboard():
    """Create performance metrics dashboard"""
    if not st.session_state.classification_history:
        st.info("No classification history yet. Try some sample tickets!")
        return
    
    history = st.session_state.classification_history
    df = pd.DataFrame(history)
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_time = df['processing_time_ms'].mean()
        st.markdown(f"""
        <div class="performance-metric">
            <h4>⏱️ Avg Response</h4>
            <h2>{avg_time:.0f}ms</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_confidence = df['confidence'].mean()
        st.markdown(f"""
        <div class="performance-metric">
            <h4>🎯 Avg Confidence</h4>
            <h2>{avg_confidence:.1%}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_cost = df['cost_estimate'].sum()
        st.markdown(f"""
        <div class="performance-metric">
            <h4>💸 Total Cost</h4>
            <h2>${total_cost:.4f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        fallback_rate = df['fallback_used'].mean() * 100
        st.markdown(f"""
        <div class="performance-metric">
            <h4>🔄 Fallback Rate</h4>
            <h2>{fallback_rate:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance over time chart
    fig_performance = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Response Time', 'Confidence Score', 'Cost per Query', 'Provider Usage'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "domain"}]]
    )
    
    # Response time trend
    fig_performance.add_trace(
        go.Scatter(y=df['processing_time_ms'], mode='lines+markers', name='Response Time'),
        row=1, col=1
    )
    
    # Confidence trend
    fig_performance.add_trace(
        go.Scatter(y=df['confidence'], mode='lines+markers', name='Confidence'),
        row=1, col=2
    )
    
    # Cost trend
    fig_performance.add_trace(
        go.Scatter(y=df['cost_estimate'], mode='lines+markers', name='Cost'),
        row=2, col=1
    )
    
    # Provider usage pie chart
    llm_usage = df['llm_provider'].value_counts()
    fig_performance.add_trace(
        go.Pie(labels=llm_usage.index, values=llm_usage.values, name="LLM Usage"),
        row=2, col=2
    )
    
    fig_performance.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig_performance, use_container_width=True)

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.title("📞 Call Centre Agent - Multi-Provider Demo")
    st.markdown("**Advanced AI classification with configurable providers and cost optimization**")
    
    # Sidebar - Provider Configuration
    with st.sidebar:
        st.header("⚙️ Provider Configuration")
        
        status = st.session_state.manager.get_provider_status()
        
        # LLM Provider Selection
        llm_options = {k: v['name'] for k, v in status['llm_providers'].items() if v['available']}
        current_llm = status['current_preferences']['llm']
        
        selected_llm = st.selectbox(
            "🤖 LLM Provider",
            options=list(llm_options.keys()),
            format_func=lambda x: llm_options[x],
            index=list(llm_options.keys()).index(current_llm) if current_llm in llm_options else 0
        )
        
        # Vector DB Provider Selection
        vdb_options = {k: v['name'] for k, v in status['vector_db_providers'].items() if v['available']}
        current_vdb = status['current_preferences']['vector_db']
        
        selected_vdb = st.selectbox(
            "🗂️ Vector DB Provider",
            options=list(vdb_options.keys()),
            format_func=lambda x: vdb_options[x],
            index=list(vdb_options.keys()).index(current_vdb) if current_vdb in vdb_options else 0
        )
        
        # Update providers if changed
        if selected_llm != current_llm or selected_vdb != current_vdb:
            if st.session_state.manager.set_providers(selected_llm, selected_vdb):
                st.success("✅ Providers updated!")
                st.experimental_rerun()
        
        st.markdown("---")
        
        # Configuration Options
        st.subheader("🔧 Options")
        use_vector_search = st.checkbox("Enable Vector Search", value=True)
        show_debug_info = st.checkbox("Show Debug Information", value=False)
        
        st.markdown("---")
        
        # Quick Stats
        st.subheader("📊 Session Stats")
        st.metric("Total Queries", st.session_state.cost_tracker['total_queries'])
        st.metric("Total Cost", f"${st.session_state.cost_tracker['total_cost']:.6f}")
        
        # Reset button
        if st.button("🔄 Reset Session"):
            st.session_state.classification_history = []
            st.session_state.cost_tracker = {
                'total_queries': 0,
                'total_cost': 0.0,
                'provider_usage': {}
            }
            st.experimental_rerun()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🧪 Classification", "📊 Providers", "💰 Cost Analysis", "📈 Performance"])
    
    with tab1:
        st.header("🎯 Ticket Classification")
        
        # Sample tickets for quick testing
        st.subheader("📋 Sample Tickets")
        sample_tickets = [
            "My internet connection is very slow and I can't stream videos",
            "I need to upgrade my mobile plan to get more data allowance",
            "There's a problem with my monthly bill - I was charged twice",
            "My phone screen is cracked and needs repair",
            "I want to cancel my service and get a refund",
            "The WiFi router keeps disconnecting every few minutes"
        ]
        
        cols = st.columns(2)
        for i, ticket in enumerate(sample_tickets):
            col = cols[i % 2]
            with col:
                if st.button(f"Test: {ticket[:30]}...", key=f"sample_{i}"):
                    st.session_state.current_ticket = ticket
        
        # Ticket input
        ticket_text = st.text_area(
            "✍️ Enter Customer Ticket:",
            value=getattr(st.session_state, 'current_ticket', ''),
            height=100,
            placeholder="Describe the customer's issue..."
        )
        
        if st.button("🚀 Classify Ticket", type="primary", disabled=not ticket_text.strip()):
            with st.spinner("🔄 Processing with multi-provider system..."):
                start_time = time.time()
                
                # Sanitize input
                clean_ticket = escape(ticket_text.strip())
                
                # Classify using multi-provider system
                result = st.session_state.manager.classify_ticket(
                    str(clean_ticket),
                    use_vector_search=use_vector_search,
                    force_llm_provider=None,
                    force_vector_provider=None
                )
                
                # Update session tracking
                st.session_state.cost_tracker['total_queries'] += 1
                st.session_state.cost_tracker['total_cost'] += result.cost_estimate
                
                # Add to history
                history_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'ticket_text': str(clean_ticket),
                    'department': result.department,
                    'confidence': result.confidence,
                    'processing_time_ms': result.processing_time_ms,
                    'cost_estimate': result.cost_estimate,
                    'llm_provider': result.providers_used.get('llm', 'unknown'),
                    'vector_provider': result.providers_used.get('vector_db', 'none'),
                    'fallback_used': result.fallback_used
                }
                st.session_state.classification_history.append(history_entry)
                
                # Display results
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 🎯 Classification Result")
                    
                    # Department with confidence indicator
                    confidence_color = "green" if result.confidence > 0.8 else "orange" if result.confidence > 0.6 else "red"
                    st.markdown(f"""
                    <div class="alert-success">
                        <h3>📂 Department: <strong>{result.department.replace('_', ' ').title()}</strong></h3>
                        <p><strong>Confidence:</strong> <span style="color: {confidence_color};">{result.confidence:.1%}</span></p>
                        <p><strong>Reasoning:</strong> {result.reasoning}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Provider information
                    providers_info = []
                    for component, provider in result.providers_used.items():
                        providers_info.append(f"{component.replace('_', ' ').title()}: {provider}")
                    
                    st.markdown(f"""
                    <div class="alert-info">
                        <p><strong>Providers Used:</strong> {', '.join(providers_info)}</p>
                        <p><strong>Processing Time:</strong> {result.processing_time_ms:.1f}ms</p>
                        <p><strong>Cost:</strong> ${result.cost_estimate:.6f}</p>
                        {"<p><strong>⚠️ Fallback Used</strong></p>" if result.fallback_used else ""}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("### 📊 Metrics")
                    st.metric("Confidence", f"{result.confidence:.1%}")
                    st.metric("Processing Time", f"{result.processing_time_ms:.1f}ms")
                    st.metric("Cost", f"${result.cost_estimate:.6f}")
                
                # Debug information
                if show_debug_info:
                    st.markdown("### 🔍 Debug Information")
                    st.json(result.metadata)
    
    with tab2:
        st.header("🔧 Provider Management")
        create_provider_status_cards()
        
        # Provider comparison table
        st.markdown("### 📋 Provider Comparison")
        status = st.session_state.manager.get_provider_status()
        
        comparison_data = []
        for category in ['llm_providers', 'vector_db_providers']:
            for provider_id, info in status[category].items():
                comparison_data.append({
                    'Category': 'LLM' if category == 'llm_providers' else 'Vector DB',
                    'Provider': info['name'],
                    'Status': '✅ Available' if info['available'] else '❌ Unavailable',
                    'Cost per Query': f"${info['cost_per_query']:.4f}",
                    'Response Time': f"{info['response_time_ms']}ms",
                    'Data Sovereignty': '🏠 Local' if provider_id in ['ollama', 'chromadb'] else '☁️ Cloud'
                })
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
    
    with tab3:
        st.header("💰 Cost Analysis")
        create_cost_comparison_chart()
        
        # Detailed cost breakdown
        st.markdown("### 📊 Detailed Cost Analysis")
        estimates = st.session_state.manager.get_cost_estimates(1000)
        
        if estimates['combinations']:
            df_costs = pd.DataFrame(estimates['combinations'])
            
            # Format costs for display
            df_display = df_costs.copy()
            df_display['Monthly Cost'] = df_display['monthly_cost'].apply(lambda x: f"${x:.2f}")
            df_display['Annual Cost'] = df_display['annual_cost'].apply(lambda x: f"${x:.2f}")
            df_display['Cost per Query'] = df_display['cost_per_query'].apply(lambda x: f"${x:.6f}")
            
            st.dataframe(
                df_display[['llm_name', 'vector_db_name', 'Cost per Query', 'Monthly Cost', 'Annual Cost', 'data_sovereignty']],
                column_config={
                    'llm_name': 'LLM Provider',
                    'vector_db_name': 'Vector DB Provider',
                    'data_sovereignty': 'Data Sovereignty'
                },
                use_container_width=True
            )
        
        # ROI Calculator
        st.markdown("### 🧮 ROI Calculator")
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_queries = st.number_input("Monthly Queries", min_value=100, max_value=100000, value=1000, step=100)
            current_cost_per_query = st.number_input("Current Cost per Query ($)", min_value=0.0, max_value=1.0, value=0.001, format="%.6f")
        
        with col2:
            if st.button("📊 Calculate Savings"):
                current_monthly = monthly_queries * current_cost_per_query
                estimates = st.session_state.manager.get_cost_estimates(monthly_queries)
                
                if estimates['cheapest']:
                    cheapest_monthly = estimates['cheapest']['monthly_cost']
                    savings = current_monthly - cheapest_monthly
                    savings_percent = (savings / current_monthly) * 100 if current_monthly > 0 else 0
                    
                    st.markdown(f"""
                    <div class="cost-savings">
                        💰 Monthly Savings: ${savings:.2f} ({savings_percent:.1f}%)
                        <br>
                        📅 Annual Savings: ${savings * 12:.2f}
                        <br>
                        🏆 Best Option: {estimates['cheapest']['llm_name']} + {estimates['cheapest']['vector_db_name']}
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab4:
        st.header("📈 Performance Dashboard")
        create_performance_dashboard()
        
        # Classification history
        if st.session_state.classification_history:
            st.markdown("### 📋 Recent Classifications")
            
            # Show last 10 classifications
            recent_history = st.session_state.classification_history[-10:]
            history_df = pd.DataFrame(recent_history)
            
            # Format for display
            display_df = history_df.copy()
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%H:%M:%S')
            display_df['ticket_preview'] = display_df['ticket_text'].str[:50] + '...'
            display_df['confidence'] = display_df['confidence'].apply(lambda x: f"{x:.1%}")
            display_df['cost'] = display_df['cost_estimate'].apply(lambda x: f"${x:.6f}")
            display_df['time'] = display_df['processing_time_ms'].apply(lambda x: f"{x:.0f}ms")
            
            st.dataframe(
                display_df[['timestamp', 'ticket_preview', 'department', 'confidence', 'llm_provider', 'time', 'cost']],
                column_config={
                    'timestamp': 'Time',
                    'ticket_preview': 'Ticket Preview',
                    'department': 'Department',
                    'confidence': 'Confidence',
                    'llm_provider': 'LLM Provider',
                    'time': 'Response Time',
                    'cost': 'Cost'
                },
                use_container_width=True
            )
            
            # Export option
            if st.button("📥 Export History"):
                history_json = json.dumps(st.session_state.classification_history, indent=2)
                st.download_button(
                    "Download JSON",
                    history_json,
                    file_name=f"classification_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        📞 Call Centre Agent System | Multi-Provider Architecture | 
        <a href="https://github.com/your-repo/call-centre-agent" target="_blank">GitHub Repository</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()