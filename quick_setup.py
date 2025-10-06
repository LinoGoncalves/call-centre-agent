#!/usr/bin/env python3
"""
Quick training data generation and model training for demo
"""

import sys
import os
from pathlib import Path
import pandas as pd
import logging

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_data_and_train():
    """Generate training data and train a basic model."""
    try:
        logger.info("🔄 Generating mock training data...")
        
        # Import the mock data generator
        from src.data.mock_data_generator import TelecomsTicketGenerator
        
        # Generate dataset
        generator = TelecomsTicketGenerator()
        df = generator.generate_dataset()
        
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Split data for training
        train_size = int(0.8 * len(df))
        train_df = df[:train_size]
        val_df = df[train_size:]
        
        # Save datasets
        train_df.to_csv("data/telecoms_tickets_train.csv", index=False)
        val_df.to_csv("data/telecoms_tickets_val.csv", index=False)
        
        logger.info(f"✅ Generated {len(train_df)} training samples and {len(val_df)} validation samples")
        
        # Now try to train a basic model
        logger.info("🎯 Training basic model...")
        
        # Import and train
        from scripts.train_model import main as train_main
        train_main()
        
        logger.info("✅ Model training completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error during training: {e}")
        # Create a minimal mock model file as fallback
        logger.info("🔄 Creating minimal fallback model...")
        create_minimal_model()

def create_minimal_model():
    """Create a minimal model file to prevent initialization errors."""
    import pickle
    
    # Create minimal model structure
    model_data = {
        'models': {},  # Empty models dict
        'ensemble_weights': {},
        'training_history': []
    }
    
    # Ensure models directory exists
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Save minimal model
    model_path = models_dir / "telco_ticket_classifier.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    logger.info(f"✅ Created minimal model at {model_path}")

if __name__ == "__main__":
    generate_data_and_train()