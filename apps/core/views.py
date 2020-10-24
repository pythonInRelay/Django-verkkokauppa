from django.shortcuts import render
from apps.store.models import Product


# Render the frontpage
def frontpage(request):
    products = Product.objects.all()  # Show all the products in the database

    context = {
        'products': products
    }
    return render(request, 'frontpage.html', context)


# Render contact page
def contact(request):
    return render(request, 'contact.html')

