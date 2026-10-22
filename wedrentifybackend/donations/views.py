from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Donation

@csrf_exempt
def add_donation(request):
    if request.method == "POST":
        donor_name = request.POST.get("donor_name")
        donor_contact = request.POST.get("donor_contact")
        dress_title = request.POST.get("dress_title")
        dress_description = request.POST.get("dress_description")
        dress_size = request.POST.get("dress_size")
        buyer_username = request.POST.get("buyer_username")
        dress_image = request.FILES.get("dress_image")

        if not all([donor_name, donor_contact, dress_title, buyer_username]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        donation = Donation.objects.create(
            donor_name=donor_name,
            donor_contact=donor_contact,
            dress_title=dress_title,
            dress_description=dress_description,
            dress_size=dress_size,
            buyer_username=buyer_username,
            dress_image=dress_image
        )

        return JsonResponse({"message": "🎉 Donation added successfully!", "id": donation.id}, status=201)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def list_donations(request):
    donations = Donation.objects.all().order_by("-created_at")
    data = []
    for d in donations:
        data.append({
            "id": d.id,
            "donor_name": d.donor_name,
            "donor_contact": d.donor_contact,
            "dress_title": d.dress_title,
            "dress_description": d.dress_description,
            "dress_size": d.dress_size,
            "buyer_username": d.buyer_username,
            "dress_image": request.build_absolute_uri(d.dress_image.url) if d.dress_image else None,
            "created_at": d.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return JsonResponse(data, safe=False)
@csrf_exempt
def delete_donation(request, id):
    if request.method == "DELETE":
        try:
            donation = Donation.objects.get(id=id)
            donation.delete()
            return JsonResponse({"message": "Donation deleted successfully!"})
        except Donation.DoesNotExist:
            return JsonResponse({"error": "Donation not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)