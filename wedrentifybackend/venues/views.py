[import subprocess
import sys
import os
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Venue

# Scrapy project ki directory (yeh 'manage.py' ke saath honi chahiye)
SCRAPER_PROJECT_DIR = 'shadiyana_scraper'


@csrf_exempt  # Alag frontend se POST request allow karne ke liye
def venue_api_view(request):
    ""
    Yeh API View do kaam karta hai:
    1. GET Request: Venues ko filter karke JSON mein return karta hai.
    2. POST Request: Scraper ko run karta hai.
    """

    # ----------------------------------------
    # 1. GET Request (Data Fetch Karna)
    # ----------------------------------------
    if request.method == 'GET':
        max_price_per_head_str = request.GET.get('max_price_per_head', '').strip()

        # Default: Saare venues fetch karo
        filtered_venues = Venue.objects.all()

        if max_price_per_head_str:
            try:
                max_price = int(max_price_per_head_str)
                # Filtering Logic
                filtered_venues = filtered_venues.filter(
                    Q(min_price_per_head__lte=max_price)
                ).order_by('min_price_per_head')
            except ValueError:
                return JsonResponse({'error': 'Invalid max_price. Must be a number.'}, status=400)

        # --- UPDATE ---
        # QuerySet ko .values() se dictionary list banayein
        # (description aur rating hata diye gaye hain)
        data = list(filtered_venues.values(
            'name',
            'address',
            'description'
            'min_price_per_head',
            'image_url'
        ))
        # -----------------------------------------------

        return JsonResponse({'venues': data, 'message': 'Venues fetched successfully'})

    # ----------------------------------------
    # 2. POST Request (Scraper Run Karna)
    # ----------------------------------------
    elif request.method == 'POST':
        if not os.path.isdir(SCRAPER_PROJECT_DIR):
            error_msg = f"Error: Scrapy project directory '{SCRAPER_PROJECT_DIR}' not found on server."
            return JsonResponse({'error': error_msg}, status=500)

        try:
            # Spider ka naam check karein (e.g., 'venue_spider')
            process = subprocess.run(
                [sys.executable, '-m', 'scrapy', 'crawl', 'venue_spider'],
                cwd=SCRAPER_PROJECT_DIR,
                capture_output=True,
                text=True,
                check=True
            )

            return JsonResponse({'message': 'Scraping started successfully! Data is being saved/updated.'})

        except subprocess.CalledProcessError as e:
            error_message = f"Scraping Failed! Error: {e.stderr.strip()}..."
            return JsonResponse({'error': error_message}, status=500)

        except FileNotFoundError:
            return JsonResponse({'error': 'Scrapy or Python executable command not found.'}, status=500)

    # ----------------------------------------
    # 3. Baki Methods (PUT, DELETE, etc.)
    # ----------------------------------------
    else:
        return JsonResponse({'error': 'Method not allowed. Use GET to fetch, POST to scrape.'}, status=405)