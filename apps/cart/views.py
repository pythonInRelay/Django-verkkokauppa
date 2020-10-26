from django.shortcuts import render, redirect
from django.conf import settings

from .cart import Cart


# Redirect and render method for updating items to the cart
def cart_detail(request):
    cart = Cart(request)
    products_string = ''  # Create new product string so Django can create string

    for item in cart:  # Loop through items in the cart and provide the following views
        product = item['product']
        url = '/%s/%s' % (product.category.slug, product.slug)  # Item pages as item
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', product_id: '%s', " \
            "'thumbnail': '%s', 'url': '%s'}," % (
            product.id, product.title, product.price, item['quantity'], item['total_price'],
            product.product_id, product.thumbnail.url, url)

        products_string += b  # Append above to products_string

    context = {
        'cart': cart,
        'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
        'products_string': products_string
    }

    return render(request, 'cart.html', context)


# Add payment success page
def success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'success.html')
