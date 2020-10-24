"""verkkokauppa URL Configuration"""

from django.contrib import admin
from django.urls import path

from apps.core.views import frontpage, contact
from apps.store.views import product_detail, category_detail

urlpatterns = [
    path('', frontpage, name='frontpage'),  # Store frontpage
    path('contact/', contact, name='contact'),  # Contact page
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),  # Product detail page
    path('<slug:slug>/', category_detail, name='category_detail'),  # Category detail page (type slug, name slug)
    path('admin/', admin.site.urls),  # Site Django admin page
]
