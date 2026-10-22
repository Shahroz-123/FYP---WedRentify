from django.urls import path
from . import views

urlpatterns = [
    # Maps the endpoint /api/add_dress/ to the add_dress_view function.
    # The 'api/' prefix is handled by the main project's urls.py file.
    path('add_dress/', views.add_dress_view, name='add_dress_api'),
path('auction/list/', views.list_auction_items, name='list_auction_api'),
    # You can add other auction-related URLs here in the future, e.g.:
    # path('dress/<int:pk>/', views.dress_detail_view, name='dress_detail'),
    # API 1: Naya dress add karne ke liye


    # API 3: Nayi bid POST karne ke liye (Aapka frontend yeh use kar raha hai)
    path('bid/', views.place_bid_view, name='place_bid'),
]
