from django.db import models

# Create your models here.
from django.db import models

class Buyer(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    cnic = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Seller(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    cnic = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=20000.00)

    def __str__(self):
        return self.username
    
# --- File: accounts/models.py (New Code Block) ---

from django.db import models
from django.utils import timezone
import random

def generate_code():
    # Generates a random 6-digit code as a string
    return str(random.randint(100000, 999999))

class VerificationCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6, default=generate_code)
    created_at = models.DateTimeField(default=timezone.now)
    # Code is valid for 10 minutes
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=10))

    def is_valid(self):
        # Checks if the current time is less than the expiration time
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Code for {self.email}: {self.code}"

# 🚨 ACTION: Run the following commands in your terminal:

