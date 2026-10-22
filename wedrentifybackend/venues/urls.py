from django.urls import path
from . import views

urlpatterns = [
    # --- UPDATED ---
    # Humara main `wedrentify/urls.py` isko '/api/venue/' par bhej raha hai.
    # Yeh single URL ab dono kaam karega:
    # 1. GET Request (isi URL par): Venues fetch karega.
    # 2. POST Request (isi URL par): Scraper run karega.

    path('', views.venue_api_view, name='venue_api'),
]

