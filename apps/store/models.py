from django.db import models


# Set relevant database tables
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    # Set correct plural spelling
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)  # Tuple of category order number

    # Add category name in Admin panel
    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)  # Del product table also
    product_id = models.IntegerField()  # UPDATE THIS LATER
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    is_featured = models.BooleanField(default=False)  # Is the product a featured product? (Displays on frontpage)
    date_added = models.DateTimeField(auto_now_add=True)  # Add time of added product to DB

    class Meta:
        ordering = ('-date_added',)  # Sort by newest product added

    # Add product name in Admin panel
    def __str__(self):
        return self.title
