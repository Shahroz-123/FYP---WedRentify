# wedrentify_admin/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Complaint


@csrf_exempt
@require_http_methods(["POST"])
def submit_complaint(request):
    try:
        data = json.loads(request.body)

        # Checkboxes se arrays ko comma-separated string mein badlein
        dispute_types = ", ".join(data.get('dispute', []))
        user_roles = ", ".join(data.get('role', []))

        # Naya Complaint object banayein aur save karein
        new_complaint = Complaint(
            dispute_type=dispute_types,
            user_role=user_roles,
            username=data.get('username'),
            cnic=data.get('cnic'),
            phone_number=data.get('phone'),
            full_name=data.get('name'),
            against_username=data.get('againstUsername'),
            against_contact=data.get('againstContact'),
            details=data.get('details')
        )
        new_complaint.save()

        # Success ka response bhejein
        return JsonResponse({'message': 'Complaint submitted successfully!'}, status=201)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
@require_http_methods(["GET"])
def list_all_complaints(request):
    """
    Database se saari complaints fetch karta hai.
    """
    try:
        # Saari complaints get karein, sab se nayi wali oopar
        all_complaints = Complaint.objects.all().order_by('-created_at')
        # Data ko JSON format mein bhejne ke liye list banayein
        data = list(all_complaints.values())
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def resolve_complaint(request, complaint_number):
    """
    Ek complaint ka status 'Resolved' mark karta hai.
    """
    try:
        complaint = Complaint.objects.get(pk=complaint_number)
        complaint.status = 'Resolved'
        complaint.save()
        return JsonResponse({'message': f'Complaint #{complaint_number} marked as Resolved.'}, status=200)
    except Complaint.DoesNotExist:
        return JsonResponse({'error': 'Complaint not found.'}, status=404)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_complaint(request, complaint_number):
    """
    Ek complaint ko database se delete karta hai.
    """
    try:
        complaint = Complaint.objects.get(pk=complaint_number)
        complaint.delete()
        return JsonResponse({'message': f'Complaint #{complaint_number} has been deleted.'}, status=200)
    except Complaint.DoesNotExist:
        return JsonResponse({'error': 'Complaint not found.'}, status=404)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Venue  # Apne Venue model ko import karein
import json


# ==========================================================
# View 1: List Venues (GET .../api/venues/list/)
# ==========================================================
@require_GET
# ==========================================================
# View 1: List Venues
# ==========================================================
@require_GET
def list_venues(request):
    """
    Saare venues ko fetch karke JSON list ki soorat mein bhejta hai.
    """
    try:
        venues = Venue.objects.all().order_by('-created_at')

        data = []
        for venue in venues:
            image_url = ""
            if venue.venue_image:
                image_url = request.build_absolute_uri(venue.venue_image.url)

            # Data ko frontend ke mutabiq map karein
            data.append({
                "id": venue.id,
                "name": venue.venue_name,
                "city": venue.venue_city,
                "image": image_url,
                "venue_description":venue.venue_description,
                "per_head_price": venue.per_head_price,
                "whatsapp_number": venue.contact_number  # Model se contact_number le rahe hain
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ==========================================================
# View 2: Add Venue
# ==========================================================
@csrf_exempt
@require_POST
def add_venue(request):
    """
    Form se naya venue data (FormData) receive karke database mein save karta hai.
    """
    try:
        data = request.POST
        files = request.FILES

        Venue.objects.create(
            venue_name=data.get('venue_name'),
            venue_city=data.get('venue_city'),
            venue_image=files.get('venue_image'),
            venue_description=data.get('venue_description'),
            per_head_price=data.get('per_head_price'),
            contact_number=data.get('contact_number')
        )

        return JsonResponse({"message": "Venue added successfully!"}, status=201)

    except Exception as e:
        print(f"Error adding venue: {e}")
        return JsonResponse({"error": "Failed to add venue. Check server logs."}, status=500)


# ==========================================================
# View 3: Delete Venue
# ==========================================================
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_venue(request, venue_id):
    """
    Venue ko uski ID ke zariye delete karta hai.
    """
    try:
        venue = Venue.objects.get(id=venue_id)
        venue.delete()
        return JsonResponse({"message": f"Venue ID #{venue_id} deleted successfully."})

    except Venue.DoesNotExist:
        return JsonResponse({"error": "Venue not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# views.py mein yeh code add karein
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import DryCleaner  # Apne model ko import karna mat bhuliyega


# ----------------- 1. ADD / LIST Dry Cleaners -----------------
@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_dry_cleaners(request):
    if request.method == "POST":
        # Data submission via FormData (for image upload)
        try:
            name = request.POST.get("drycleaner-name")
            contact_number = request.POST.get("contact-number")
            image_file = request.FILES.get("drycleaner-image")  # Image file

            if not name or not contact_number or not image_file:
                return JsonResponse({"error": "Name, contact number, and image are required."}, status=400)

            # Save to database
            dry_cleaner = DryCleaner.objects.create(
                name=name,
                contact_number=contact_number,
                image=image_file
            )

            return JsonResponse({
                "message": "Dry Cleaner added successfully!",
                "id": dry_cleaner.id,
                "name": dry_cleaner.name
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":
        # List all dry cleaners
        cleaners = DryCleaner.objects.all().order_by('name')
        data = []
        for c in cleaners:
            data.append({
                "id": c.id,
                "name": c.name,
                "contact_number": c.contact_number,
                # Image URL return karein (agar maujood ho)
                "image_url": request.build_absolute_uri(c.image.url) if c.image else None
            })
        return JsonResponse(data, safe=False)


# ----------------- 2. DELETE Dry Cleaner -----------------
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_dry_cleaner(request, cleaner_id):
    try:
        cleaner = DryCleaner.objects.get(id=cleaner_id)
        cleaner_name = cleaner.name

        # Database se delete karein
        cleaner.delete()

        return JsonResponse({"message": f"Dry Cleaner '{cleaner_name}' deleted successfully."}, status=200)

    except DryCleaner.DoesNotExist:
        return JsonResponse({"error": "Dry Cleaner not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)