from django.shortcuts import render, redirect

from .cart import Cart


# Redirect and render method for updating items to the cart
def cart_detail(request):
    cart = Cart(request)
    products_string = ''  # Create new product string so Django can create string

    for item in cart:  # Loop through items in the cart
        product = item['product']
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', product_id: '%s'}," % (product.id, product.title, product.price, item['quantity'], item['total_price'], product.product_id)

        products_string += b  # Append above to products_string

    context = {
        'cart': cart,
        'products_string': products_string
    }

    return render(request, 'cart.html', context)
