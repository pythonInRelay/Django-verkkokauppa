import json
import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from django.conf import settings
from apps.cart.cart import Cart

from apps.order.utils import checkout

from .models import Product
from apps.order.models import Order


def create_checkout_session(request):
    cart = Cart(request)

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    items = []
    for item in cart:
        product = item['product']

        price = int(product.price * 100)

        obj = {
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': product.title
                },
                'unit_amount': price  # Cents not dollars! Stripe does conversion (Stripe docs)
            },
            'quantity': item['quantity']
        }
        items.append(obj)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://localhost:8000/cart/success/',
        cancel_url='http://localhost:8000/cart/'
    )

    """ Create Order Block Start """

    data = json.loads(request.body)
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    city = data['city']
    country = data['country']
    payment_intent = session.payment_intent

    orderid = checkout(request, first_name, last_name, email, address, zipcode, city, country)

    total_price = 0.00

    # Create new variable and loop through all products
    for item in cart:
        product = item['product']
        total_price += (float(product.price) * int(item['quantity']))  # Add total price to admin page data

    order = Order.objects.get(pk=orderid)
    order.payment_intent = payment_intent
    order.paid_amount = total_price
    order.save()

    """ Create Order Block End """

    return JsonResponse({'session': session})


def api_checkout(request):
    cart = Cart(request)

    data = json.loads(request.body)
    json_response = {'success': True}
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    city = data['city']
    country = data['country']

    orderid = checkout(request, first_name, last_name, email, address, zipcode, city, country)

    paid = True

    if paid:
        order = Order.objects.get(pk=orderid)
        order.paid = True
        order.paid_amount = cart.get_total_cost()
        order.save()

        cart.clear()  # When order is complete and paid clear the cart

    return JsonResponse(json_response)


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

