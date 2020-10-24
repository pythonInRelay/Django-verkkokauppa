from django.conf import settings


# Cart cookie logic and init func
class Cart(object):
    def __init__(self, request):
        self.session = request.session  # Set session to the one in the request
        cart = self.session.get(settings.SESSION_COOKIE_AGE)  # Cart instance gets cookie age

        if not cart:  # If no session exists
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

        # Function for adding products to cart
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        price = product.price

        if product_id not in self.cart:  # Checks if product id is inside the cart already, creates and instance and sets below
            self.cart[product_id] = {'quantity': 0, 'price': price, 'id': product_id}  # Set to string instead of dict index

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += 1  # Add one extra when updating quantity

        # Save function
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart  # Update cookie/session
        self.session.modified = True  # Browser knows session has been modified
