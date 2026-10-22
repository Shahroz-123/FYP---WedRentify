import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET

# --- YEH HAIN AAPKE MODELS ---
# (Aapke models.py ke mutabiq AuctionDress aur Bid, dono ko import karein)
from .models import AuctionDress, DressChoices, Bid


# ==========================================================
# View 1: Add Dress (Aapka Original Code - Bilkul Sahi)
# ==========================================================
@csrf_exempt
def add_dress_view(request):
    """
    Handles the POST request from the frontend to save a new dress listing.
    Manually validates data received as multipart/form-data.
    """
    if request.method == 'POST':

        # 1. Retrieve Data from request.POST (form fields) and request.FILES (file upload)
        data = request.POST

        seller_username = data.get('seller_username')
        dress_image = request.FILES.get('dress_image')

        # Manually extract fields for validation/conversion
        original_price_pkr = data.get('original_price_pkr')
        dress_age_months = data.get('dress_age_months')
        trail_length_ft = data.get('trail_length_ft')

        # Convert string values from the frontend for boolean fields
        is_fully_embroidered = data.get('is_fully_embroidered') == 'True'
        is_handwork = data.get('is_handwork') == 'True'

        errors = {}

        # 2. Manual Validation
        if not seller_username:
            errors['seller_username'] = 'Seller username is required.'

        if not dress_image:
            errors['dress_image'] = 'Dress image upload is required.'

        # Validation for numeric fields
        try:
            original_price_pkr = int(original_price_pkr)
            if original_price_pkr <= 1000:
                errors['original_price_pkr'] = 'Original price must be greater than PKR 1000.'
        except (TypeError, ValueError):
            errors['original_price_pkr'] = 'Original price is invalid or missing.'

        try:
            dress_age_months = int(dress_age_months)
        except (TypeError, ValueError):
            errors['dress_age_months'] = 'Dress age is invalid or missing.'

        try:
            trail_length_ft = float(trail_length_ft)
        except (TypeError, ValueError):
            errors['trail_length_ft'] = 'Trail length is invalid or missing.'

        # Check if any validation errors occurred
        if errors:
            # 3. Return errors if validation fails
            return JsonResponse({
                "success": False,
                "error": "Data validation failed.",
                "errors": errors
            }, status=400)  # Bad Request

        # 4. Save the model instance to the database
        try:
            dress = AuctionDress.objects.create(
                seller_username=seller_username,
                dress_color=data.get('dress_color', ''),
                dress_image=dress_image,
                seller_contact=data.get('seller_contact', ''),
                original_price_pkr=original_price_pkr,
                condition=data.get('condition', ''),
                dress_age_months=dress_age_months,
                fabric=data.get('fabric', ''),
                work_intensity=data.get('work_intensity', ''),
                trail_length_ft=trail_length_ft,
                is_fully_embroidered=is_fully_embroidered,
                is_handwork=is_handwork,
            )

            # 5. Return success response
            return JsonResponse({
                "success": True,
                "message": "Dress successfully added to the auction list!",
                "dress_id": dress.id,
                "image_url": request.build_absolute_uri(dress.dress_image.url) if dress.dress_image else None,
            }, status=201)  # Created

        except Exception as e:
            # Catch database or unexpected server errors
            print(f"Database Save Error: {e}")
            return JsonResponse({
                "success": False,
                "error": "A server error occurred while saving to the database."
            }, status=500)

    # Only allow POST requests
    return JsonResponse({
        "success": False,
        "error": "Only POST method is allowed for this endpoint."
    }, status=405)  # Method Not Allowed


# ==========================================================
# View 2: List Items (Aapka Original Code - Thora Fix Kiya Hai)
# ==========================================================
@require_GET
def list_auction_items(request):
    """
    Fetches active, paginated auction items AND
    DELETES any expired items before sending the list.
    """
    try:
        now = timezone.now()

        # Aapke code ke mutabiq auction 1 ghante ki hai
        # (Aapke variable ka naam 'four_hours_ago' tha, lekin logic 1 ghante ka tha)
        one_hour_ago = now - timedelta(hours=4)

        # --- Delete Logic ---
        try:
            # 1 ghante se purane items delete karein
            expired_items = AuctionDress.objects.filter(date_added__lt=one_hour_ago)
            count = expired_items.count()
            if count > 0:
                expired_items.delete()
                print(f"Successfully deleted {count} expired auction items.")
        except Exception as e:
            print(f"Error during scheduled deletion: {e}")
        # --- End of Delete Logic ---

        # 2. Filter karein baaqi active auctions (jo 1 ghante ke andar add hue)
        active_auctions_list = AuctionDress.objects.filter(
            date_added__gte=one_hour_ago
        ).order_by('-date_added')

        # 3. Pagination parameters
        page_number = request.GET.get('page', 1)
        limit = request.GET.get('limit', 12)

        # 4. Paginate
        paginator = Paginator(active_auctions_list, limit)
        try:
            page_items = paginator.page(page_number)
        except PageNotAnInteger:
            page_items = paginator.page(1)
        except EmptyPage:
            page_items = paginator.page(paginator.num_pages)

        # 5. Data ko JSON ke liye Format karein
        auctions_json = []
        for dress in page_items:
            # Expiry time = 1 ghanta (jaisa aapke logic mein tha)
            expiration_time = dress.date_added + timedelta(hours=4)

            # === YAHAN HUM 'BID' TABLE SE DATA UTHA RAHE HAIN ===
            try:
                bid_info = Bid.objects.get(auction_item=dress)
                current_bid = bid_info.highest_bid
                highest_bidder = bid_info.buyer_username
                highest_bidder_contact = bid_info.buyer_contact

            except Bid.DoesNotExist:
                current_bid = 0
                highest_bidder = "No Bids Yet"
                highest_bidder_contact = None
            # === END OF BID LOGIC ===

            image_url = None
            if dress.dress_image and hasattr(dress.dress_image, 'url'):
                image_url = request.build_absolute_uri(dress.dress_image.url)

            auctions_json.append({
                'id': dress.id,
                'dress_name': f"{dress.condition} {dress.dress_color} {dress.fabric} Dress",
                'dress_image_url': image_url,
                'orginalprice': dress.original_price_pkr,  # Yeh 'AuctionDress' se aa raha hai
                'deletion_time': expiration_time.isoformat(),
                'seller_username': dress.seller_username,  # Yeh 'AuctionDress' se aa raha hai
                'seller_contact': dress.seller_contact,  # Yeh 'AuctionDress' se aa raha hai
                'dress_condition': dress.condition,
                'dress_fabric': dress.fabric,
                'dress_color': dress.dress_color,

                # === YEH DATA 'BID' TABLE SE AA RAHA HAI ===
                'current_bid': current_bid,
                'highest_bidder': highest_bidder,
                'highest_bidder_contact': highest_bidder_contact,
            })

        # 6. Paginated data wapis bhej dein
        return JsonResponse({
            'success': True,
            'current_page': page_items.number,
            'page_count': paginator.num_pages,
            'auctions': auctions_json
        }, status=200)

    except Exception as e:
        print(f"Error in list_auction_items: {e}")
        return JsonResponse({
            "success": False,
            "error": "A server error occurred."
        }, status=500)


# ==========================================================
# View 3: Place Bid (YEH HAI AAPKA FIXED FUNCTION)
# ==========================================================
@csrf_exempt
def place_bid_view(request):
    if request.method == "POST":
        try:
            # Frontend se JSON data read karein
            data = json.loads(request.body)

            dress_id = data.get('dress_id')
            buyer_username = data.get('buyer_username')
            contact_number = data.get('contact_number')
            bid_price = int(data.get('bid_price'))

            # 1. FIX: AuctionItem ki jagah AuctionDress dhoondein
            try:
                item = AuctionDress.objects.get(id=dress_id)
            except AuctionDress.DoesNotExist:
                return JsonResponse({"error": "Auction item not found."}, status=404)

            # 2. FIX: Expiry logic ko 'list_auction_items' se match karein (1 ghanta)
            expiration_time = item.date_added + timedelta(hours=1)

            if timezone.now() >= expiration_time:
                # Item delete ho chuka hoga, lekin phir bhi check kar rahe hain
                return JsonResponse({"error": "Auction has already expired."}, status=400)

            # 3. Bid table se row dhoondein, ya agar nahi hai toh banayein
            # (Yeh 100% aapka logic hai)
            bid_obj, created = Bid.objects.get_or_create(
                auction_item=item,  # Yeh AuctionDress object hai
                # 'defaults' tab istemal hota hai jab row pehli baar 'create' ho
                defaults={
                    'seller_username': item.seller_username,
                    'seller_contact': item.seller_contact,
                    'highest_bid': 0  # Shuru mein 0
                }
            )

            # 4. Check karein ke nayi bid purani (highest_bid) se zyada hai
            if bid_price > bid_obj.highest_bid:

                # Agar zyada hai, toh "Bid" row ko UPDATE karein
                bid_obj.highest_bid = bid_price
                bid_obj.buyer_username = buyer_username
                bid_obj.buyer_contact = contact_number

                bid_obj.save()  # Bid table mein row update ho gayi!

                return JsonResponse({
                    "success": True,
                    "message": "Bid placed successfully!",
                })
            else:
                # Agar bid kam hai
                return JsonResponse({"error": f"Your bid must be higher than Rs {bid_obj.highest_bid}."},
                                    status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)