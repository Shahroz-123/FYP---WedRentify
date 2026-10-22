import scrapy
from ..items import VenueItem
from scrapy.loader import ItemLoader


class VenueSpider(scrapy.Spider):
    """
    Yeh spider 'peonyeventsplanner.com.pk' blog post ko scrape karega.
    (Yeh static HTML hai, yeh 100% chalega)
    """
    name = 'venue_spider'

    # --- NAYI WEBSITE ---
    start_urls = ['https://peonyeventsplanner.com.pk/blog/best-marriage-halls-and-marquees-in-lahore/']

    # --- YEH HAI ASLI FIX ---
    # Hum 'USER_AGENT' ko direct spider mein set kar rahe hain
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }

    # --- END FIX ---

    def parse(self, response):
        """
        Main parsing function (HTML response ko parse karega).
        """

        # --- YEH BHI FIX HAI ---
        # Sahi CSS Selector (div.entry-content ke andar <ol> ke <li>)
        list_items = response.css('div.entry-content ol li')

        if not list_items:
            self.logger.warning(f"No venue list items (<li>) found on {response.url}. Selectors might be outdated.")
            return

        self.logger.info(f"KAMYABI! Is page par {len(list_items)} venues mile.")

        for item in list_items:
            loader = ItemLoader(item=VenueItem(), selector=item)

            # 1. Get Name
            # (e.g., <strong>1. The Nishat Hotel</strong>)
            name_text = item.css('strong::text').get()
            if name_text:
                # "1. " ko naam se hatana
                clean_name = name_text.split('.', 1)[-1].strip()
                loader.add_value('name', clean_name)

            # 2. Get Address
            # (e.g., <p><strong>Address:</strong> Main Boulevard, Lahore</p>)
            address_text = item.xpath('.//p[strong[contains(text(), "Address:")]]/text()').get()
            if address_text:
                loader.add_value('address', address_text.strip())

            # 3. Get Image URL
            loader.add_css('image_url', 'img::attr(src)')

            # 4. Price (Is blog post par price nahi hai)
            loader.add_value('min_price_per_head', 0)  # Default 0

            yield loader.load_item()