# wedrentify_admin/models.py

from django.db import models


class Complaint(models.Model):
    # Unique, auto-incrementing complaint number
    complaint_number = models.AutoField(primary_key=True)

    # Fields from your form
    dispute_type = models.CharField(max_length=255, help_text="e.g., Rental, Auction, Payment")
    user_role = models.CharField(max_length=100, help_text="e.g., Seller, Buyer")
    username = models.CharField(max_length=150)
    cnic = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=20)
    full_name = models.CharField(max_length=255)
    against_username = models.CharField(max_length=150, blank=True, null=True)
    against_contact = models.CharField(max_length=20, blank=True, null=True)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Status field for admin to track progress
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Complaint #{self.complaint_number} by {self.username} - Status: {self.status}"


from django.db import models


class Venue(models.Model):
    """
    Yeh model aapke 'Add New Venue' form ka data store karega.
    """

    # City choices, aapke HTML form ke dropdown se li gayi hain
    CITY_CHOICES = [
        ('Lahore', 'Lahore'),
        ('Karachi', 'Karachi'),
        ('Islamabad', 'Islamabad'),
        ('Rawalpindi', 'Rawalpindi'),
        ('Faisalabad', 'Faisalabad'),
    ]

    # Form Field: venue_name
    venue_name = models.CharField(max_length=255)

    # Form Field: venue_city
    venue_city = models.CharField(max_length=50, choices=CITY_CHOICES)

    # Form Field: venue_image
    # 'upload_to' media folder ke andar 'venue_images/' ka sub-folder banayega
    venue_image = models.ImageField(upload_to='venue_images/', null=True, blank=True)

    # Form Field: venue_description
    venue_description = models.CharField(max_length=255, blank=True, null=True)

    # Form Field: per_head_price (DecimalField currency ke liye behtar hai)
    per_head_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Form Field: contact_number
    # (Aapke table JS 'whatsapp_number' dhoond raha hai, lekin form
    # 'contact_number' bhej raha hai, isliye model form se match karega)
    contact_number = models.CharField(max_length=20)

    # Admin panel mein behtar display ke liye
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.venue_name} ({self.venue_city})"


# models.py mein yeh code add karein
from django.db import models


class DryCleaner(models.Model):
    """Stores information about registered Dry Cleaning vendors."""

    # Auto-incrementing primary key
    id = models.BigAutoField(primary_key=True)

    # Dry Cleaner ka naam
    name = models.CharField(max_length=255, unique=True, verbose_name="Dry Cleaner Name")

    # Contact number (Text field for flexibility)
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number")

    # Image ya logo upload karne ke liye field
    image = models.ImageField(upload_to='drycleaner_images/', null=True, blank=True)

    # Date of registration
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dry Cleaner"
        verbose_name_plural = "Dry Cleaners"
        ordering = ['name']

    def __str__(self):
        return self.name

# Agar aapko yeh model pehle se maujood models.py file mein daalna hai, toh sirf
# class DryCleaner(models.Model): ... wala hissa copy karein.