from django.shortcuts import render
from apps.store.models import Product


# Render the frontpage
def frontpage(request):
    products = Product.objects.filter(is_featured=True)  # Show ONLY FEATURED products on frontpage

    context = {
        'products': products
    }
    return render(request, 'frontpage.html', context)


# Render contact page
def contact(request):
    return render(request, 'contact.html')


# Render the about page
def about(request):
    return render(request, 'about.html')