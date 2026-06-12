from django.db import models


class Book(models.Model):

    RATING_CHOICES = [
        (1, '⭐ One'),
        (2, '⭐⭐ Two'),
        (3, '⭐⭐⭐ Three'),
        (4, '⭐⭐⭐⭐ Four'),
        (5, '⭐⭐⭐⭐⭐ Five'),
    ]

    AVAILABILITY_CHOICES = [
        ('In Stock',    'In Stock'),
        ('Out of Stock','Out of Stock'),
    ]

    title        = models.CharField(max_length=500)
    price        = models.DecimalField(max_digits=6, decimal_places=2)
    rating       = models.CharField(max_length=10, blank=True)
    rating_num   = models.IntegerField(choices=RATING_CHOICES, default=0)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='In Stock')
    category     = models.CharField(max_length=100, blank=True)
    description  = models.TextField(blank=True)
    upc          = models.CharField(max_length=100, unique=True)
    num_reviews  = models.IntegerField(default=0)
    image_url    = models.URLField(max_length=500, blank=True)
    book_url     = models.URLField(max_length=500, blank=True)
    scraped_at   = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering        = ['title']
        verbose_name    = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title