import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from apps.cart.cart import Cart

from .models import Product


# Create the api for adding products to the cart
def api_add_to_cart(request):

    data = json.loads(request.body)
    json_response = {'success': True}
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']  # Default quantity is 1

    cart = Cart(request)  # Update cart to above values

    product = get_object_or_404(Product, pk=product_id)  # Public key is product_id if it can't be found throw 404

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)  # If not updating the cart, add 1 quantity
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)  # Else update with user's chosen quantity

    return JsonResponse(json_response)

# Create the api for removing products to the cart
def api_remove_from_cart(request):
    data = json.loads(request.body)
    json_response = {'success': True}
    product_id = str(data['product_id'])  # Cast as string or throws an error in console

    cart = Cart(request)  # Update cart to above values
    cart.remove(product_id)  # Remove the product from the cart

    return JsonResponse(json_response)

