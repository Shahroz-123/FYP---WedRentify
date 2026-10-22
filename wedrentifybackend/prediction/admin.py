# prediction/admin.py
# Django admin configuration

from django.contrib import admin
from .models import Prediction, APILog


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'predicted_rental_price', 'condition',
        'fabric', 'confidence', 'created_at'
    ]
    list_filter = ['condition', 'fabric', 'confidence', 'created_at']
    search_fields = ['condition', 'fabric']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Input Features', {
            'fields': (
                'original_price_pkr', 'condition', 'dress_age_months',
                'fabric', 'is_fully_embroidered', 'work_intensity',
                'trail_length_ft', 'is_handwork'
            )
        }),
        ('Prediction', {
            'fields': ('predicted_rental_price', 'confidence')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'created_at')
        }),
    )


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'endpoint', 'method', 'status_code',
        'response_time', 'ip_address', 'created_at'
    ]
    list_filter = ['method', 'status_code', 'created_at']
    search_fields = ['endpoint', 'ip_address']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False  # Logs are created automatically
