import scrapy
from datetime import datetime
from scraper.items import BookItem


RATING_MAP = {
    "One":   1,
    "Two":   2,
    "Three": 3,
    "Four":  4,
    "Five":  5,
}


class BooksSpider(scrapy.Spider):
    name            = "books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls      = ["http://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        """Parse each listing page — extract book links and follow next page."""

        # Get all book links on this page
        books = response.css("article.product_pod h3 a::attr(href)").getall()
        self.logger.info(f"Found {len(books)} books on {response.url}")

        for href in books:
            # Fix relative URL
            book_url = response.urljoin(href)
            yield response.follow(book_url, callback=self.parse_book)

        # Follow next page
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            next_url = response.urljoin(next_page)
            self.logger.info(f"Following next page: {next_url}")
            yield response.follow(next_url, callback=self.parse)

    def parse_book(self, response):
        """Extract full details from individual book page."""

        # ── Title ─────────────────────────────────────────────────────────────
        title = response.css("h1::text").get(default="").strip()

        # ── Price ─────────────────────────────────────────────────────────────
        price = response.css("p.price_color::text").get(default="").strip()

        # ── Rating ────────────────────────────────────────────────────────────
        rating_word = response.css("p.star-rating::attr(class)").get(default="")
        rating_word = rating_word.replace("star-rating", "").strip()
        rating_num  = RATING_MAP.get(rating_word, 0)

        # ── Availability ──────────────────────────────────────────────────────
        availability = response.css("p.availability::text").getall()
        availability = " ".join(availability).strip()

        # ── Category ──────────────────────────────────────────────────────────
        # Breadcrumb: Home > category > book title
        breadcrumb = response.css("ul.breadcrumb li a::text").getall()
        category   = breadcrumb[-1].strip() if len(breadcrumb) >= 2 else "Unknown"

        # ── Description ───────────────────────────────────────────────────────
        description = response.css("article.product_page > p::text").get(default="").strip()

        # ── Product table (UPC, reviews) ──────────────────────────────────────
        table_rows = response.css("table.table tr")
        upc         = ""
        num_reviews = 0
        for row in table_rows:
            header = row.css("th::text").get(default="")
            value  = row.css("td::text").get(default="")
            if header == "UPC":
                upc = value
            elif header == "Number of reviews":
                try:
                    num_reviews = int(value)
                except ValueError:
                    num_reviews = 0

        # ── Image ─────────────────────────────────────────────────────────────
        image_src = response.css("div.item.active img::attr(src)").get(default="")
        image_url = response.urljoin(image_src)

        item = BookItem()
        item["title"]        = title
        item["price"]        = price
        item["rating"]       = rating_word
        item["rating_num"]   = rating_num
        item["availability"] = availability
        item["category"]     = category
        item["description"]  = description
        item["upc"]          = upc
        item["num_reviews"]  = num_reviews
        item["image_url"]    = image_url
        item["book_url"]     = response.url
        item["scraped_at"]   = datetime.utcnow().isoformat() + "Z"

        yield item