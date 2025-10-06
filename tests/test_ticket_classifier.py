"""
Unit tests for the ticket classification system
Ensuring 80%+ test coverage as per development standards
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.ticket_classifier import TicketClassificationPipeline
from src.data.mock_data_generator import TelecomsTicketGenerator


class TestTicketClassificationPipeline:
    """Test suite for the main classification pipeline."""
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing."""
        generator = TelecomsTicketGenerator(seed=42)
        dataset = generator.generate_dataset()
        
        # Use smaller sample for fast tests
        sample_size = min(1000, len(dataset))
        dataset_sample = dataset.sample(n=sample_size, random_state=42)
        
        X = dataset_sample['ticket_text'].tolist()
        y = dataset_sample['category'].tolist()
        
        return X, y
    
    @pytest.fixture
    def trained_pipeline(self, sample_data):
        """Create a trained pipeline for testing."""
        X, y = sample_data
        
        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Train pipeline
        pipeline = TicketClassificationPipeline(random_state=42)
        pipeline.fit(X_train, y_train, X_val, y_val)
        
        return pipeline
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization."""
        pipeline = TicketClassificationPipeline(random_state=42)
        
        assert pipeline.random_state == 42
        assert len(pipeline.models) == 0
        assert len(pipeline.ensemble_weights) == 0
    
    def test_text_preprocessing(self):
        """Test text preprocessing functionality."""
        pipeline = TicketClassificationPipeline()
        
        # Test various text inputs
        test_cases = [
            ("My BILL is too HIGH!!!", "my bill is too high!!!"),
            ("  Extra    spaces  ", "extra spaces"),
            ("Special chars: @#$%", "special chars:")
        ]
        
        for input_text, expected in test_cases:
            result = pipeline._preprocess_text(input_text)
            assert result == expected
    
    def test_pipeline_training(self, sample_data):
        """Test the training process."""
        X, y = sample_data
        
        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        pipeline = TicketClassificationPipeline(random_state=42)
        results = pipeline.fit(X_train, y_train, X_val, y_val)
        
        # Check that models are trained
        assert 'logistic_regression' in pipeline.models
        assert 'random_forest' in pipeline.models
        
        # Check that results are returned
        assert 'logistic_regression_accuracy' in results
        assert 'random_forest_accuracy' in results
        
        # Check ensemble weights are set
        assert len(pipeline.ensemble_weights) == 2
        assert sum(pipeline.ensemble_weights.values()) == pytest.approx(1.0, rel=1e-3)
    
    def test_prediction_functionality(self, trained_pipeline):
        """Test prediction methods."""
        test_texts = [
            "My bill is too expensive this month",
            "Internet connection is very slow",
            "I want to upgrade my plan"
        ]
        
        # Test predict method
        predictions = trained_pipeline.predict(test_texts)
        assert len(predictions) == len(test_texts)
        assert all(isinstance(pred, str) for pred in predictions)
        
        # Test predict_proba method
        probabilities = trained_pipeline.predict_proba(test_texts)
        assert probabilities.shape == (len(test_texts), 6)  # 6 categories
        assert np.allclose(probabilities.sum(axis=1), 1.0)  # Probabilities sum to 1
    
    def test_evaluation_metrics(self, trained_pipeline, sample_data):
        """Test evaluation functionality."""
        X, y = sample_data
        
        # Use small test set
        X_test = X[-100:]
        y_test = y[-100:]
        
        results = trained_pipeline.evaluate(X_test, y_test)
        
        # Check required metrics are present
        required_keys = [
            'accuracy', 'inference_time_total', 'avg_inference_time_ms',
            'samples_evaluated', 'classification_report', 
            'meets_accuracy_target', 'meets_speed_target'
        ]
        
        for key in required_keys:
            assert key in results
        
        # Check metric values are reasonable
        assert 0.0 <= results['accuracy'] <= 1.0
        assert results['avg_inference_time_ms'] > 0
        assert results['samples_evaluated'] == len(X_test)
    
    def test_model_persistence(self, trained_pipeline, tmp_path):
        """Test model saving and loading."""
        # Save model
        model_path = tmp_path / "test_model.pkl"
        trained_pipeline.save_model(str(model_path))
        
        assert model_path.exists()
        
        # Load model into new pipeline
        new_pipeline = TicketClassificationPipeline()
        new_pipeline.load_model(str(model_path))
        
        # Check that models are loaded
        assert len(new_pipeline.models) == 2
        assert len(new_pipeline.ensemble_weights) == 2
        
        # Test that predictions work
        test_text = ["My internet is slow"]
        original_pred = trained_pipeline.predict(test_text)
        loaded_pred = new_pipeline.predict(test_text)
        
        assert original_pred == loaded_pred


class TestTelecomsTicketGenerator:
    """Test suite for the data generation component."""
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        generator = TelecomsTicketGenerator(seed=42)
        
        assert generator.fake.seed_instance == 42
        assert len(generator.categories) == 6
        assert sum(generator.categories.values()) >= 5000  # Total should be 5000+
    
    def test_dataset_generation(self):
        """Test dataset generation."""
        generator = TelecomsTicketGenerator(seed=42)
        # Use smaller dataset for testing
        generator.categories = {cat: 100 for cat in generator.categories.keys()}
        
        dataset = generator.generate_dataset()
        
        # Check dataset structure
        expected_columns = ['ticket_id', 'category', 'ticket_text', 'priority', 
                          'created_date', 'customer_type', 'location']
        assert all(col in dataset.columns for col in expected_columns)
        
        # Check data quality
        assert len(dataset) == 600  # 6 categories * 100 each
        assert dataset['category'].nunique() == 6
        assert dataset['ticket_text'].str.len().min() >= 10
        assert dataset['ticket_text'].str.len().max() <= 500
    
    def test_category_text_generation(self):
        """Test category-specific text generation."""
        generator = TelecomsTicketGenerator(seed=42)
        
        # Test each category generates appropriate text
        for category in generator.categories.keys():
            text = generator._generate_category_text(category)
            assert isinstance(text, str)
            assert len(text) > 0
    
    def test_data_quality_validation(self):
        """Test data quality validation."""
        generator = TelecomsTicketGenerator(seed=42)
        # Use smaller dataset
        generator.categories = {cat: 50 for cat in generator.categories.keys()}
        
        dataset = generator.generate_dataset()
        quality_report = generator._generate_quality_report(dataset)
        
        # Check quality metrics
        assert isinstance(quality_report, dict)
        assert 'no_duplicates' in quality_report
        assert 'no_missing_values' in quality_report
        assert 'category_coverage' in quality_report


class TestAPIIntegration:
    """Integration tests for the FastAPI application."""
    
    @pytest.fixture
    def mock_model(self):
        """Create a mock model for API testing."""
        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = ['BILLING']
        mock_pipeline.predict_proba.return_value = np.array([[0.1, 0.8, 0.05, 0.03, 0.01, 0.01]])
        return mock_pipeline
    
    @patch('src.api.main.model_pipeline')
    def test_health_endpoint(self, mock_model_global):
        """Test health check endpoint."""
        from fastapi.testclient import TestClient
        from src.api.main import app
        
        mock_model_global.return_value = Mock()
        client = TestClient(app)
        
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
    
    @patch('src.api.main.model_pipeline')
    def test_classification_endpoint(self, mock_model_global, mock_model):
        """Test single ticket classification endpoint."""
        from fastapi.testclient import TestClient
        from src.api.main import app
        
        mock_model_global = mock_model
        app.dependency_overrides = {}
        
        client = TestClient(app)
        
        # Test successful classification
        test_request = {
            "ticket_text": "My bill is too high this month",
            "ticket_id": "TEST123"
        }
        
        with patch('src.api.main.model_pipeline', mock_model):
            response = client.post("/classify", json=test_request)
        
        assert response.status_code == 200
        
        data = response.json()
        assert "predicted_category" in data
        assert "confidence" in data
        assert "processing_time_ms" in data
    
    def test_categories_endpoint(self):
        """Test categories information endpoint."""
        from fastapi.testclient import TestClient
        from src.api.main import app
        
        client = TestClient(app)
        
        response = client.get("/categories")
        assert response.status_code == 200
        
        data = response.json()
        assert "categories" in data
        assert "total_categories" in data
        assert data["total_categories"] == 6


@pytest.mark.integration
class TestEndToEndWorkflow:
    """End-to-end integration tests."""
    
    def test_complete_pipeline_workflow(self):
        """Test the complete ML pipeline from data generation to prediction."""
        # Generate data
        generator = TelecomsTicketGenerator(seed=42)
        # Use smaller dataset for testing
        generator.categories = {cat: 200 for cat in generator.categories.keys()}
        
        dataset = generator.generate_dataset()
        
        # Prepare data
        X = dataset['ticket_text'].tolist()
        y = dataset['category'].tolist()
        
        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train model
        pipeline = TicketClassificationPipeline(random_state=42)
        results = pipeline.fit(X_train, y_train)
        
        # Evaluate model
        evaluation = pipeline.evaluate(X_test, y_test)
        
        # Check that the pipeline meets basic requirements
        assert evaluation['accuracy'] > 0.5  # At least better than random
        assert evaluation['avg_inference_time_ms'] < 5000  # Reasonable speed
        assert len(pipeline.models) == 2  # Both models trained


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])