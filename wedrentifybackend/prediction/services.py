# prediction/services.py
# Service layer for ML model operations

import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ModelService:
    """
    Service for loading and using the ML model
    """
    _instance = None
    _model = None
    _encoders = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        """Load the trained model"""
        try:
            model_path = settings.MODEL_PATH
            logger.info(f"Loading model from {model_path}")
            
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            if isinstance(model_data, dict):
                self._model = model_data.get('model')
                self._encoders = model_data.get('label_encoders', {})
                logger.info("✅ Model loaded successfully")
            else:
                self._model = model_data
                self._encoders = {}
                logger.warning("⚠️  Model loaded without encoders")
                
        except FileNotFoundError:
            logger.error(f"❌ Model file not found at {model_path}")
            raise
        except Exception as e:
            logger.error(f"❌ Error loading model: {str(e)}")
            raise
    
    def is_loaded(self):
        """Check if model is loaded"""
        return self._model is not None
    
    def preprocess(self, data):
        """
        Preprocess input data for prediction
        
        Args:
            data (dict): Raw input data
            
        Returns:
            pd.DataFrame: Preprocessed data
        """
        try:
            # Feature order
            feature_names = [
                'original_price_pkr',
                'condition',
                'dress_age_months',
                'fabric',
                'is_fully_embroidered',
                'work_intensity',
                'trail_length_ft',
                'is_handwork'
            ]
            
            processed = {}
            
            # Numeric features
            processed['original_price_pkr'] = float(data['original_price_pkr'])
            processed['dress_age_months'] = int(data['dress_age_months'])
            processed['trail_length_ft'] = float(data['trail_length_ft'])
            
            # Boolean features
            processed['is_fully_embroidered'] = int(data['is_fully_embroidered'])
            processed['is_handwork'] = int(data['is_handwork'])
            
            # Categorical features - encode
            categorical_features = ['condition', 'fabric', 'work_intensity']
            
            for feature in categorical_features:
                value = str(data[feature])
                
                if feature in self._encoders:
                    encoder = self._encoders[feature]
                    if value in encoder.classes_:
                        processed[feature] = encoder.transform([value])[0]
                    else:
                        # Use first class as default
                        logger.warning(f"Unknown value '{value}' for {feature}")
                        processed[feature] = 0
                else:
                    # No encoder available, use simple encoding
                    processed[feature] = 0
            
            # Create DataFrame
            df = pd.DataFrame([processed], columns=feature_names)
            
            return df
            
        except Exception as e:
            logger.error(f"Preprocessing error: {str(e)}")
            raise
    
    def predict(self, data):
        """
        Make prediction
        
        Args:
            data (dict): Input features
            
        Returns:
            float: Predicted rental price
        """
        if not self.is_loaded():
            raise Exception("Model not loaded")
        
        try:
            # Preprocess
            df = self.preprocess(data)
            
            # Predict
            prediction = self._model.predict(df)[0]
            
            # Ensure reasonable range
            prediction = max(1000, min(prediction, 50000))
            
            logger.info(f"Prediction: {prediction:.2f} PKR")
            
            return float(prediction)
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise
    
    def get_model_info(self):
        """Get model information"""
        if not self.is_loaded():
            return {"status": "not_loaded"}
        
        info = {
            "status": "loaded",
            "model_type": type(self._model).__name__,
            "has_encoders": len(self._encoders) > 0,
            "encoder_features": list(self._encoders.keys())
        }
        
        # Feature importances if available
        if hasattr(self._model, 'feature_importances_'):
            feature_names = [
                'original_price_pkr', 'condition', 'dress_age_months',
                'fabric', 'is_fully_embroidered', 'work_intensity',
                'trail_length_ft', 'is_handwork'
            ]
            info['feature_importances'] = dict(zip(
                feature_names,
                self._model.feature_importances_.tolist()
            ))
        
        return info


class RecommendationService:
    """
    Service for generating recommendations
    """
    
    @staticmethod
    def generate(data, predicted_price):
        """
        Generate personalized recommendations
        
        Args:
            data (dict): Input features
            predicted_price (float): Predicted price
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        # Price-based
        original_price = data.get('original_price_pkr', 0)
        if original_price > 0:
            rental_ratio = (predicted_price / original_price) * 100
            if rental_ratio < 15:
                recommendations.append({
                    "type": "pricing",
                    "message": f"Rental price is {rental_ratio:.1f}% of original - great value!",
                    "icon": "💰"
                })
            elif rental_ratio > 30:
                recommendations.append({
                    "type": "pricing",
                    "message": "Consider competitive pricing to attract renters",
                    "icon": "📊"
                })
        
        # Condition-based
        condition = data.get('condition', '')
        if condition in ['Poor', 'Fair']:
            recommendations.append({
                "type": "maintenance",
                "message": "Professional cleaning can increase rental value significantly",
                "icon": "✨"
            })
        elif condition in ['Brand New', 'Excellent']:
            recommendations.append({
                "type": "marketing",
                "message": "Pristine condition! Highlight this in photos for premium pricing",
                "icon": "⭐"
            })
        
        # Age-based
        age_months = data.get('dress_age_months', 0)
        if age_months > 24:
            recommendations.append({
                "type": "marketing",
                "message": "Emphasize timeless design and designer labels",
                "icon": "🎨"
            })
        elif age_months < 6:
            recommendations.append({
                "type": "marketing",
                "message": "New dress! Highlight this for better bookings",
                "icon": "🆕"
            })
        
        # Fabric-based
        fabric = data.get('fabric', '')
        premium_fabrics = ['Silk', 'Velvet', 'Raw Silk', 'Brocade']
        if fabric in premium_fabrics:
            recommendations.append({
                "type": "marketing",
                "message": f"Premium {fabric}! Feature close-up shots",
                "icon": "👗"
            })
        
        # Embroidery-based
        if data.get('is_fully_embroidered') or data.get('work_intensity') in ['Heavy', 'Very Heavy']:
            recommendations.append({
                "type": "marketing",
                "message": "Heavy embroidery is valuable - show detailed photos!",
                "icon": "🌟"
            })
        
        if data.get('is_handwork'):
            recommendations.append({
                "type": "marketing",
                "message": "Handwork is rare! Make this a key feature",
                "icon": "🖐️"
            })
        
        # General recommendations
        recommendations.append({
            "type": "photography",
            "message": "Include 6-8 high-quality photos from multiple angles",
            "icon": "📸"
        })
        
        recommendations.append({
            "type": "details",
            "message": "Provide exact measurements and size information",
            "icon": "📏"
        })
        
        return recommendations


class PricingService:
    """
    Service for pricing guidance
    """
    
    @staticmethod
    def generate_guidance(predicted_price, data):
        """
        Generate pricing guidance
        
        Args:
            predicted_price (float): Predicted price
            data (dict): Input features
            
        Returns:
            dict: Pricing guidance
        """
        # Base ranges
        min_price = predicted_price * 0.85
        recommended_price = predicted_price
        max_price = predicted_price * 1.15
        
        # Adjust based on condition
        condition = data.get('condition', 'Good')
        if condition in ['Brand New', 'Excellent']:
            max_price = predicted_price * 1.25
        elif condition in ['Poor', 'Fair']:
            min_price = predicted_price * 0.75
        
        return {
            "minimum_price": round(min_price, 2),
            "recommended_price": round(recommended_price, 2),
            "maximum_price": round(max_price, 2),
            "suggested_discount": round((1 - min_price / predicted_price) * 100, 1),
            "premium_potential": round((max_price / predicted_price - 1) * 100, 1)
        }
    
    @staticmethod
    def calculate_confidence(data):
        """
        Calculate prediction confidence
        
        Args:
            data (dict): Input features
            
        Returns:
            str: Confidence level
        """
        confidence_score = 100
        
        # Reduce for extreme values
        original_price = data.get('original_price_pkr', 0)
        if original_price < 5000 or original_price > 200000:
            confidence_score -= 10
        
        age_months = data.get('dress_age_months', 0)
        if age_months > 60:
            confidence_score -= 5
        
        condition = data.get('condition', 'Good')
        if condition == 'Poor':
            confidence_score -= 10
        
        # Map to level
        if confidence_score >= 90:
            return "Very High"
        elif confidence_score >= 75:
            return "High"
        elif confidence_score >= 60:
            return "Medium"
        else:
            return "Low"
