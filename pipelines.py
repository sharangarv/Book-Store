import json
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CleaningPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if not adapter.get("title"):
            raise DropItem(f"Missing title: {adapter.get('book_url')}")

        # Clean price
        price_raw = adapter.get("price", "")
        try:
            adapter["price"] = float(
                price_raw.replace("£", "").replace("Â", "").strip()
            )
        except ValueError:
            adapter["price"] = 0.0

        # Clean availability
        avail = adapter.get("availability") or ""
        adapter["availability"] = "In Stock" if "In stock" in avail else "Out of Stock"

        # Clean description
        adapter["description"] = (adapter.get("description") or "").strip()

        return item


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file  = open("books.json", "w", encoding="utf-8")
        self.books = []
        spider.logger.info("📂 JsonWriterPipeline opened — ready to save books")

    def close_spider(self, spider):
        json.dump(self.books, self.file, ensure_ascii=False, indent=2)
        self.file.close()
        spider.logger.info(f"✅ Saved {len(self.books)} books to books.json")

    def process_item(self, item, spider):
        self.books.append(dict(item))
        return item