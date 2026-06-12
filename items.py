import scrapy


class BookItem(scrapy.Item):
    title       = scrapy.Field()
    price       = scrapy.Field()
    rating      = scrapy.Field()    # One, Two, Three, Four, Five
    rating_num  = scrapy.Field()    # 1, 2, 3, 4, 5
    availability = scrapy.Field()  # In stock / Out of stock
    category    = scrapy.Field()
    description = scrapy.Field()
    upc         = scrapy.Field()    # unique product code
    num_reviews = scrapy.Field()
    image_url   = scrapy.Field()
    book_url    = scrapy.Field()
    scraped_at  = scrapy.Field()