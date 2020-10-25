import datetime
import os

from random import randint

from apps.cart.cart import Cart

from apps.order.models import Order, OrderItem


# Create a database entry for all the following customer data
def checkout(request, first_name, last_name, email, address, zipcode, city, country):
    order = Order(first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode, city=city, country=country)
    order.save()

    # Create a cart instance
    cart = Cart(request)

    # For each item in cart, create one of the order items for each product
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

    # Get the id from the above order
    return order.id
