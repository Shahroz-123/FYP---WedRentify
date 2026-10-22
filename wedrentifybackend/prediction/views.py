# prediction/views.py
# API Views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import connection
import time
import logging

from .serializers import (
    PredictionRequestSerializer,
    PredictionResponseSerializer,
    HealthCheckSerializer,
    FeaturesInfoSerializer
)
from .services import ModelService, RecommendationService, PricingService
from .models import Prediction, APILog

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class HealthCheckView(APIView):
    """
    GET /api/health/
    Check API and model status
    """

    def get(self, request):
        """Health check endpoint"""
        start_time = time.time()

        try:
            # Check model
            model_service = ModelService()
            model_status = "loaded" if model_service.is_loaded() else "not loaded"

            # Check database
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_status = "connected"
        except Exception as e:
            db_status = "error"
            logger.error(f"Database check failed: {str(e)}")

        response_data = {
            "status": "healthy",
            "timestamp": timezone.now(),
            "model_status": model_status,
            "version": "2.0.0",
            "database": db_status
        }

        # Log API call
        response_time = (time.time() - start_time) * 1000
        APILog.objects.create(
            endpoint='/api/health/',
            method='GET',
            status_code=200,
            response_time=response_time,
            ip_address=get_client_ip(request)
        )

        serializer = HealthCheckSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeaturesInfoView(APIView):
    """
    GET /api/features/
    Get feature information and validation rules
    """

    def get(self, request):
        """Get features information"""
        start_time = time.time()

        features_info = {
            "original_price_pkr": {
                "type": "numeric",
                "range": [1000, 500000],
                "description": "Original purchase price in PKR",
                "importance": "79.65%"
            },
            "condition": {
                "type": "categorical",
                "values": ["Brand New", "Excellent", "Fair", "Good", "Worn Once"],
                "description": "Current condition of the dress",
                "importance": "9.39%"
            },
            "dress_age_months": {
                "type": "numeric",
                "range": [0, 120],
                "description": "Age of dress in months",
                "importance": "2.89%"
            },
            "fabric": {
                "type": "categorical",
                "values": [
                    "Banarsi", "Brocade", "Chiffon", "Cotton Silk", "Jamawar",
                    "Karandi", "Khaddar", "Korean Raw Silk", "Organza",
                    "Pure Chiffon", "Raw Silk", "Silk", "Velvet", "Georgette", "Net"
                ],
                "description": "Primary fabric material",
                "importance": "1.27%"
            },
            "is_fully_embroidered": {
                "type": "boolean",
                "values": [True, False],
                "description": "Whether dress is fully embroidered",
                "importance": "2.21%"
            },
            "work_intensity": {
                "type": "categorical",
                "values": ["Heavy", "Light", "Medium"],
                "description": "Intensity of embroidery work",
                "importance": "2.21%"
            },
            "trail_length_ft": {
                "type": "numeric",
                "range": [0, 10],
                "description": "Trail/train length in feet",
                "importance": "1.11%"
            },
            "is_handwork": {
                "type": "boolean",
                "values": [True, False],
                "description": "Whether dress has hand embroidery",
                "importance": "1.27%"
            }
        }

        validation_rules = {
            "required_fields": [
                "original_price_pkr", "condition", "dress_age_months",
                "fabric", "is_fully_embroidered", "work_intensity",
                "trail_length_ft", "is_handwork"
            ],
            "total_features": 8
        }

        response_data = {
            "success": True,
            "features": features_info,
            "validation_rules": validation_rules
        }

        # Log API call
        response_time = (time.time() - start_time) * 1000
        APILog.objects.create(
            endpoint='/api/features/',
            method='GET',
            status_code=200,
            response_time=response_time,
            ip_address=get_client_ip(request)
        )

        serializer = FeaturesInfoSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PredictView(APIView):
    """
    POST /api/predict/
    Make rental price prediction
    """

    def post(self, request):
        """Make prediction"""
        start_time = time.time()

        try:
            # Validate input
            serializer = PredictionRequestSerializer(data=request.data)
            if not serializer.is_valid():
                response_time = (time.time() - start_time) * 1000
                APILog.objects.create(
                    endpoint='/api/predict/',
                    method='POST',
                    status_code=400,
                    response_time=response_time,
                    ip_address=get_client_ip(request)
                )
                return Response({
                    "success": False,
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data

            # Get services
            model_service = ModelService()

            if not model_service.is_loaded():
                return Response({
                    "success": False,
                    "error": "Model not loaded. Please contact support."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Make prediction
            predicted_price = model_service.predict(data)

            # Generate pricing guidance
            pricing_guidance = PricingService.generate_guidance(predicted_price, data)

            # Generate recommendations
            recommendations = RecommendationService.generate(data, predicted_price)

            # Calculate confidence
            confidence = PricingService.calculate_confidence(data)

            # Create input summary
            input_summary = {
                "original_price": f"PKR {data['original_price_pkr']:,.0f}",
                "condition": data['condition'],
                "age": f"{data['dress_age_months']} months",
                "fabric": data['fabric'],
                "fully_embroidered": "Yes" if data['is_fully_embroidered'] else "No",
                "work_intensity": data['work_intensity'],
                "trail_length": f"{data['trail_length_ft']} ft",
                "handwork": "Yes" if data['is_handwork'] else "No"
            }

            # Save prediction to database
            try:
                Prediction.objects.create(
                    original_price_pkr=data['original_price_pkr'],
                    condition=data['condition'],
                    dress_age_months=data['dress_age_months'],
                    fabric=data['fabric'],
                    is_fully_embroidered=data['is_fully_embroidered'],
                    work_intensity=data['work_intensity'],
                    trail_length_ft=data['trail_length_ft'],
                    is_handwork=data['is_handwork'],
                    predicted_rental_price=predicted_price,
                    confidence=confidence,
                    ip_address=get_client_ip(request)
                )
            except Exception as e:
                logger.error(f"Failed to save prediction: {str(e)}")

            # Prepare response
            response_data = {
                "success": True,
                "prediction": {
                    "rental_price_pkr": round(predicted_price, 2),
                    "currency": "PKR",
                    "confidence": confidence
                },
                "pricing_guidance": pricing_guidance,
                "recommendations": recommendations,
                "input_summary": input_summary,
                "timestamp": timezone.now()
            }

            # Log API call
            response_time = (time.time() - start_time) * 1000
            APILog.objects.create(
                endpoint='/api/predict/',
                method='POST',
                status_code=200,
                response_time=response_time,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            logger.info(f"✅ Prediction: {predicted_price:.2f} PKR")

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"❌ Prediction error: {str(e)}")

            response_time = (time.time() - start_time) * 1000
            APILog.objects.create(
                endpoint='/api/predict/',
                method='POST',
                status_code=500,
                response_time=response_time,
                ip_address=get_client_ip(request)
            )

            return Response({
                "success": False,
                "error": "An error occurred during prediction. Please try again."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PredictionHistoryView(APIView):
    """
    GET /api/predictions/
    Get prediction history
    """

    def get(self, request):
        """Get recent predictions"""
        try:
            limit = int(request.query_params.get('limit', 10))
            limit = min(limit, 100)  # Max 100

            predictions = Prediction.objects.all()[:limit]

            data = [{
                "id": pred.id,
                "predicted_price": float(pred.predicted_rental_price),
                "confidence": pred.confidence,
                "condition": pred.condition,
                "fabric": pred.fabric,
                "created_at": pred.created_at
            } for pred in predictions]

            return Response({
                "success": True,
                "count": len(data),
                "predictions": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching predictions: {str(e)}")
            return Response({
                "success": False,
                "error": "Failed to fetch predictions"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModelInfoView(APIView):
    """
    GET /api/model-info/
    Get model information
    """

    def get(self, request):
        """Get model info"""
        try:
            model_service = ModelService()
            model_info = model_service.get_model_info()

            return Response({
                "success": True,
                "model_info": model_info
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            return Response({
                "success": False,
                "error": "Failed to get model information"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
