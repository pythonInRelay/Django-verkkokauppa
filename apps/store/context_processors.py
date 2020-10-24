from .models import Category


# Add new categories to base.html automatically
def menu_categories(request):
    categories = Category.objects.all()  # Show all of them

    return {'menu_categories': categories}
