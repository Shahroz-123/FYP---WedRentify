# Scrapy settings for shadiyana_scraper project

# --- DJANGO INTEGRATION (ZAROORI) ---
import os
import sys
import django

# Path to the Django project root (wedrentifybackend)
DJANGO_PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Django project ko Python path mein add karo
sys.path.append(DJANGO_PROJECT_PATH)

# Django settings module ko set karo
os.environ['DJANGO_SETTINGS_MODULE'] = 'wedrentify.settings'

# Django ko setup karo taaki models import ho sakein
django.setup()
# --- END DJANGO INTEGRATION ---


BOT_NAME = "shadiyana_scraper"

SPIDER_MODULES = ["shadiyana_scraper.spiders"]
NEWSPIDER_MODULE = "shadiyana_scraper.spiders"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Scraper ko Google Chrome browser ki tarah mask karo
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'


# Configure item pipelines
ITEM_PIPELINES = {
   "shadiyana_scraper.pipelines.ShadiyanaScraperPipeline": 300,
}

# --- PLAYWRIGHT INTEGRATION (ADD AT THE END) ---
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# --- END PLAYWRIGHT INTEGRATION ---