# prediction/models.py
# Database models for storing predictions

from django.db import models
from django.utils import timezone

class Prediction(models.Model):
    """
    Store prediction history
    """
    # Input features
    original_price_pkr = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50)
    dress_age_months = models.IntegerField()
    fabric = models.CharField(max_length=50)
    is_fully_embroidered = models.BooleanField()
    work_intensity = models.CharField(max_length=50)
    trail_length_ft = models.DecimalField(max_digits=5, decimal_places=2)
    is_handwork = models.BooleanField()

    # Output
    predicted_rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    confidence = models.CharField(max_length=20)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Prediction {self.id} - PKR {self.predicted_rental_price}"


class APILog(models.Model):
    """
    Store API access logs
    """
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    response_time = models.FloatField(help_text="Response time in milliseconds")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code}"


from django.db import models

# Create your models here.
