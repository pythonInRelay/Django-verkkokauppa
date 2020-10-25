from django.conf import settings

from apps.store.models import Product


# Cart cookie logic and init func
class Cart(object):
    def __init__(self, request):
        self.session = request.session  # Set session to the one in the request
        cart = self.session.get(settings.CART_SESSION_ID)  # Cart instance gets cart items

        if not cart:  # If no session exists
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    # Calculate item price according to quantity when adding to cart
    def __iter__(self):
        product_ids = self.cart.keys()

        product_clean_ids = []

        for pid in product_ids:
            product_clean_ids.append(pid)

            self.cart[str(pid)]['product'] = Product.objects.get(pk=pid)

        for item in self.cart.values():
            item['total_price'] = float(item['price']) * int(item['quantity'])

            yield item  # Be sure price is set to int

    # Get length of all products, for each item in cart calculate its value
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # Function for adding products to cart
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        price = product.price

        if product_id not in self.cart:  # Checks if product id is inside the cart already, creates and instance and sets below
            self.cart[product_id] = {'quantity': 0, 'price': price, 'id': product_id}  # Set to string instead of dict index

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity  # Add one extra when updating quantity
        else:
            self.cart[product_id]['quantity'] += 1  # When adding a new product to cart, just add 1

        self.save()

    # Function for removing items from the cart
    def remove(self, product_id):
        if product_id in self.cart:  # If the id exists in the cart remove it and save
            del self.cart[product_id]
            self.save()

    # Save function
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart  # Update cookie/session
        self.session.modified = True  # Browser knows session has been modified

    # Clear cart after order complete
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True  # Update browser session

    # Cart button increment function (return value of item quantity plus items in cart)
    def get_total_length(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    # Show total price for the whole cart in navbar
    def get_total_cost(self):
        return sum(float(item['total_price']) for item in self)
