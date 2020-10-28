import json
import stripe

from django.conf import settings
from django.http import HttpResponse

from .cart import Cart

from apps.order.models import Order


# Uses the Stripe API to process payments by querying the private key against my test business
def webhook(request):
    payload = request.body
    event = None  # Create empty event

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as err:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':  # Update the event if the payment succeeds
        payment_intent = event.data.object
        print('Payment intent:', payment_intent)

        order = Order.objects.get(payment_intent=payment_intent.id)
        order.paid = True  # Set to paid on the orders page
        order.save()

    return HttpResponse(status=200)
