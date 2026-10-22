import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Dress, SecurityDeposit
from accounts.models import Seller
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import RentOrder
from django.core.mail import send_mail # 🚨 YEH IMPORT ZAROORI HAI
from django.conf import settings
import json

@csrf_exempt
@csrf_exempt
def add_dress_with_deposit(request):
    if request.method == "POST":
        try:
            seller_username = request.POST.get("seller_username")
            if not seller_username:
                return JsonResponse({"error": "Seller username is required"}, status=400)

            seller = Seller.objects.get(username=seller_username)

            rent_price_raw = request.POST.get("rent_price")
            if not rent_price_raw:
                return JsonResponse({"error": "Rent price is required"}, status=400)

            try:
                rent_price = float(rent_price_raw)
            except ValueError:
                return JsonResponse({"error": "Rent price must be a number"}, status=400)
            ai_condition_value = request.POST.get("ai_condition", "Not Checked")
            # Dress create
            dress = Dress.objects.create(
                seller=seller,
                name=request.POST.get("name", "Untitled"),
                description=request.POST.get("description", ""),
                rent_price=rent_price,
                city=request.POST.get("city", "Unknown"),
                category=request.POST.get("category", "Uncategorized"),
                occasion=request.POST.get("occasion", "General"),
                color=request.POST.get("color", "Not specified"),
                length=request.POST.get("length", "Medium"),
                size=request.POST.get("size", "M"),
                size_description=request.POST.get("size_description", ""),
                available_from=request.POST.get("available_from") or None,
                available_to=request.POST.get("available_to") or None,
                image=request.FILES.get("image"),
                seller_username=seller_username,
                contact_number=request.POST.get("contact_number", "Not provided"),
                ai_condition=ai_condition_value,
            )

            # Deposit = 10% of rent price
            deposit_amount = rent_price * 0.1

            SecurityDeposit.objects.create(
                seller=seller,
                dress=dress,
                amount=deposit_amount,
                cvc_number=request.POST.get("cvc", "0000")
            )

            return JsonResponse({
                "message": "Dress added with security deposit",
                "dress_id": dress.id,
                "deposit_amount": deposit_amount
            }, status=201)

        except Seller.DoesNotExist:
            return JsonResponse({"error": "Seller not found with this username"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
@csrf_exempt
def delete_dress_with_refund(request, dress_id):
    if request.method == "DELETE":
        try:
            dress = Dress.objects.get(id=dress_id)
            deposit = SecurityDeposit.objects.get(dress=dress)

            # ❄️ Check if deposit is frozen
            if deposit.is_frozen:
                return JsonResponse({
                    "error": "This deposit is currently frozen by admin. You cannot delete this dress."
                }, status=403)

            # Proceed if not frozen
            deposit.refunded = True
            deposit.save()
            dress.delete()

            return JsonResponse({
                "message": "Dress deleted successfully, deposit refunded",
                "deposit_refunded": deposit.amount
            }, status=200)

        except Dress.DoesNotExist:
            return JsonResponse({"error": "Dress not found"}, status=404)
        except SecurityDeposit.DoesNotExist:
            return JsonResponse({"error": "Deposit not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)
def list_security_deposits(request):
    deposits = SecurityDeposit.objects.all().select_related('seller', 'dress')
    data = [
        {
            "id": d.id,
            "seller_username": d.seller.username,
            "dress_id": d.dress.id,
            "amount": float(d.amount),
            "is_frozen": d.is_frozen
        }
        for d in deposits
    ]
    return JsonResponse(data, safe=False)
@csrf_exempt
def toggle_freeze_deposit(request, deposit_id):
    if request.method == "POST":
        try:
            deposit = SecurityDeposit.objects.get(id=deposit_id)
            deposit.is_frozen = not deposit.is_frozen  # Toggle state
            deposit.save()

            return JsonResponse({
                "message": f"Deposit {'frozen' if deposit.is_frozen else 'unfrozen'} successfully",
                "is_frozen": deposit.is_frozen
            }, status=200)

        except SecurityDeposit.DoesNotExist:
            return JsonResponse({"error": "Deposit not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)




@csrf_exempt
def list_dresses(request):
    if request.method == "GET":
        dresses = Dress.objects.all()
        data = []
        for d in dresses:
            data.append({
                "id": d.id,
                "name": d.name,
                "color": d.color,
                "rent_price": str(d.rent_price),
                 "category":d.category,
                "description":d.description,
                "size": d.size,
                "length": d.length,
                "city": d.city,
                "occasion": d.occasion,
                "image": request.build_absolute_uri(d.image.url) if d.image else None,
                "seller_username":d.seller_username,
                "contact_number":d.contact_number,
                "ai_condition":d.ai_condition,
            })
        return JsonResponse(data, safe=False)
from .models import RentOrder

@csrf_exempt
# --- File: rentals/views.py ---

@csrf_exempt
def create_rent_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))

            # 1. RentOrder Object banana aur 'new_order' variable mein assign karna
            new_order = RentOrder.objects.create(
                product_id=data.get('product_id'),
                product_name=data.get('product_name'),
                seller_username=data.get('seller_username'),
                seller_contact=data.get('seller_contact'),
                seller_email=data.get('seller_email', 'unknown@wedrentify.com'),
                username=data.get('username'),
                email=data.get('email'),
                postal_code=data.get('postal_code'),
                city=data.get('city'),
                purchase_date=data.get('purchase_date'),
                full_name=data.get('full_name'),
                address=data.get('address'),
                phone_number=data.get('phone_number'),
            )

            # 2. Seller ko email notification bhejne ka logic
            seller_email_to_send = new_order.seller_email

            if seller_email_to_send and seller_email_to_send != 'unknown@wedrentify.com':

                subject = f"🎉 WedRentify: New Order #{new_order.pk} Received!"
                message_body = f"""
Dear {new_order.seller_username},

you have recieved the new order your (Order No: #{new_order.pk})!

Product: {new_order.product_name}
Seller Contact: {new_order.seller_contact}

Buyer Details:
- Name: {new_order.full_name}
- Contact: {new_order.phone_number}
- Buyer Email: {new_order.email}

Kindly! contact the buyer asap.

Thanks,
WedRentify Team
"""
                try:
                    # 🚨 Ye send_mail ab sahi tarah se try block ke andar hai
                    send_mail(
                        subject,
                        message_body,
                        settings.DEFAULT_FROM_EMAIL,
                        [seller_email_to_send],
                        fail_silently=False,
                    )
                except Exception as mail_err:
                    # Mail fail hone par sirf log karein
                    print(f"EMAIL SENDING FAILED for Order #{new_order.pk}: {mail_err}")

            # 3. Final success response (Return statement yahan aayega)
            return JsonResponse({"status": "success", "message": "Order saved and seller notified!"}, status=201)

        except Exception as e:
            # Ye block JSON load error, ya DB save error ko handle karega
            print(f"Error processing rental order: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)



def seller_orders(request, seller_username):
    if request.method == "GET":
        orders = RentOrder.objects.filter(seller_username=seller_username).order_by('-created_at')
        data = []
        for order in orders:
            data.append({
                "order_no": order.order_no,
                "product_id": order.product_id,
                "product_name": order.product_name,
                "seller_username": order.seller_username,
                "seller_contact": order.seller_contact,
                "username": order.username,
                "email": order.email,
                "postal_code": order.postal_code,
                "city": order.city,
                "purchase_date": str(order.purchase_date),
                "full_name": order.full_name,
                "address": order.address,
                "phone_number": order.phone_number,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return JsonResponse({"orders": data}, safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

stripe.api_key =settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = int(float(data.get("amount", 0))) * 100  # Convert to paisa

            if amount <= 0:
                return JsonResponse({"error": "Invalid amount"}, status=400)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'pkr',
                        'product_data': {'name': 'Dress Rental Payment'},
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://127.0.0.1:5500/tayyab_fyp%20-%20Updated/success.html',
                cancel_url='http://127.0.0.1:5500/cancel.html',
            )

            return JsonResponse({'sessionId': session.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_my_orders(request):
    """
    Fetches ALL rent orders from the database.
    Warning: Use this only for admin purposes.
    """
    all_orders = RentOrder.objects.all().order_by('-created_at')
    data = list(all_orders.values())  # .values() gets all fields
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["DELETE"])  # This view will only accept DELETE requests
def delete_order(request, order_no):
    """
    Finds and deletes a specific RentOrder instance by its primary key (order_no).
    """
    try:
        # Find the specific order in the database using its primary key
        order_to_delete = RentOrder.objects.get(pk=order_no)

        # Delete the found order
        order_to_delete.delete()

        # Return a success message in JSON format with a 200 OK status
        return JsonResponse({'message': f'Order #{order_no} has been deleted successfully.'}, status=200)

    except RentOrder.DoesNotExist:
        # If no order with the given 'order_no' is found, return a 404 Not Found error
        return JsonResponse({'error': f'Order with number {order_no} not found.'}, status=404)

    except Exception as e:
        # If any other unexpected error occurs, return a 500 Internal Server Error
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
