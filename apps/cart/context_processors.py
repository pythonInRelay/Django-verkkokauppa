from .cart import Cart


#  Makes the cart available globally so its length is always visible
def cart(request):  # Creates a new instance from context every time it is requested
    return {'cart': Cart(request)}
