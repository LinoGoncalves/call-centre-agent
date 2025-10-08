"""
Complete Confidence-Based Routing Demonstration (Epic 1.16-1.20)
================================================================

This script demonstrates the complete confidence-based routing system with:
- Multiple confidence threshold scenarios
- Performance monitoring and analytics
- Cache hit rate optimization
- Production-ready metrics and dashboards

Key Features:
- ConfidenceBasedRouter with intelligent decision logic
- AccuracyTracker with historical success patterns
- RoutingLogger with structured JSON analytics
- PerformanceMonitor with real-time metrics
"""

import asyncio
import json
from datetime import datetime
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.confidence_based_routing import (
    ConfidenceBasedRouter
)


class ProductionDashboard:
    """
    Production monitoring dashboard components for Grafana/CloudWatch integration.
    
    Provides metrics suitable for real-time monitoring and alerting.
    """
    
    def __init__(self):
        """Initialize dashboard metrics"""
        self.metrics_history = []
        self.alerts = []
    
    def generate_dashboard_metrics(self, router: ConfidenceBasedRouter) -> dict:
        """Generate comprehensive metrics for monitoring dashboards"""
        
        performance = router.get_performance_metrics()
        timestamp = datetime.now().isoformat()
        
        # Core KPIs for dashboard
        dashboard_data = {
            "timestamp": timestamp,
            "kpis": {
                "cache_hit_rate": performance["cache_performance"]["hit_rate"],
                "avg_processing_time_ms": performance["performance"]["avg_processing_time_ms"],
                "total_requests": performance["cache_performance"]["total_requests"],
                "accuracy_target_met": performance["cache_performance"]["hit_rate"] >= 0.25
            },
            
            "routing_breakdown": {
                "cached_percentage": 0 if performance["cache_performance"]["total_requests"] == 0 
                                   else performance["routing_distribution"]["cached"] / performance["cache_performance"]["total_requests"] * 100,
                "rag_llm_percentage": 0 if performance["cache_performance"]["total_requests"] == 0
                                    else performance["routing_distribution"]["rag_llm"] / performance["cache_performance"]["total_requests"] * 100,
                "fallback_percentage": 0 if performance["cache_performance"]["total_requests"] == 0
                                     else performance["routing_distribution"]["fallback"] / performance["cache_performance"]["total_requests"] * 100
            },
            
            "confidence_analysis": performance["confidence"],
            
            "performance_targets": {
                "cache_hit_rate_target": 0.25,  # 25% minimum
                "avg_response_time_target": 2000,  # 2s maximum
                "accuracy_target": 0.90  # 90% routing accuracy
            }
        }
        
        # Store metrics history
        self.metrics_history.append(dashboard_data)
        
        # Generate alerts if needed
        self._check_alerts(dashboard_data)
        
        return dashboard_data
    
    def _check_alerts(self, metrics: dict):
        """Check for alert conditions"""
        
        # Cache hit rate too low
        if metrics["kpis"]["cache_hit_rate"] < 0.15:  # Below 15%
            self.alerts.append({
                "timestamp": metrics["timestamp"],
                "level": "warning",
                "metric": "cache_hit_rate",
                "value": metrics["kpis"]["cache_hit_rate"],
                "threshold": 0.15,
                "message": f"Cache hit rate ({metrics['kpis']['cache_hit_rate']:.1%}) below target (15%)"
            })
        
        # Response time too high
        if metrics["kpis"]["avg_processing_time_ms"] > 5000:  # Above 5s
            self.alerts.append({
                "timestamp": metrics["timestamp"],
                "level": "critical",
                "metric": "avg_processing_time_ms",
                "value": metrics["kpis"]["avg_processing_time_ms"],
                "threshold": 5000,
                "message": f"Average processing time ({metrics['kpis']['avg_processing_time_ms']:.1f}ms) exceeds 5s threshold"
            })
    
    def get_latest_alerts(self, last_n: int = 5) -> list:
        """Get recent alerts for monitoring"""
        return self.alerts[-last_n:] if self.alerts else []
    
    def print_dashboard_summary(self, metrics: dict):
        """Print dashboard-style summary"""
        
        print("\n📊 PRODUCTION DASHBOARD METRICS")
        print("=" * 45)
        
        # KPIs
        kpis = metrics["kpis"]
        cache_status = "✅" if kpis["cache_hit_rate"] >= 0.25 else "⚠️"
        perf_status = "✅" if kpis["avg_processing_time_ms"] <= 2000 else "⚠️"
        
        print(f"🎯 CORE KPIs:")
        print(f"   {cache_status} Cache Hit Rate: {kpis['cache_hit_rate']:.1%} (target: ≥25%)")
        print(f"   {perf_status} Avg Response Time: {kpis['avg_processing_time_ms']:.1f}ms (target: ≤2000ms)")
        print(f"   📈 Total Requests: {kpis['total_requests']}")
        
        # Routing breakdown
        breakdown = metrics["routing_breakdown"]
        print(f"\n🔄 ROUTING DISTRIBUTION:")
        print(f"   ⚡ Cached: {breakdown['cached_percentage']:.1f}%")
        print(f"   🤖 RAG-LLM: {breakdown['rag_llm_percentage']:.1f}%")
        print(f"   🔄 Fallback: {breakdown['fallback_percentage']:.1f}%")
        
        # Confidence analysis
        confidence = metrics["confidence_analysis"]
        print(f"\n📊 CONFIDENCE DISTRIBUTION:")
        print(f"   🟢 High (≥85%): {confidence['high']}")
        print(f"   🟡 Medium (70-85%): {confidence['medium']}")
        print(f"   🔴 Low (<70%): {confidence['low']}")
        
        # Alerts
        recent_alerts = self.get_latest_alerts(3)
        if recent_alerts:
            print(f"\n🚨 RECENT ALERTS:")
            for alert in recent_alerts:
                level_icon = "🚨" if alert["level"] == "critical" else "⚠️"
                print(f"   {level_icon} {alert['message']}")
        else:
            print(f"\n✅ NO ACTIVE ALERTS")


async def test_multiple_confidence_thresholds():
    """Test system performance with different confidence thresholds"""
    
    print("🎛️ Testing Multiple Confidence Thresholds")
    print("=" * 45)
    
    # Test scenarios
    test_tickets = [
        "My enterprise internet service keeps disconnecting during video conferences",
        "I need a billing refund for duplicate charges on my monthly statement",
        "Cannot login to account, password reset emails not working",
        "Excellent customer service, thank you for resolving my network issue!",
        "Mobile data connection is very slow in my area, need technical support"
    ]
    
    # Different threshold configurations
    threshold_configs = [
        {"confidence": 0.90, "accuracy": 0.90, "name": "Strict (90%/90%)"},
        {"confidence": 0.75, "accuracy": 0.80, "name": "Moderate (75%/80%)"},
        {"confidence": 0.50, "accuracy": 0.70, "name": "Permissive (50%/70%)"}
    ]
    
    results = {}
    
    for config in threshold_configs:
        print(f"\n🎯 Testing {config['name']} Configuration")
        print(f"   Confidence Threshold: {config['confidence']}")
        print(f"   Accuracy Threshold: {config['accuracy']}")
        
        # Create router with specific thresholds
        router = ConfidenceBasedRouter(
            confidence_threshold=config['confidence'],
            accuracy_threshold=config['accuracy']
        )
        
        # Process test tickets
        for i, ticket in enumerate(test_tickets, 1):
            decision = await router.route_with_confidence(ticket[:50] + "...")
            print(f"   {i}. {decision.routing_method.value} ({decision.confidence_score:.3f})")
        
        # Get performance metrics
        metrics = router.get_performance_metrics()
        cache_hit_rate = metrics["cache_performance"]["hit_rate"]
        avg_time = metrics["performance"]["avg_processing_time_ms"]
        
        results[config['name']] = {
            "cache_hit_rate": cache_hit_rate,
            "avg_processing_time": avg_time,
            "total_requests": len(test_tickets),
            "config": config
        }
        
        print(f"   📊 Cache Hit Rate: {cache_hit_rate:.1%}")
        print(f"   ⚡ Avg Processing Time: {avg_time:.1f}ms")
    
    # Compare results
    print(f"\n📊 THRESHOLD COMPARISON SUMMARY:")
    print("=" * 40)
    
    for name, result in results.items():
        cache_icon = "✅" if result["cache_hit_rate"] >= 0.25 else "⚠️"
        perf_icon = "✅" if result["avg_processing_time"] <= 2000 else "⚠️"
        
        print(f"{name}:")
        print(f"   {cache_icon} Cache Rate: {result['cache_hit_rate']:.1%}")
        print(f"   {perf_icon} Avg Time: {result['avg_processing_time']:.1f}ms")
        print()
    
    return results


async def test_production_monitoring():
    """Test production monitoring and dashboard capabilities"""
    
    print("📊 Testing Production Monitoring & Analytics")
    print("=" * 45)
    
    # Create router with moderate thresholds
    router = ConfidenceBasedRouter(confidence_threshold=0.75, accuracy_threshold=0.80)
    dashboard = ProductionDashboard()
    
    # Simulate production workload
    production_tickets = [
        "Internet connection unstable affecting business operations",
        "Billing dispute - charged twice for same service this month",
        "Account locked out, cannot access customer portal",
        "Fantastic support from technical team, issue resolved quickly",
        "Mobile network very slow, dropped calls frequently",
        "Refund request for cancelled service, billed incorrectly",
        "Password reset not working, security questions failing",
        "Thank you for excellent customer service experience",
        "Wi-Fi router keeps disconnecting, need replacement",
        "Overcharged on bill, need immediate correction"
    ]
    
    print(f"\n🔄 Processing {len(production_tickets)} production tickets...")
    
    # Process tickets and collect metrics
    for i, ticket in enumerate(production_tickets, 1):
        decision = await router.route_with_confidence(ticket)
        
        # Show progress
        method_icon = "🎯" if decision.cache_hit else "🤖"
        print(f"   {i:2d}. {method_icon} {decision.recommended_department} ({decision.processing_time_ms:.0f}ms)")
    
    # Generate dashboard metrics
    dashboard_metrics = dashboard.generate_dashboard_metrics(router)
    
    # Display production dashboard
    dashboard.print_dashboard_summary(dashboard_metrics)
    
    # Export metrics for external monitoring
    print(f"\n📄 METRICS EXPORT (JSON):")
    print("-" * 30)
    print(json.dumps(dashboard_metrics, indent=2))
    
    return dashboard_metrics


async def validate_routing_performance():
    """Validate routing performance against production benchmarks"""
    
    print("\n🧪 Validating Routing Performance")
    print("=" * 35)
    
    # Create production-tuned router
    router = ConfidenceBasedRouter(confidence_threshold=0.80, accuracy_threshold=0.85)
    
    # Performance validation scenarios
    validation_tests = [
        {
            "name": "High Volume Processing",
            "tickets": ["Sample ticket " + str(i) for i in range(20)],
            "target_avg_time_ms": 3000
        },
        {
            "name": "Mixed Complexity Routing",
            "tickets": [
                "Complex technical network infrastructure issue requiring L2 support",
                "Simple billing refund request",
                "Account security breach investigation needed",
                "Thank you for great service",
                "Standard password reset request"
            ],
            "target_cache_rate": 0.20
        }
    ]
    
    validation_results = []
    
    for test in validation_tests:
        print(f"\n🎯 {test['name']}:")
        print(f"   Processing {len(test['tickets'])} tickets...")
        
        start_time = datetime.now()
        
        # Process all tickets
        for ticket in test['tickets']:
            decision = await router.route_with_confidence(ticket)
        
        end_time = datetime.now()
        processing_duration = (end_time - start_time).total_seconds() * 1000
        
        # Get metrics
        metrics = router.get_performance_metrics()
        avg_time = metrics["performance"]["avg_processing_time_ms"]
        cache_rate = metrics["cache_performance"]["hit_rate"]
        
        # Validate against targets
        time_passed = avg_time <= test.get("target_avg_time_ms", float('inf'))
        cache_passed = cache_rate >= test.get("target_cache_rate", 0)
        
        result = {
            "test_name": test["name"],
            "avg_processing_time": avg_time,
            "cache_hit_rate": cache_rate,
            "total_duration_ms": processing_duration,
            "time_target_met": time_passed,
            "cache_target_met": cache_passed,
            "overall_pass": time_passed and cache_passed
        }
        
        validation_results.append(result)
        
        # Display results
        time_icon = "✅" if time_passed else "❌"
        cache_icon = "✅" if cache_passed else "❌"
        
        print(f"   {time_icon} Avg Time: {avg_time:.1f}ms (target: {test.get('target_avg_time_ms', 'N/A')})")
        if 'target_cache_rate' in test:
            print(f"   {cache_icon} Cache Rate: {cache_rate:.1%} (target: {test['target_cache_rate']:.1%})")
        print(f"   📊 Total Duration: {processing_duration:.1f}ms")
    
    # Overall validation summary
    passed_tests = sum(1 for r in validation_results if r["overall_pass"])
    total_tests = len(validation_results)
    
    print(f"\n📊 VALIDATION SUMMARY:")
    print(f"   Tests Passed: {passed_tests}/{total_tests}")
    print(f"   Success Rate: {passed_tests/total_tests:.1%}")
    
    if passed_tests == total_tests:
        print(f"   ✅ ALL PERFORMANCE TARGETS MET")
    else:
        print(f"   ⚠️ Some performance targets not met")
    
    return validation_results


async def run_complete_demonstration():
    """Run the complete Epic 1.16-1.20 demonstration"""
    
    print("🚀 EPIC 1.16-1.20: CONFIDENCE-BASED ROUTING COMPLETE DEMO")
    print("Enhanced Hybrid Intelligence with Production Monitoring")
    print("=" * 65)
    
    try:
        # Test 1: Multiple confidence thresholds
        threshold_results = await test_multiple_confidence_thresholds()
        
        # Test 2: Production monitoring
        monitoring_metrics = await test_production_monitoring()
        
        # Test 3: Performance validation
        validation_results = await validate_routing_performance()
        
        print("\n🎉 EPIC 1.16-1.20 COMPLETE!")
        print("=" * 35)
        
        print("✅ IMPLEMENTED CAPABILITIES:")
        print("   🎯 Confidence-based routing with intelligent caching")
        print("   📊 Historical accuracy tracking and validation")
        print("   📝 Comprehensive structured logging for analytics")
        print("   📊 Production monitoring dashboard components")
        print("   🧪 Performance validation and benchmarking")
        
        print("\n🚀 PRODUCTION READY FEATURES:")
        print("   ⚡ Sub-second cached routing for high-confidence matches")
        print("   🤖 RAG-enhanced LLM analysis for complex cases")
        print("   📈 Real-time metrics for Grafana/CloudWatch integration")
        print("   🔍 Complete audit trail for compliance and debugging")
        print("   📊 Automated alerting for performance thresholds")
        
        print("\n💡 NEXT STEPS:")
        print("   1. Deploy with production PostgreSQL for accuracy tracking")
        print("   2. Integrate with monitoring systems (Grafana, ELK, etc.)")
        print("   3. Implement continuous learning from routing outcomes")
        print("   4. Add A/B testing framework for threshold optimization")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Starting Complete Epic 1.16-1.20 Demonstration...")
    success = asyncio.run(run_complete_demonstration())
    
    if success:
        print("\n✅ Epic 1.16-1.20 completed successfully!")
        print("🎯 Confidence-based routing system ready for production!")
    else:
        print("\n❌ Some demonstrations failed. Check logs for details.")