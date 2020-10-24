from django.shortcuts import render, get_object_or_404

from .models import Product, Category


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
