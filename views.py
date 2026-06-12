from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Book


def book_list(request):
    query    = request.GET.get('q', '')
    category = request.GET.get('category', '')
    rating   = request.GET.get('rating', '')
    sort     = request.GET.get('sort', 'title')

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    if category:
        books = books.filter(category=category)

    if rating:
        books = books.filter(rating_num=rating)

    sort_map = {
        'title':       'title',
        'price_asc':   'price',
        'price_desc':  '-price',
        'rating':      '-rating_num',
    }
    books = books.order_by(sort_map.get(sort, 'title'))

    paginator = Paginator(books, 20)
    page      = paginator.get_page(request.GET.get('page'))

    categories = Book.objects.values_list(
        'category', flat=True
    ).distinct().order_by('category')

    return render(request, 'books/book_list.html', {
        'page_obj':   page,
        'query':      query,
        'category':   category,
        'rating':     rating,
        'sort':       sort,
        'categories': categories,
        'total':      Book.objects.count(),
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})
