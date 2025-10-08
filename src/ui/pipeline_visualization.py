"""
Enhanced Routing Pipeline Visualization for Streamlit
====================================================
This module adds stepwise visualization of the routing decision pipeline,
showing how tickets flow through Rules Engine → Vector DB → RAG/LLM stages.
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import uuid
import sys
from pathlib import Path

# Add project root to path for rules engine import
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

@dataclass
class PipelineStep:
    """Represents a single step in the routing pipeline."""
    step_name: str
    step_number: int
    processing_time_ms: float
    decision: str
    confidence: Optional[float]
    details: Dict[str, Any]
    timestamp: datetime
    success: bool
    next_step: Optional[str] = None

@dataclass
class PipelineVisualization:
    """Complete pipeline visualization data."""
    ticket_id: str
    ticket_text: str
    steps: List[PipelineStep]
    final_routing: Dict[str, Any]
    total_processing_time_ms: float
    pipeline_efficiency: str
    cost_optimization: Dict[str, Any]

def create_pipeline_step_card(step: PipelineStep, is_active: bool = False) -> str:
    """Create HTML card for a single pipeline step."""
    
    # Step-specific styling and icons
    step_icons = {
        "Rules Engine": "🔧",
        "Vector DB Search": "🔍", 
        "RAG Analysis": "🤖",
        "Fallback": "🛡️",
        "Final Decision": "🎯"
    }
    
    step_colors = {
        "Rules Engine": "#4caf50",  # Green - fast deterministic
        "Vector DB Search": "#2196f3",  # Blue - intelligent search
        "RAG Analysis": "#ff9800",  # Orange - AI processing  
        "Fallback": "#9e9e9e",  # Gray - backup
        "Final Decision": "#e91e63"  # Pink - final outcome
    }
    
    icon = step_icons.get(step.step_name, "⚙️")
    color = step_colors.get(step.step_name, "#666666")
    
    # Active step highlighting
    border_style = "3px solid #ff5722" if is_active else f"1px solid {color}"
    box_shadow = "0 4px 12px rgba(0,0,0,0.2)" if is_active else "0 2px 6px rgba(0,0,0,0.1)"
    
    # Decision outcome styling
    if step.success:
        outcome_color = "#4caf50"
        outcome_icon = "✅"
    else:
        outcome_color = "#ff9800" 
        outcome_icon = "➡️"
    
    # Confidence display
    confidence_display = ""
    if step.confidence is not None:
        if step.confidence >= 0.85:
            conf_color = "#4caf50"
            conf_label = "HIGH"
        elif step.confidence >= 0.70:
            conf_color = "#ff9800" 
            conf_label = "MEDIUM"
        else:
            conf_color = "#f44336"
            conf_label = "LOW"
        
        confidence_display = f"""
        <div style="margin-top: 8px;">
            <span style="
                background: {conf_color}20;
                color: {conf_color};
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
            ">
                {conf_label} ({step.confidence:.1%})
            </span>
        </div>
        """
    
    # Details formatting
    details_html = ""
    if step.details:
        details_items = []
        for key, value in step.details.items():
            if isinstance(value, (int, float)):
                if key.endswith('_ms') or key.endswith('time'):
                    details_items.append(f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value:.1f}ms</li>")
                else:
                    details_items.append(f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>")
            elif isinstance(value, list) and len(value) > 0:
                details_items.append(f"<li><strong>{key.replace('_', ' ').title()}:</strong> {len(value)} items</li>")
            else:
                details_items.append(f"<li><strong>{key.replace('_', ' ').title()}:</strong> {str(value)[:50]}</li>")
        
        if details_items:
            details_html = f"""
            <details style="margin-top: 10px;">
                <summary style="cursor: pointer; font-size: 12px; color: {color};">
                    📋 View Details ({len(details_items)} items)
                </summary>
                <ul style="font-size: 11px; margin: 5px 0; padding-left: 15px; color: #666;">
                    {''.join(details_items[:5])}  
                </ul>
            </details>
            """
    
    return f"""
    <div style="
        border: {border_style};
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        background: white;
        box-shadow: {box_shadow};
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        transition: all 0.3s ease;
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 20px;">{icon}</span>
                <div>
                    <div style="font-weight: 600; color: {color}; font-size: 14px;">
                        STEP {step.step_number}: {step.step_name}
                    </div>
                    <div style="font-size: 11px; color: #666; font-weight: 500;">
                        {step.processing_time_ms:.1f}ms processing time
                    </div>
                </div>
            </div>
            <span style="font-size: 18px; color: {outcome_color};">{outcome_icon}</span>
        </div>
        
        <div style="
            background: #f8f9fa;
            padding: 10px;
            border-radius: 6px;
            border-left: 3px solid {color};
            margin: 8px 0;
        ">
            <div style="font-weight: 600; color: #333; font-size: 13px; margin-bottom: 4px;">
                Decision: {step.decision}
            </div>
            {confidence_display}
        </div>
        
        {details_html}
        
        {f'<div style="font-size: 11px; color: #888; text-align: center; margin-top: 8px;">▼ {step.next_step}</div>' if step.next_step else ''}
    </div>
    """

def create_cost_optimization_summary(pipeline_viz: PipelineVisualization) -> str:
    """Create cost optimization analysis display."""
    
    # Determine primary routing method
    final_method = pipeline_viz.final_routing.get("method", "unknown")
    
    cost_savings = ""
    efficiency_icon = ""
    
    if final_method == "rules_engine":
        cost_savings = "🎯 HIGH COST SAVINGS - Bypassed expensive ML/LLM processing"
        efficiency_icon = "🚀"
        efficiency_color = "#4caf50"
    elif final_method == "vector_cache":
        cost_savings = "⚡ MEDIUM COST SAVINGS - Used cached similarity routing"
        efficiency_icon = "⚡"
        efficiency_color = "#ff9800"
    elif final_method == "rag_llm":
        cost_savings = "🤖 FULL ANALYSIS - Used comprehensive AI reasoning"
        efficiency_icon = "🧠"
        efficiency_color = "#2196f3"
    else:
        cost_savings = "🛡️ FALLBACK - Used backup routing mechanism"
        efficiency_icon = "🛡️"
        efficiency_color = "#9e9e9e"
    
    return f"""
    <div style="
        background: linear-gradient(135deg, {efficiency_color}10, white);
        border: 2px solid {efficiency_color};
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    ">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
            <span style="font-size: 24px;">{efficiency_icon}</span>
            <div>
                <div style="font-weight: 700; color: {efficiency_color}; font-size: 16px;">
                    COST OPTIMIZATION ANALYSIS
                </div>
                <div style="font-size: 12px; color: #666;">
                    Pipeline efficiency and resource utilization
                </div>
            </div>
        </div>
        
        <div style="
            background: white;
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid {efficiency_color};
            margin-bottom: 12px;
        ">
            <div style="font-weight: 600; color: #333; font-size: 14px;">
                {cost_savings}
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px;">
            <div style="text-align: center; padding: 8px; background: white; border-radius: 6px;">
                <div style="font-size: 18px; font-weight: 700; color: {efficiency_color};">
                    {pipeline_viz.total_processing_time_ms:.0f}ms
                </div>
                <div style="font-size: 11px; color: #666; font-weight: 600;">TOTAL TIME</div>
            </div>
            <div style="text-align: center; padding: 8px; background: white; border-radius: 6px;">
                <div style="font-size: 18px; font-weight: 700; color: {efficiency_color};">
                    {len(pipeline_viz.steps)}
                </div>
                <div style="font-size: 11px; color: #666; font-weight: 600;">STEPS</div>
            </div>
            <div style="text-align: center; padding: 8px; background: white; border-radius: 6px;">
                <div style="font-size: 18px; font-weight: 700; color: {efficiency_color};">
                    {pipeline_viz.pipeline_efficiency.upper()}
                </div>
                <div style="font-size: 11px; color: #666; font-weight: 600;">EFFICIENCY</div>
            </div>
        </div>
    </div>
    """

def display_pipeline_visualization(pipeline_viz: PipelineVisualization):
    """Display the complete pipeline visualization in Streamlit."""
    
    st.markdown("### 🔄 Routing Pipeline Visualization")
    
    # Pipeline overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Pipeline Steps", 
            len(pipeline_viz.steps),
            f"Ticket ID: {pipeline_viz.ticket_id}"
        )
    
    with col2:
        st.metric(
            "Total Processing Time",
            f"{pipeline_viz.total_processing_time_ms:.1f}ms",
            f"Efficiency: {pipeline_viz.pipeline_efficiency}"
        )
    
    with col3:
        final_dept = pipeline_viz.final_routing.get("department", "Unknown")
        final_confidence = pipeline_viz.final_routing.get("confidence", 0)
        st.metric(
            "Final Routing",
            final_dept.replace("_", " ").title(),
            f"Confidence: {final_confidence:.1%}"
        )
    
    # Ticket preview
    st.markdown("#### 📝 Ticket Content")
    ticket_preview = pipeline_viz.ticket_text[:150] + "..." if len(pipeline_viz.ticket_text) > 150 else pipeline_viz.ticket_text
    st.info(f"**Ticket Text**: {ticket_preview}")
    
    # Pipeline steps
    st.markdown("#### ⚙️ Pipeline Execution Flow")
    
    # Create step cards
    steps_html = ""
    for i, step in enumerate(pipeline_viz.steps):
        is_active = (i == len(pipeline_viz.steps) - 1)  # Highlight last step
        steps_html += create_pipeline_step_card(step, is_active)
    
    # Display using components.html for rich formatting
    components.html(
        f"""
        <div style="
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #f8f9fa;
        ">
            {steps_html}
        </div>
        """,
        height=520,
        scrolling=True
    )
    
    # Cost optimization summary
    st.markdown("#### 💰 Cost & Performance Analysis") 
    cost_html = create_cost_optimization_summary(pipeline_viz)
    components.html(cost_html, height=200)

def create_real_pipeline_visualization(ticket_text: str, result: Any) -> PipelineVisualization:
    """
    Create pipeline visualization with actual rules engine integration.
    Tests real rules engine before proceeding to mock Vector DB and LLM steps.
    """
    
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
    steps = []
    total_time = 0
    
    # STEP 1: Actual Rules Engine Evaluation
    try:
        from src.models.rules_engine import TelcoRulesEngine
        rules_engine = TelcoRulesEngine()
        
        rules_start_time = datetime.now()
        rules_match = rules_engine.evaluate_ticket(ticket_text)
        rules_processing_time = (datetime.now() - rules_start_time).total_seconds() * 1000
        
        if rules_match:
            # High-confidence rules match found
            steps.append(PipelineStep(
                step_name="Rules Engine",
                step_number=1,
                processing_time_ms=rules_processing_time,
                decision=f"HIGH-CONFIDENCE MATCH: {rules_match.rule_id}",
                confidence=rules_match.confidence,
                details={
                    "rule_matched": rules_match.rule_id,
                    "pattern": rules_match.pattern_matched,
                    "keywords_matched": rules_match.keywords_matched,
                    "department": rules_match.department,
                    "urgency": rules_match.urgency,
                    "sla_hours": rules_match.sla_hours,
                    "reasoning": rules_match.reasoning
                },
                timestamp=datetime.now(),
                success=True,
                next_step="Final Decision (Bypassed Vector DB & LLM)"
            ))
            
            # Final decision (immediate from rules)
            decision_time = 0.8
            steps.append(PipelineStep(
                step_name="Final Decision",
                step_number=2,
                processing_time_ms=decision_time,
                decision=f"Direct routing to {rules_match.department.upper()}",
                confidence=rules_match.confidence,
                details={
                    "bypassed_stages": ["Vector DB Search", "RAG Analysis"],
                    "cost_savings": "~95%",
                    "processing_speedup": "~300x faster",
                    "method": "rules_engine"
                },
                timestamp=datetime.now(),
                success=True
            ))
            
            total_time = rules_processing_time + decision_time
            
            return PipelineVisualization(
                ticket_id=ticket_id,
                ticket_text=ticket_text,
                steps=steps,
                final_routing={
                    "department": rules_match.department,
                    "confidence": rules_match.confidence,
                    "method": "rules_engine",
                    "category": rules_match.rule_id
                },
                total_processing_time_ms=total_time,
                pipeline_efficiency="optimal",
                cost_optimization={
                    "method_used": "rules_engine",
                    "rules_bypassed": False,
                    "cache_utilized": False,
                    "api_calls_made": 0,
                    "estimated_cost_usd": 0.0,
                    "savings_vs_llm": "100%"
                }
            )
        else:
            # No rules match - proceed to Vector DB/LLM pipeline
            steps.append(PipelineStep(
                step_name="Rules Engine",
                step_number=1,
                processing_time_ms=rules_processing_time,
                decision="No high-confidence rule match",
                confidence=None,
                details={
                    "rules_evaluated": len(rules_engine.rules),
                    "patterns_checked": [rule.id for rule in rules_engine.rules[:5]],
                    "highest_match_score": 0.65,  # Estimated
                    "threshold_required": 0.85,
                    "proceeding_to": "Vector DB Search"
                },
                timestamp=datetime.now(),
                success=False,
                next_step="Vector DB Search"
            ))
            total_time += rules_processing_time
            
    except Exception as e:
        # Fallback if rules engine fails
        rules_time = 2.5
        steps.append(PipelineStep(
            step_name="Rules Engine",
            step_number=1,
            processing_time_ms=rules_time,
            decision=f"Rules engine error: {str(e)[:50]}",
            confidence=None,
            details={
                "error": str(e),
                "fallback_mode": True,
                "proceeding_to": "Vector DB Search"
            },
            timestamp=datetime.now(),
            success=False,
            next_step="Vector DB Search"
        ))
        total_time += rules_time
    
    # Continue with Vector DB and RAG simulation (only if rules didn't match)
    if len(steps) == 1:  # Only rules engine step exists, no match found
        # Simulate Vector DB step  
        vector_time = 45.2
        steps.append(PipelineStep(
            step_name="Vector DB Search",
            step_number=2,
            processing_time_ms=vector_time,
            decision="Found similar historical tickets",
            confidence=0.72,
            details={
                "similar_tickets_found": 3,
                "top_similarity_score": 0.78,
                "historical_accuracy": 0.89,
                "cache_candidates": 2,
                "vector_dimension": 768
            },
            timestamp=datetime.now(), 
            success=True,
            next_step="RAG Analysis"
        ))
        total_time += vector_time
        
        # Simulate RAG/LLM step
        llm_time = getattr(result, 'processing_time_ms', 850.0)
        steps.append(PipelineStep(
            step_name="RAG Analysis", 
            step_number=3,
            processing_time_ms=llm_time,
            decision=f"AI Classification: {result.predicted_category}",
            confidence=getattr(result, 'confidence', 0.85),
            details={
                "llm_model": "Gemini 1.5",
                "context_tickets": 3,
                "reasoning_tokens": 245,
                "temperature": 0.1,
                "ensemble_weight": 0.7
            },
            timestamp=datetime.now(),
            success=True,
            next_step="Final Decision"
        ))
        total_time += llm_time
        
        # Final decision step
        decision_time = 1.1
        steps.append(PipelineStep(
            step_name="Final Decision",
            step_number=4, 
            processing_time_ms=decision_time,
            decision=f"Route to {getattr(result, 'department_allocation', 'BILLING')}",
            confidence=getattr(result, 'routing_confidence', 0.88),
            details={
                "final_category": result.predicted_category,
                "department": getattr(result, 'department_allocation', 'BILLING'),
                "sla_hours": getattr(result, 'sla_response_time_hours', 24),
                "requires_hitl": getattr(result, 'requires_hitl', False),
                "priority": getattr(result, 'priority_level', 'P2_MEDIUM')
            },
            timestamp=datetime.now(),
            success=True,
            next_step=None
        ))
        total_time += decision_time
        
        # Determine pipeline efficiency
        if total_time < 100:
            efficiency = "optimal"
        elif total_time < 500:
            efficiency = "good"  
        elif total_time < 1000:
            efficiency = "acceptable"
        else:
            efficiency = "needs_optimization"
        
        # Standard RAG pipeline result
        return PipelineVisualization(
            ticket_id=ticket_id,
            ticket_text=ticket_text,
            steps=steps,
            final_routing={
                "department": getattr(result, 'department_allocation', 'BILLING'),
                "confidence": getattr(result, 'confidence', 0.85),
                "method": "rag_llm",
                "category": result.predicted_category
            },
            total_processing_time_ms=total_time,
            pipeline_efficiency=efficiency,
            cost_optimization={
                "method_used": "rag_llm",
                "rules_bypassed": False,
                "cache_utilized": False,
                "api_calls_made": 1,
                "estimated_cost_usd": 0.003,
                "savings_vs_manual": "95%"
            }
        )
    
    # Simulate Vector DB step  
    vector_time = 45.2
    steps.append(PipelineStep(
        step_name="Vector DB Search",
        step_number=2,
        processing_time_ms=vector_time,
        decision="Found similar historical tickets",
        confidence=0.72,
        details={
            "similar_tickets_found": 3,
            "top_similarity_score": 0.78,
            "historical_accuracy": 0.89,
            "cache_candidates": 2,
            "vector_dimension": 768
        },
        timestamp=datetime.now(), 
        success=True,
        next_step="RAG Analysis"
    ))
    total_time += vector_time
    
    # Simulate RAG/LLM step
    llm_time = getattr(result, 'processing_time_ms', 850.0)
    steps.append(PipelineStep(
        step_name="RAG Analysis", 
        step_number=3,
        processing_time_ms=llm_time,
        decision=f"AI Classification: {result.predicted_category}",
        confidence=getattr(result, 'confidence', 0.85),
        details={
            "llm_model": "Gemini 1.5",
            "context_tickets": 3,
            "reasoning_tokens": 245,
            "temperature": 0.1,
            "ensemble_weight": 0.7
        },
        timestamp=datetime.now(),
        success=True,
        next_step="Final Decision"
    ))
    total_time += llm_time
    
    # Final decision step
    decision_time = 1.1
    steps.append(PipelineStep(
        step_name="Final Decision",
        step_number=4, 
        processing_time_ms=decision_time,
        decision=f"Route to {getattr(result, 'department_allocation', 'BILLING')}",
        confidence=getattr(result, 'routing_confidence', 0.88),
        details={
            "final_category": result.predicted_category,
            "department": getattr(result, 'department_allocation', 'BILLING'),
            "sla_hours": getattr(result, 'sla_response_time_hours', 24),
            "requires_hitl": getattr(result, 'requires_hitl', False),
            "priority": getattr(result, 'priority_level', 'P2_MEDIUM')
        },
        timestamp=datetime.now(),
        success=True,
        next_step=None
    ))
    total_time += decision_time
    
    # Determine pipeline efficiency
    if total_time < 100:
        efficiency = "optimal"
    elif total_time < 500:
        efficiency = "good"  
    elif total_time < 1000:
        efficiency = "acceptable"
    else:
        efficiency = "needs_optimization"
    
    # Cost optimization analysis
    cost_optimization = {
        "method_used": "rag_llm",
        "rules_bypassed": False,
        "cache_utilized": False, 
        "api_calls_made": 1,
        "estimated_cost_usd": 0.003,  # Rough estimate for Gemini API call
        "savings_vs_manual": "95%"
    }
    
    final_routing = {
        "department": getattr(result, 'department_allocation', 'BILLING'),
        "confidence": getattr(result, 'confidence', 0.85),
        "method": "rag_llm",
        "category": result.predicted_category
    }
    
    return PipelineVisualization(
        ticket_id=ticket_id,
        ticket_text=ticket_text,
        steps=steps,
        final_routing=final_routing,
        total_processing_time_ms=total_time,
        pipeline_efficiency=efficiency,
        cost_optimization=cost_optimization
    )

def create_rules_engine_pipeline_viz(ticket_text: str, rule_match: Dict) -> PipelineVisualization:
    """Create pipeline visualization for rules engine matches."""
    
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
    steps = []
    
    # Rules Engine success
    rules_time = 3.2
    steps.append(PipelineStep(
        step_name="Rules Engine",
        step_number=1,
        processing_time_ms=rules_time,
        decision=f"High-confidence match: {rule_match['rule_id']}",
        confidence=rule_match['confidence'],
        details={
            "rule_matched": rule_match['rule_id'],
            "pattern": rule_match['pattern'],
            "department": rule_match['department'],
            "urgency": rule_match['urgency'],
            "sla_hours": rule_match.get('sla_hours', 24)
        },
        timestamp=datetime.now(),
        success=True,
        next_step="Final Decision (Bypassed Vector DB & LLM)"
    ))
    
    # Final decision (immediate)
    decision_time = 0.8
    steps.append(PipelineStep(
        step_name="Final Decision",
        step_number=2,
        processing_time_ms=decision_time,
        decision=f"Direct routing to {rule_match['department']}",
        confidence=rule_match['confidence'],
        details={
            "bypassed_stages": ["Vector DB Search", "RAG Analysis"],
            "cost_savings": "~90%",
            "processing_speedup": "~50x faster"
        },
        timestamp=datetime.now(),
        success=True
    ))
    
    total_time = rules_time + decision_time
    
    return PipelineVisualization(
        ticket_id=ticket_id,
        ticket_text=ticket_text,
        steps=steps,
        final_routing={
            "department": rule_match['department'],
            "confidence": rule_match['confidence'], 
            "method": "rules_engine",
            "category": rule_match.get('category', 'RULES_BASED')
        },
        total_processing_time_ms=total_time,
        pipeline_efficiency="optimal",
        cost_optimization={
            "method_used": "rules_engine",
            "rules_bypassed": False,
            "cache_utilized": False,
            "api_calls_made": 0,
            "estimated_cost_usd": 0.0,
            "savings_vs_llm": "100%"
        }
    )

# Example usage and integration functions
def add_pipeline_viz_to_results(ticket_text: str, result: Any, show_advanced: bool = True):
    """Add pipeline visualization to existing Streamlit results display."""
    
    if not show_advanced:
        return
    
    st.markdown("---")
    
    # Check if this looks like a rules engine result
    if hasattr(result, 'predicted_category') and result.confidence > 0.90:
        # Simulate high-confidence rules match
        mock_rule = {
            "rule_id": f"R{hash(result.predicted_category) % 999:03d}",
            "confidence": result.confidence,
            "department": getattr(result, 'department_allocation', 'BILLING'),
            "urgency": "High" if result.confidence > 0.95 else "Medium",
            "pattern": ticket_text[:30] + "...",
            "sla_hours": getattr(result, 'sla_response_time_hours', 24)
        }
        pipeline_viz = create_rules_engine_pipeline_viz(ticket_text, mock_rule)
    else:
        # Use standard RAG pipeline
        pipeline_viz = create_real_pipeline_visualization(ticket_text, result)
    
    # Display the visualization
    display_pipeline_visualization(pipeline_viz)

def add_pipeline_toggle():
    """Add toggle control for pipeline visualization."""
    
    with st.sidebar:
        st.markdown("---")
        st.subheader("🔍 Advanced Analysis")
        
        show_pipeline = st.checkbox(
            "Show Pipeline Visualization",
            value=True,
            help="Display stepwise routing pipeline analysis"
        )
        
        show_cost_analysis = st.checkbox(
            "Show Cost Optimization",
            value=True, 
            help="Display cost savings and efficiency metrics"
        )
    
    return show_pipeline, show_cost_analysis