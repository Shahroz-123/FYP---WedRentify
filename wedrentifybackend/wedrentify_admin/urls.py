# wedrentify_admin/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Yeh aapka purana URL hai (Contact Us form ke liye)
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),

    # Frontend ispar GET request bhejega: .../api/admin/disputes/all/
    path('disputes/', views.list_all_complaints, name='list_all_complaints'),

    # 2. Ek complaint ko 'Resolved' mark karne ke liye URL
    # Frontend ispar PUT request bhejega: .../api/admin/disputes/123/resolve/
    path('disputes/<int:complaint_number>/resolve/', views.resolve_complaint, name='resolve_complaint'),

    # 3. Ek complaint ko delete karne ke liye URL
    # Frontend ispar DELETE request bhejega: .../api/admin/disputes/123/delete/
    path('disputes/<int:complaint_number>/delete/', views.delete_complaint, name='delete_complaint'),
    # 1. GET .../api/wedrentify_admin/venues/list/
    path('venues/list/', views.list_venues, name='venue_list'),

    # 2. POST .../api/wedrentify_admin/venues/add/
    path('venues/add/', views.add_venue, name='venue_add'),

    # 3. DELETE .../api/wedrentify_admin/venues/delete/<id>/
    path('venues/delete/<int:venue_id>/', views.delete_venue, name='venue_delete'),
path("drycleaners/", views.manage_dry_cleaners, name="manage_dry_cleaners"), # GET and POST
    path("drycleaners/delete/<int:cleaner_id>/", views.delete_dry_cleaner, name="delete_dry_cleaner"), # DELE
]


