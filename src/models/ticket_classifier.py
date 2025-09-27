"""
Ticket Classification Model Implementation
Hybrid ensemble approach: Traditional ML + Transformer models
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
import pickle
import time
from typing import Dict, List, Tuple, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TicketClassificationPipeline:
    """Hybrid ensemble pipeline for ticket classification."""
    
    def __init__(self, random_state: int = 42) -> None:
        """Initialize the classification pipeline."""
        self.random_state = random_state
        self.models: Dict[str, Any] = {}
        self.vectorizers: Dict[str, Any] = {}
        self.ensemble_weights: Dict[str, float] = {}
        self.label_encoder = None
        self.training_history: Dict[str, Any] = {}
        
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess ticket text."""
        import re
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters (keep punctuation for context)
        text = re.sub(r'[^\w\s\.\,\!\?]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _create_traditional_pipeline(self) -> Pipeline:
        """Create traditional ML pipeline with TF-IDF + Logistic Regression."""
        return Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=10000,
                ngram_range=(1, 2),
                stop_words='english',
                min_df=2,
                max_df=0.95,
                sublinear_tf=True
            )),
            ('classifier', LogisticRegression(
                random_state=self.random_state,
                max_iter=1000,
                class_weight='balanced',
                solver='liblinear'
            ))
        ])
    
    def _create_ensemble_pipeline(self) -> Pipeline:
        """Create ensemble ML pipeline with TF-IDF + Random Forest."""
        return Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=8000,
                ngram_range=(1, 3),
                stop_words='english',
                min_df=3,
                max_df=0.90
            )),
            ('classifier', RandomForestClassifier(
                n_estimators=100,
                random_state=self.random_state,
                class_weight='balanced',
                max_depth=20,
                min_samples_split=5
            ))
        ])
    
    def fit(self, X_train: List[str], y_train: List[str], 
            X_val: List[str] = None, y_val: List[str] = None) -> Dict[str, float]:
        """Train all models in the ensemble."""
        logger.info("🚀 Starting model training...")
        
        # Preprocess text data
        X_train_processed = [self._preprocess_text(text) for text in X_train]
        if X_val is not None:
            X_val_processed = [self._preprocess_text(text) for text in X_val]
        
        results = {}
        
        # Train traditional model (fast baseline)
        logger.info("📊 Training Logistic Regression model...")
        start_time = time.time()
        
        self.models['logistic_regression'] = self._create_traditional_pipeline()
        self.models['logistic_regression'].fit(X_train_processed, y_train)
        
        training_time_lr = time.time() - start_time
        
        if X_val is not None:
            y_pred_lr = self.models['logistic_regression'].predict(X_val_processed)
            lr_accuracy = accuracy_score(y_val, y_pred_lr)
            results['logistic_regression_accuracy'] = lr_accuracy
            logger.info(f"   ✅ LR Accuracy: {lr_accuracy:.4f}, Time: {training_time_lr:.2f}s")
        
        # Train ensemble model (higher accuracy)
        logger.info("🌲 Training Random Forest model...")
        start_time = time.time()
        
        self.models['random_forest'] = self._create_ensemble_pipeline()
        self.models['random_forest'].fit(X_train_processed, y_train)
        
        training_time_rf = time.time() - start_time
        
        if X_val is not None:
            y_pred_rf = self.models['random_forest'].predict(X_val_processed)
            rf_accuracy = accuracy_score(y_val, y_pred_rf)
            results['random_forest_accuracy'] = rf_accuracy
            logger.info(f"   ✅ RF Accuracy: {rf_accuracy:.4f}, Time: {training_time_rf:.2f}s")
            
            # Set ensemble weights based on validation performance
            total_accuracy = lr_accuracy + rf_accuracy
            self.ensemble_weights = {
                'logistic_regression': lr_accuracy / total_accuracy,
                'random_forest': rf_accuracy / total_accuracy
            }
            
            logger.info(f"🎯 Ensemble weights: LR={self.ensemble_weights['logistic_regression']:.3f}, "
                       f"RF={self.ensemble_weights['random_forest']:.3f}")
        
        # Store training history
        self.training_history = {
            'training_time_lr': training_time_lr,
            'training_time_rf': training_time_rf,
            'total_training_time': training_time_lr + training_time_rf,
            'results': results
        }
        
        logger.info("✅ Training complete!")
        return results
    
    def predict(self, X: List[str]) -> List[str]:
        """Make predictions using ensemble approach."""
        X_processed = [self._preprocess_text(text) for text in X]
        
        # Get predictions from both models
        pred_lr = self.models['logistic_regression'].predict(X_processed)
        pred_rf = self.models['random_forest'].predict(X_processed)
        
        # Get prediction probabilities for confidence-based ensemble
        proba_lr = self.models['logistic_regression'].predict_proba(X_processed)
        proba_rf = self.models['random_forest'].predict_proba(X_processed)
        
        # Weighted ensemble prediction
        ensemble_predictions = []
        
        for i in range(len(X_processed)):
            # Weight the probabilities
            weighted_proba = (
                self.ensemble_weights['logistic_regression'] * proba_lr[i] +
                self.ensemble_weights['random_forest'] * proba_rf[i]
            )
            
            # Get class with highest weighted probability
            predicted_class_idx = np.argmax(weighted_proba)
            predicted_class = self.models['logistic_regression'].classes_[predicted_class_idx]
            ensemble_predictions.append(predicted_class)
        
        return ensemble_predictions
    
    def predict_proba(self, X: List[str]) -> np.ndarray:
        """Get prediction probabilities from ensemble."""
        X_processed = [self._preprocess_text(text) for text in X]
        
        # Get probabilities from both models
        proba_lr = self.models['logistic_regression'].predict_proba(X_processed)
        proba_rf = self.models['random_forest'].predict_proba(X_processed)
        
        # Return weighted ensemble probabilities
        ensemble_proba = (
            self.ensemble_weights['logistic_regression'] * proba_lr +
            self.ensemble_weights['random_forest'] * proba_rf
        )
        
        return ensemble_proba
    
    def evaluate(self, X_test: List[str], y_test: List[str]) -> Dict[str, Any]:
        """Comprehensive model evaluation."""
        logger.info("📈 Starting model evaluation...")
        
        # Time the inference
        start_time = time.time()
        predictions = self.predict(X_test)
        inference_time = time.time() - start_time
        avg_inference_time = inference_time / len(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions, output_dict=True)
        
        # Model performance summary
        evaluation_results = {
            'accuracy': accuracy,
            'inference_time_total': inference_time,
            'avg_inference_time_ms': avg_inference_time * 1000,
            'samples_evaluated': len(X_test),
            'classification_report': report,
            'meets_accuracy_target': accuracy >= 0.85,
            'meets_speed_target': avg_inference_time < 2.0
        }
        
        logger.info(f"📊 Evaluation Results:")
        logger.info(f"   Accuracy: {accuracy:.4f}")
        logger.info(f"   Avg inference time: {avg_inference_time*1000:.2f}ms")
        logger.info(f"   Accuracy target (≥85%): {'✅' if evaluation_results['meets_accuracy_target'] else '❌'}")
        logger.info(f"   Speed target (<2s): {'✅' if evaluation_results['meets_speed_target'] else '❌'}")
        
        return evaluation_results
    
    def save_model(self, filepath: str) -> None:
        """Save the trained model pipeline."""
        model_data = {
            'models': self.models,
            'ensemble_weights': self.ensemble_weights,
            'training_history': self.training_history
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"💾 Model saved to {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """Load a trained model pipeline."""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.models = model_data['models']
        self.ensemble_weights = model_data['ensemble_weights']
        self.training_history = model_data['training_history']
        
        logger.info(f"📂 Model loaded from {filepath}")


def main():
    """Main training script."""
    logger.info("🎯 Starting Telkom Call Centre Ticket Classification Training")
    
    # This would normally load from the generated dataset
    # For now, we'll create a placeholder that shows the expected interface
    
    logger.info("📋 Training pipeline interface ready")
    logger.info("📁 Expected data files:")
    logger.info("   - data/telecoms_tickets_train.csv")
    logger.info("   - data/telecoms_tickets_val.csv") 
    logger.info("   - data/telecoms_tickets_test.csv")


if __name__ == "__main__":
    main()