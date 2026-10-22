from django.db import models
from django.http import JsonResponse

from accounts.models import Seller
class Dress(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="dresses")
    name = models.CharField(max_length=200)
    description = models.TextField()
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)

    city = models.CharField(max_length=100, default="Unknown")
    category = models.CharField(max_length=50, default="Uncategorized")
    occasion = models.CharField(max_length=100, default="General")
    color = models.CharField(max_length=50, default="Not specified")
    length = models.CharField(max_length=20, default="Medium")
    size = models.CharField(max_length=10, default="M")
    size_description = models.TextField(default="No description")

    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="dresses/", null=True, blank=True)
    contact_number = models.CharField(max_length=15, default="Not provided")

    created_at = models.DateTimeField(auto_now_add=True)
    seller_username = models.CharField(max_length=150, null=True, blank=True)
    ai_condition = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class SecurityDeposit(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="deposits")
    dress = models.OneToOneField(Dress, on_delete=models.CASCADE, related_name="deposit")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    cvc_number = models.CharField(max_length=4, null=True, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    refunded = models.BooleanField(default=False)
    is_frozen = models.BooleanField(default=False)  # 🔥 NEW FIELD

    def __str__(self):
        return f"{self.seller.username} - {self.amount}"

from django.db import models

class RentOrder(models.Model):
    order_no = models.AutoField(primary_key=True)  # ✅ Auto-incremented order number

    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    seller_username = models.CharField(max_length=255)
    seller_contact = models.CharField(max_length=20, blank=True, null=True)

    username = models.CharField(max_length=255)
    email = models.EmailField()
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    purchase_date = models.DateField()
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    seller_email = models.EmailField(max_length=254, default='no-email@example.com')
    def __str__(self):
        return f"Order #{self.order_no} - {self.username} ordered {self.product_name}"


def get_my_orders(request):
    """
    Fetches and returns all rent orders for the currently
    authenticated user.
    """
    # 2. Filter orders by the 'username' field, matching the logged-in user
    try:
        user_orders = RentOrder.objects.filter(username=request.user.username).order_by('-created_at')

        # 3. Convert the QuerySet to a list of dictionaries
        # .values() selects only the fields you need for the frontend
        data = list(user_orders.values(
            'order_no',
            'product_id',
            'product_name',
            'seller_username',
            'purchase_date',
            'full_name',
            'address',
            'city',
            'postal_code',
            'phone_number',
            'created_at'
        ))

        # 4. Return the list as a JSON response
        # safe=False is required because we are sending a list, not a dict
        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)