#!/usr/bin/env python3
"""
Training script for Telco Call Centre Ticket Classification
Executes the hybrid ensemble model training pipeline
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Add src to Python path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

from models.ticket_classifier import TicketClassificationPipeline
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Execute the complete training pipeline."""
    logger.info("🎯 Starting Telco Call Centre Ticket Classification Training")
    
    # Load datasets
    try:
        train_df = pd.read_csv('data/telecoms_tickets_train.csv')
        val_df = pd.read_csv('data/telecoms_tickets_val.csv')
        test_df = pd.read_csv('data/telecoms_tickets_test.csv')
        
        logger.info(f"📊 Data loaded successfully:")
        logger.info(f"   Training: {len(train_df)} samples")
        logger.info(f"   Validation: {len(val_df)} samples") 
        logger.info(f"   Test: {len(test_df)} samples")
        
    except FileNotFoundError as e:
        logger.error(f"❌ Data files not found: {e}")
        logger.error("💡 Please run 'python src/data/mock_data_generator.py' first")
        return False
    
    # Prepare data
    X_train = train_df['ticket_text'].tolist()
    y_train = train_df['category'].tolist()
    X_val = val_df['ticket_text'].tolist()
    y_val = val_df['category'].tolist()
    X_test = test_df['ticket_text'].tolist()
    y_test = test_df['category'].tolist()
    
    # Initialize and train pipeline
    pipeline = TicketClassificationPipeline(random_state=42)
    
    logger.info("🚀 Training hybrid ensemble models...")
    training_results = pipeline.fit(X_train, y_train, X_val, y_val)
    
    # Evaluate on test set
    logger.info("📈 Evaluating model performance...")
    evaluation_results = pipeline.evaluate(X_test, y_test)
    
    # Save trained model
    model_path = 'models/telco_ticket_classifier.pkl'
    os.makedirs('models', exist_ok=True)
    pipeline.save_model(model_path)
    
    # Final results summary
    logger.info("\n" + "="*60)
    logger.info("🎉 TRAINING COMPLETE - FINAL RESULTS")
    logger.info("="*60)
    logger.info(f"📊 Test Accuracy: {evaluation_results['accuracy']:.4f}")
    logger.info(f"🎯 Accuracy Target (≥85%): {'✅ PASSED' if evaluation_results['meets_accuracy_target'] else '❌ FAILED'}")
    logger.info(f"⚡ Avg Inference Time: {evaluation_results['avg_inference_time_ms']:.2f}ms")
    logger.info(f"🚀 Speed Target (<2s): {'✅ PASSED' if evaluation_results['meets_speed_target'] else '❌ FAILED'}")
    logger.info(f"💾 Model saved to: {model_path}")
    logger.info("="*60)
    
    # Performance validation
    success = (evaluation_results['meets_accuracy_target'] and 
               evaluation_results['meets_speed_target'])
    
    if success:
        logger.info("✅ MODEL TRAINING SUCCESSFUL - All targets met!")
        return True
    else:
        logger.warning("⚠️ MODEL TRAINING NEEDS ATTENTION - Some targets not met")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)