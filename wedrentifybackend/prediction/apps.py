# prediction/apps.py
from django.apps import AppConfig


class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    verbose_name = 'Dress Rental Price Prediction'
