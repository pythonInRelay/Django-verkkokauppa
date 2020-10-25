from django.db import models

from apps.store.models import Product


# Database entries for user info, self explanatory
class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

# Add order creation time
    created_at = models.DateTimeField(auto_now_add=True)

# Is order paid? If yes, how much?
    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.first_name


# Database entry for the order item
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # When delete order del items
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)  # Do not del order if product goes out of stock
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id
