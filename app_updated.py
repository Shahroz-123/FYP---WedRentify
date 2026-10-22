#!/usr/bin/env python3
"""
Flask API for Pakistani Wedding Dress Rental Price Prediction
Updated for 8 key features
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from model_loader import ModelLoader
from preprocess_updated import DressPreprocessor
from utils.validators import InputValidator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize components
model_loader = ModelLoader()
preprocessor = DressPreprocessor()
validator = InputValidator()

# Load model on startup
try:
    model_loader.load_model()
    logger.info("✅ Model loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load model: {str(e)}")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        model_status = "loaded" if model_loader.model is not None else "not loaded"

        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "model_status": model_status,
            "version": "2.0.0",
            "features": "8-feature model"
        }), 200
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


@app.route('/api/features', methods=['GET'])
def get_features():
    """
    Get information about expected features
    """
    try:
        feature_info = preprocessor.get_feature_info()
        validation_schema = validator.get_validation_schema()

        return jsonify({
            "success": True,
            "feature_info": feature_info,
            "validation_schema": validation_schema
        }), 200

    except Exception as e:
        logger.error(f"❌ Error getting features: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint

    Expected JSON:
    {
        "original_price_pkr": number,
        "condition": string,
        "dress_age_months": integer,
        "fabric": string,
        "is_fully_embroidered": boolean,
        "work_intensity": string,
        "trail_length_ft": number,
        "is_handwork": boolean
    }
    """
    try:
        # Get JSON data
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400

        logger.info(f"📥 Received prediction request: {data}")

        # Validate input
        is_valid, validation_errors = validator.validate_dress_input(data)
        if not is_valid:
            return jsonify({
                "success": False,
                "errors": validation_errors
            }), 400

        # Check if model is loaded
        if model_loader.model is None:
            return jsonify({
                "success": False,
                "error": "Model not loaded. Please contact support."
            }), 500

        # Preprocess input
        processed_data = preprocessor.preprocess(data)

        # Make prediction
        prediction = model_loader.predict(processed_data)

        # Generate pricing guidance
        pricing = generate_pricing_guidance(prediction, data)

        # Generate recommendations
        recommendations = generate_recommendations(data, prediction)

        # Prepare response
        response = {
            "success": True,
            "prediction": {
                "rental_price_pkr": round(prediction, 2),
                "currency": "PKR",
                "confidence": calculate_confidence(data)
            },
            "pricing_guidance": pricing,
            "recommendations": recommendations,
            "input_summary": create_input_summary(data),
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"✅ Prediction: {prediction:.2f} PKR")

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"❌ Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": "An error occurred during prediction. Please try again.",
            "details": str(e) if app.debug else None
        }), 500


def generate_pricing_guidance(predicted_price, data):
    """
    Generate pricing guidance based on prediction
    """
    # Calculate price ranges
    min_price = round(predicted_price * 0.85, 2)
    recommended_price = round(predicted_price, 2)
    max_price = round(predicted_price * 1.15, 2)

    # Adjust based on condition
    condition = data.get('condition', 'Good')
    if condition in ['Brand New', 'Excellent']:
        max_price = round(predicted_price * 1.25, 2)
    elif condition in ['Poor', 'Fair']:
        min_price = round(predicted_price * 0.75, 2)

    return {
        "minimum_price": min_price,
        "recommended_price": recommended_price,
        "maximum_price": max_price,
        "suggested_discount": round((1 - min_price / predicted_price) * 100, 1),
        "premium_potential": round((max_price / predicted_price - 1) * 100, 1)
    }


def generate_recommendations(data, predicted_price):
    """
    Generate personalized recommendations
    """
    recommendations = []

    # Price-based recommendations
    original_price = data.get('original_price_pkr', 0)
    if original_price > 0:
        rental_ratio = (predicted_price / original_price) * 100
        if rental_ratio < 15:
            recommendations.append({
                "type": "pricing",
                "message": f"Rental price is {rental_ratio:.1f}% of original price - great value for renters!",
                "icon": "💰"
            })
        elif rental_ratio > 30:
            recommendations.append({
                "type": "pricing",
                "message": "Consider competitive pricing to attract more renters",
                "icon": "📊"
            })

    # Condition recommendations
    condition = data.get('condition', 'Good')
    if condition in ['Poor', 'Fair']:
        recommendations.append({
            "type": "maintenance",
            "message": "Professional cleaning and minor repairs can significantly increase rental value",
            "icon": "✨"
        })
    elif condition in ['Brand New', 'Excellent']:
        recommendations.append({
            "type": "marketing",
            "message": "Highlight pristine condition in photos - this commands premium pricing!",
            "icon": "⭐"
        })

    # Age recommendations
    age_months = data.get('dress_age_months', 0)
    if age_months > 24:
        recommendations.append({
            "type": "marketing",
            "message": "Emphasize timeless design and any designer labels to overcome age concerns",
            "icon": "🎨"
        })
    elif age_months < 6:
        recommendations.append({
            "type": "marketing",
            "message": "New dress advantage! Highlight this in your listing for better bookings",
            "icon": "🆕"
        })

    # Fabric recommendations
    fabric = data.get('fabric', '')
    premium_fabrics = ['Silk', 'Velvet', 'Raw Silk', 'Brocade']
    if fabric in premium_fabrics:
        recommendations.append({
            "type": "marketing",
            "message": f"Premium {fabric} fabric! Feature close-up photos to showcase quality",
            "icon": "👗"
        })

    # Embroidery recommendations
    is_fully_embroidered = data.get('is_fully_embroidered', False)
    is_handwork = data.get('is_handwork', False)
    work_intensity = data.get('work_intensity', 'Moderate')

    if is_fully_embroidered or work_intensity in ['Heavy', 'Very Heavy']:
        recommendations.append({
            "type": "marketing",
            "message": "Heavy embroidery is a major selling point - take detailed close-up shots!",
            "icon": "🌟"
        })

    if is_handwork:
        recommendations.append({
            "type": "marketing",
            "message": "Handwork is rare and valuable - make this a key feature in your description",
            "icon": "🖐️"
        })

    # Trail length recommendations
    trail_length = data.get('trail_length_ft', 0)
    if trail_length > 3:
        recommendations.append({
            "type": "info",
            "message": "Long trail is perfect for formal events - mention venue suitability",
            "icon": "👰"
        })

    # General recommendations
    recommendations.append({
        "type": "photography",
        "message": "Include 6-8 high-quality photos from multiple angles with good lighting",
        "icon": "📸"
    })

    recommendations.append({
        "type": "details",
        "message": "Provide exact measurements, size details, and any alterations made",
        "icon": "📏"
    })

    # Seasonal timing
    recommendations.append({
        "type": "timing",
        "message": "List 2-3 months before peak wedding season (October-December) for best results",
        "icon": "📅"
    })

    return recommendations


def calculate_confidence(data):
    """
    Calculate prediction confidence based on input quality
    """
    confidence_score = 100

    # Reduce confidence for extreme values
    original_price = data.get('original_price_pkr', 0)
    if original_price < 5000 or original_price > 200000:
        confidence_score -= 10

    age_months = data.get('dress_age_months', 0)
    if age_months > 60:
        confidence_score -= 5

    condition = data.get('condition', 'Good')
    if condition == 'Poor':
        confidence_score -= 10

    # Map to confidence level
    if confidence_score >= 90:
        return "Very High"
    elif confidence_score >= 75:
        return "High"
    elif confidence_score >= 60:
        return "Medium"
    else:
        return "Low"


def create_input_summary(data):
    """
    Create a readable summary of input data
    """
    return {
        "original_price": f"PKR {data.get('original_price_pkr', 0):,.0f}",
        "condition": data.get('condition', 'N/A'),
        "age": f"{data.get('dress_age_months', 0)} months",
        "fabric": data.get('fabric', 'N/A'),
        "fully_embroidered": "Yes" if data.get('is_fully_embroidered', False) else "No",
        "work_intensity": data.get('work_intensity', 'N/A'),
        "trail_length": f"{data.get('trail_length_ft', 0)} ft",
        "handwork": "Yes" if data.get('is_handwork', False) else "No"
    }


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"❌ Internal server error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'

    print("\n" + "="*60)
    print("🚀 DRESS RENTAL PRICE PREDICTION API")
    print("="*60)
    print(f"🌐 Running on: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📊 Features: 8-feature model")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=port, debug=debug)
