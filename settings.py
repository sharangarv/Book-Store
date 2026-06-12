BOT_NAME = "books_scraper"

SPIDER_MODULES   = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

ROBOTSTXT_OBEY           = True
DOWNLOAD_DELAY           = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS      = 8

DEFAULT_REQUEST_HEADERS = {
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

ITEM_PIPELINES = {
    "scraper.pipelines.CleaningPipeline":   100,
    "scraper.pipelines.JsonWriterPipeline": 200,
}

FEED_EXPORT_ENCODING = "utf-8"
LOG_LEVEL            = "INFO"