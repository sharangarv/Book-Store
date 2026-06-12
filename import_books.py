"""
Imports scraped books from books.json into MySQL via Django ORM.

Usage:
    python manage.py import_books
    python manage.py import_books --file path/to/books.json
    python manage.py import_books --clear
"""

import json
from pathlib import Path
from datetime import datetime, timezone

from django.core.management.base import BaseCommand, CommandError
from books.models import Book


class Command(BaseCommand):
    help = 'Import scraped books from JSON into MySQL database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='books.json',
            help='Path to books.json (default: books.json)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing books before importing',
        )

    def handle(self, *args, **options):
        filepath = Path(options['file'])

        if not filepath.exists():
            raise CommandError(
                f"File not found: {filepath.resolve()}\n"
                f"Make sure books.json is in the same folder as manage.py"
            )

        if options['clear']:
            count = Book.objects.count()
            Book.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {count} existing books.'))

        with open(filepath, encoding='utf-8') as f:
            books = json.load(f)

        self.stdout.write(f"\nImporting {len(books)} books...\n")

        created_count = 0
        updated_count = 0
        error_count   = 0

        for data in books:
            upc = (data.get('upc') or '').strip()
            if not upc:
                error_count += 1
                continue

            # Parse scraped_at
            scraped_at  = None
            raw_scraped = data.get('scraped_at', '')
            if raw_scraped:
                try:
                    scraped_at = datetime.fromisoformat(
                        raw_scraped.replace('Z', '+00:00')
                    )
                except ValueError:
                    pass

            try:
                obj, created = Book.objects.update_or_create(
                    upc=upc,
                    defaults={
                        'title':        (data.get('title')       or '')[:500],
                        'price':        data.get('price')        or 0.0,
                        'rating':       (data.get('rating')      or '')[:10],
                        'rating_num':   data.get('rating_num')   or 0,
                        'availability': data.get('availability') or 'Out of Stock',
                        'category':     (data.get('category')    or '')[:100],
                        'description':  data.get('description')  or '',
                        'num_reviews':  data.get('num_reviews')  or 0,
                        'image_url':    (data.get('image_url')   or '')[:500],
                        'book_url':     (data.get('book_url')    or '')[:500],
                        'scraped_at':   scraped_at,
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(f"  [NEW] {obj.title[:65]}")
                else:
                    updated_count += 1
                    self.stdout.write(f"  [UPD] {obj.title[:65]}")

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"  [ERR] {data.get('title', '')[:50]} → {e}")
                )

        # Summary
        self.stdout.write("\n" + "=" * 55)
        self.stdout.write(self.style.SUCCESS(f"  ✅  Created  : {created_count}"))
        self.stdout.write(                   f"  🔄  Updated  : {updated_count}")
        self.stdout.write(                   f"  ❌  Errors   : {error_count}")
        self.stdout.write(                   f"  📦  Total in DB : {Book.objects.count()}")
        self.stdout.write("=" * 55 + "\n")