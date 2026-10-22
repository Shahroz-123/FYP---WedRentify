from django.db import models

# Create your models here.
from django.db import models


class Venue(models.Model):
    # Venue ka naam (main key)
    name = models.CharField(max_length=255, unique=True, verbose_name="Venue Ka Naam")
    # Venue ka address
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="Pata")
    # Venue ki description (brief summary)
    description = models.TextField(blank=True, null=True, verbose_name="Tafseel")
    # Minimum price per head (filtering ke liye integer mein store karenge)
    # Yeh woh value hai jo hamara scraper nikalega
    min_price_per_head = models.IntegerField(default=0, help_text="PKR / Head Mein Qeemat",
                                             verbose_name="Min Price Per Head")
    # Rating (e.g., 4.5)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name="Rating")
    # Image URL (sirf URL store karenge)
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Tasveer Ka URL")

    # Jab data scrape hua tha
    scraped_on = models.DateTimeField(auto_now_add=True, verbose_name="Data Scrape Hua")

    class Meta:
        verbose_name = "Wedding Venue"
        verbose_name_plural = "Wedding Venues"
        # Hum data ko naye se purane ke order mein dekhenge
        ordering = ['-scraped_on']

    def __str__(self):
        return self.name
