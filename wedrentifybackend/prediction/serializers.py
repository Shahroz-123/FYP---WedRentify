# prediction/serializers.py
# Serializers for request/response validation

from rest_framework import serializers
from .models import Prediction


class PredictionRequestSerializer(serializers.Serializer):
    """
    Validates prediction request data
    """
    original_price_pkr = serializers.FloatField(
        min_value=1000,
        max_value=500000,
        required=True,
        help_text="Original purchase price in PKR (1,000 - 500,000)"
    )
    
    condition = serializers.ChoiceField(
        choices=['Brand New', 'Excellent', 'Fair', 'Good', 'Worn Once'],
        required=True,
        help_text="Current condition of the dress"
    )
    
    dress_age_months = serializers.IntegerField(
        min_value=0,
        max_value=120,
        required=True,
        help_text="Age of dress in months (0-120)"
    )
    
    fabric = serializers.ChoiceField(
        choices=[
            'Banarsi', 'Brocade', 'Chiffon', 'Cotton Silk', 'Jamawar',
            'Karandi', 'Khaddar', 'Korean Raw Silk', 'Organza', 'Pure Chiffon',
            'Raw Silk', 'Silk', 'Velvet', 'Georgette', 'Net'
        ],
        required=True,
        help_text="Primary fabric material"
    )
    
    is_fully_embroidered = serializers.BooleanField(
        required=True,
        help_text="Whether dress is fully embroidered"
    )
    
    work_intensity = serializers.ChoiceField(
        choices=['Heavy', 'Light', 'Medium'],
        required=True,
        help_text="Intensity of embroidery work"
    )
    
    trail_length_ft = serializers.FloatField(
        min_value=0,
        max_value=10,
        required=True,
        help_text="Trail/train length in feet (0-10)"
    )
    
    is_handwork = serializers.BooleanField(
        required=True,
        help_text="Whether dress has hand embroidery"
    )


class PredictionResponseSerializer(serializers.Serializer):
    """
    Formats prediction response
    """
    success = serializers.BooleanField()
    prediction = serializers.DictField()
    pricing_guidance = serializers.DictField()
    recommendations = serializers.ListField()
    input_summary = serializers.DictField()
    timestamp = serializers.DateTimeField()


class PredictionModelSerializer(serializers.ModelSerializer):
    """
    Serializer for Prediction model
    """
    class Meta:
        model = Prediction
        fields = '__all__'
        read_only_fields = ['created_at']


class HealthCheckSerializer(serializers.Serializer):
    """
    Health check response
    """
    status = serializers.CharField()
    timestamp = serializers.DateTimeField()
    model_status = serializers.CharField()
    version = serializers.CharField()
    database = serializers.CharField()


class FeaturesInfoSerializer(serializers.Serializer):
    """
    Features information response
    """
    success = serializers.BooleanField()
    features = serializers.DictField()
    validation_rules = serializers.DictField()
