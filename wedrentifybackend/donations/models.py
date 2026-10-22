from django.db import models

class Donation(models.Model):
    donor_name = models.CharField(max_length=100)
    donor_contact = models.CharField(max_length=20)
    dress_title = models.CharField(max_length=150)
    dress_description = models.TextField(blank=True, null=True)
    dress_size = models.CharField(max_length=50, blank=True, null=True)
    dress_image = models.ImageField(upload_to='donations/', blank=True, null=True)
    buyer_username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dress_title} donated by {self.donor_name}"
