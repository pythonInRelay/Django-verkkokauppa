from io import BytesIO  # For buffer
from django.core.files import File  # Needed to work with files
from django.db import models
from PIL import Image  # Python Image Library


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
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)  # Del product table also
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    product_id = models.IntegerField()
    is_featured = models.BooleanField(default=False)  # Is the product a featured product? (Displays on frontpage)

    image = models.ImageField(upload_to='uploads/', blank=True, null=True)  # Change upload DIR from root
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)  # Add time of added product to DB

    class Meta:
        ordering = ('-date_added',)  # Sort by newest product added

    # Add product name in Admin panel
    def __str__(self):
        return self.title

    # Override default save function to upload the image file and not template file
    def save(self, *args, **kwargs):
        print('Save', self.image.path)
        self.thumbnail = self.make_thumbnail(self.image)

        # When saving in admin page this function is called and a thumbnail with the below settings is returned
        super().save(*args, *kwargs)

    # Set options for thumbnail

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()  # Create BytesIO object
        img.save(thumb_io, 'JPEG', quality=85)

        # Create Django friendly file object
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
