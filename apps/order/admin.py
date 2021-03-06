import datetime

from django.urls import reverse
from django.contrib import admin

from .models import Order, OrderItem

# Add additional information to admin page with order ID, name, created at etc. Thanks to Django templates!


# On the other page return the person's first and last name
def order_name(obj):
    return '%s %s' % (obj.first_name, obj.last_name)
order_name.short_description = 'Name'


# Add date when the orders get shipped
def admin_order_shipped(modeladmin, request, queryset):
    for order in queryset:
        order.shipped_date = datetime.datetime.now()
        order.status = Order.SHIPPED
        order.save()
    return
admin_order_shipped.short_description = 'Set shipped'


# Show ordered products in admin page
class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


# Sorting features
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', order_name, 'status', 'created_at']
    list_filter = ['created_at', 'status']
    search_fields = ['first_name', 'address', 'id']
    inlines = [OrderItemInLine]
    actions = [admin_order_shipped]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
