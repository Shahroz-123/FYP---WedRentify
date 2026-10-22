from itemadapter import ItemAdapter
from venues.models import Venue
import logging
from asgiref.sync import sync_to_async  # <-- YEH IMPORT ZAROORI HAI

logger = logging.getLogger(__name__)


class ShadiyanaScraperPipeline:

    # --- YEH FUNCTION BLOCKING HAI, ISKO WRAP KARENGE ---
    @sync_to_async
    def save_item_to_db(self, adapter):
        """
        Yeh function database operations ko sync_to_async wrapper mein chalayega.
        """
        try:
            venue, created = Venue.objects.update_or_create(
                name=adapter.get('name'),
                defaults={
                    'address': adapter.get('address'),
                    'min_price_per_head': adapter.get('min_price_per_head', 0),
                    'image_url': adapter.get('image_url'),
                }
            )

            if created:
                logger.info(f"NAYA VENUE CREATE HUA: {venue.name}")
            else:
                logger.info(f"VENUE UPDATE HUA: {venue.name}")

        except Exception as e:
            # Item ko dict mein convert karein taaki log mein error na aaye
            item_dict = adapter.asdict()
            logger.error(f"Venue save karne mein error aaya: {e} - Item: {item_dict}")

    # --- PROCESS_ITEM AB 'ASYNC' HONA ZAROORI HAI ---
    async def process_item(self, item, spider):
        """
        Yeh function item receive karega aur wrapped function ko call karega.
        """
        adapter = ItemAdapter(item)

        if not adapter.get('name'):
            logger.warning(f"Venue item ko reject kar diya gaya (naam nahi tha): {item}")
            return item

        # 'await' use karein wrapped function call karne ke liye
        await self.save_item_to_db(adapter)

        return item