# prediction/urls.py
# URL routing for prediction app

from django.urls import path
from .views import (
    HealthCheckView,
    FeaturesInfoView,
    PredictView,
    PredictionHistoryView,
    ModelInfoView
)

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('features/', FeaturesInfoView.as_view(), name='features-info'),
    path('predict/', PredictView.as_view(), name='predict'),
    path('predictions/', PredictionHistoryView.as_view(), name='prediction-history'),
    path('model-info/', ModelInfoView.as_view(), name='model-info'),
]
