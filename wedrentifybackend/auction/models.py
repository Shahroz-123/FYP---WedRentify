from django.db import models

# Define choices for fields to ensure data consistency
class DressChoices:
    # Condition Choices
    CONDITION_CHOICES = [
        ('Brand New', 'Brand New'),
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Worn Once', 'Worn Once'),
    ]

    # Fabric Choices
    FABRIC_CHOICES = [
        ('Silk', 'Silk'),
        ('Velvet', 'Velvet'),
        ('Chiffon', 'Chiffon'),
        ('Cotton Silk', 'Cotton Silk'),
        ('Raw Silk', 'Raw Silk'),
        ('Organza', 'Organza'),
        ('Georgette', 'Georgette'),
        ('Net', 'Net'),
        ('Brocade', 'Brocade'),
        ('Banarsi', 'Banarsi'),
        ('Jamawar', 'Jamawar'),
        ('Karandi', 'Karandi'),
        ('Khaddar', 'Khaddar'),
        ('Korean Raw Silk', 'Korean Raw Silk'),
        ('Pure Chiffon', 'Pure Chiffon'),
    ]

    # Work Intensity Choices
    INTENSITY_CHOICES = [
        ('Heavy', 'Heavy'),
        ('Medium', 'Medium'),
        ('Light', 'Light'),
    ]


class AuctionDress(models.Model):
    """
    Model to store details of a Pakistani Wedding Dress added for auction.
    This model maps directly to the form fields in your frontend.
    """
    # Seller/Tracking Information (from localStorage)
    seller_username = models.CharField(
        max_length=100,
        help_text="Username of the seller who uploaded the dress."
    )

    # Core Dress Details
    dress_color = models.CharField(
        max_length=50,
        help_text="Primary color of the dress (e.g., Red, Royal Blue)."
    )
    dress_image = models.ImageField(
        upload_to='dress_images/',
        help_text="Image file of the dress.",
        null=True, blank=True # Allow null/blank temporarily if testing without file uploads
    )
    seller_contact = models.CharField(
        max_length=15,
        help_text="Seller's contact phone number."
    )

    # Prediction Fields
    original_price_pkr = models.IntegerField(
        help_text="Original purchase price in PKR (e.g., 50000)."
    )
    condition = models.CharField(
        max_length=20,
        choices=DressChoices.CONDITION_CHOICES,
        help_text="Condition of the dress (e.g., Brand New, Worn Once)."
    )
    dress_age_months = models.IntegerField(
        help_text="Age of the dress in months."
    )
    fabric = models.CharField(
        max_length=50,
        choices=DressChoices.FABRIC_CHOICES,
        help_text="Primary fabric type."
    )
    work_intensity = models.CharField(
        max_length=10,
        choices=DressChoices.INTENSITY_CHOICES,
        help_text="Embroidery work intensity."
    )
    trail_length_ft = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text="Length of the trail/train in feet (e.g., 2.5)."
    )
    is_fully_embroidered = models.BooleanField(
        default=False,
        help_text="Is the entire dress fully embroidered?"
    )
    is_handwork = models.BooleanField(
        default=False,
        help_text="Does the dress feature handwork/hand embroidery?"
    )

    # Metadata
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dress_color} Dress ({self.fabric}) - Seller: {self.seller_username}"

    class Meta:
        verbose_name = "Auction Dress Listing"
        verbose_name_plural = "Auction Dress Listings"
from django.db import models

class Bid(models.Model):
    # OneToOneField yeh yakeeni banata hai ke har dress ki sirf EK hi bid row ho

    # FIX: Yahan 'AuctionItem' ki jagah 'AuctionDress' ayega
    auction_item = models.OneToOneField(AuctionDress, on_delete=models.CASCADE, primary_key=True)

    # Seller ki details (jo hum copy karke layenge)
    seller_username = models.CharField(max_length=150)
    seller_contact = models.CharField(max_length=20)

    # Bid ki details (yeh update hoti rahengi)
    highest_bid = models.IntegerField(default=0)
    buyer_username = models.CharField(max_length=150, blank=True, null=True)
    buyer_contact = models.CharField(max_length=20, blank=True, null=True)

    last_updated = models.DateTimeField(auto_now=True)  # Yeh track rakhega kab update hua

    def __str__(self):
        # FIX: Yahan bhi 'auction_item.dress_name' ki jagah 'auction_item.dress_color'
        # ya koi aur field ayega jo AuctionDress mein hai (jaise 'dress_color')
        # Hum 'auction_item' use kar sakte hain kyunke woh object ko refer kar raha hai
        return f"Bid for {self.auction_item} (Current: {self.highest_bid})"
    last_updated = models.DateTimeField(auto_now=True)  # Yeh track rakhega kab update hua

    def __str__(self):
        return f"Bid for {self.auction_item.dress_name} (Current: {self.highest_bid})"