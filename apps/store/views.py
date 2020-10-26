from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Product, Category


# Create the necessary search function for assignment
def search(request):
    query = request.GET.get('query')
    qs = Q(title__icontains=query) | Q(description__icontains=query)
    if query.isdigit():  # Because product_id is an integer it must be cast as an int on its own to prevent a ValueError
        qs |= Q(product_id=query)
    products = Product.objects.filter(qs)

    context = {
        'query': query,
        'products': products
    }

    return render(request, 'search.html', context)


def product_detail(request, category_slug, slug):  # Maybe remove unused category_slug
    product = get_object_or_404(Product, slug=slug)  # Get the product or show 404

    context = {
        'product': product
    }

    return render(request, 'product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()  # Get the related field from views.py

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'category_detail.html', context)
