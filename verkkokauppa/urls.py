"""verkkokauppa URL Configuration"""

from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from apps.cart.views import cart_detail
from apps.core.views import frontpage, contact, about
from apps.store.views import product_detail, category_detail

from apps.store.api import api_add_to_cart, api_remove_from_cart

urlpatterns = [

    # Site Pages
    path('', frontpage, name='frontpage'),  # Store frontpage
    path('cart/', cart_detail, name='cart'),  # Shopping cart page
    path('contact/', contact, name='contact'),  # Contact page
    path('about/', about, name='about'),  # About page

    # Admin Page
    path('admin/', admin.site.urls),  # Site Django admin page

    # API
    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),  # Add product to cart API functionality
    path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),  # Remove product from cart API functionality


    # Store Pages
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),  # Product detail page
    path('<slug:slug>/', category_detail, name='category_detail'),  # Category detail page (type slug, name slug)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Fix media directory
