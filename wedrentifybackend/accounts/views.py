from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import json
from .models import Buyer, Seller, generate_code
from django.contrib.auth.hashers import make_password
from .models import VerificationCode

# -------- Buyer Signup --------
@csrf_exempt
def buyer_signup(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        try:

            buyer = Buyer.objects.create(
                username=data["username"],
                password=make_password(data["password"]),
                cnic=data["cnic"],
                phone=data["phone"],
                email=data["email"]
            )

            return JsonResponse({"message": "Buyer created", "id": buyer.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


# -------- Seller Signup --------
@csrf_exempt
def seller_signup(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        try:
            seller = Seller.objects.create(
                username=data["username"],
                password=make_password(data["password"]),
                cnic=data["cnic"],
                phone=data["phone"],
                email=data["email"]
            )
            return JsonResponse({"message": "Seller created", "id": seller.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
# -------- Buyer Login --------
@csrf_exempt
def buyer_login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        try:
            buyer = Buyer.objects.get(username=data["username"])
            if check_password(data["password"], buyer.password):
                return JsonResponse({"message": "Buyer login successful", "id": buyer.id})
            else:
                return JsonResponse({"error": "Invalid password"}, status=400)
        except Buyer.DoesNotExist:
            return JsonResponse({"error": "Buyer not found"}, status=400)


# -------- Seller Login --------
@csrf_exempt
def seller_login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        try:
            seller = Seller.objects.get(username=data["username"])
            if check_password(data["password"], seller.password):
                return JsonResponse({"message": "Seller login successful", "id": seller.id})
            else:
                return JsonResponse({"error": "Invalid password"}, status=400)
        except Seller.DoesNotExist:
            return JsonResponse({"error": "Seller not found"}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Buyer, Seller
import json

# ✅ Get all users (buyers + sellers)
def list_all_users(request):
    buyers = list(Buyer.objects.values("id", "username", "cnic", "email"))
    sellers = list(Seller.objects.values("id", "username", "cnic", "email"))
    users = [{"type": "Buyer", **b} for b in buyers] + [{"type": "Seller", **s} for s in sellers]
    return JsonResponse(users, safe=False)

# ✅ Delete user by ID and type
@csrf_exempt
def delete_user(request, user_type, user_id):
    if request.method == "DELETE":
        try:
            if user_type.lower() == "buyer":
                Buyer.objects.get(id=user_id).delete()
            elif user_type.lower() == "seller":
                Seller.objects.get(id=user_id).delete()
            else:
                return JsonResponse({"error": "Invalid user type"}, status=400)
            return JsonResponse({"message": f"{user_type} deleted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# --- File: accounts/views.py (Function 1: Sends Code) ---

from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import datetime
# Import your new model



@csrf_exempt
def send_verification_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username', 'User')  # Use 'User' if username is not in JSON

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            # 1. Generate or update the code object
            # This automatically calls generate_code() for the 'code' field
            code_obj, created = VerificationCode.objects.update_or_create(
                email=email,
                defaults={
                    'code': generate_code(),
                    'created_at': timezone.now(),
                    'expires_at': timezone.now() + datetime.timedelta(minutes=10)
                }
            )

            # 2. Send the email using the code
            subject = "WedRentify Verification Code"
            message = f"Hello {username},\n\nYour verification code is: {code_obj.code}\n\nThis code expires in 10 minutes. Do not share this code with anyone."

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return JsonResponse({"message": "Verification code sent"}, status=200)

        except Exception as e:
            print(f"Error sending verification email: {str(e)}")
            return JsonResponse({"error": "Failed to send code. Please check email address."}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# --- File: accounts/views.py (Verify Code Function) ---

@csrf_exempt
def verify_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            submitted_code = data.get('code')

            if not email or not submitted_code:
                return JsonResponse({"error": "Email and code are required."}, status=400)

            try:
                code_obj = VerificationCode.objects.get(email=email)
            except VerificationCode.DoesNotExist:
                return JsonResponse({"error": "Invalid email or code request."}, status=400)

            # 1. Check if the code is correct and not expired
            if code_obj.code == submitted_code and code_obj.is_valid():
                # 2. Delete the code immediately upon success (one-time use)
                code_obj.delete()
                return JsonResponse({"message": "Code verified successfully!"}, status=200)

            # 3. Handle incorrect or expired code
            if not code_obj.is_valid():
                code_obj.delete()  # Delete expired code
                return JsonResponse({"error": "Code expired. Please request a new one."}, status=400)
            else:
                return JsonResponse({"error": "Invalid code entered."}, status=400)

        except Exception as e:
            print(f"Error during code verification: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)