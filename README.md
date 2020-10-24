# Verkkokauppa using Django

### Description

A simple verkkokauppa made in Django

Frontend template is a free bootstrap4 ecommerce template. In this case bootstrap4 does not need to be installed.

Application requirements:

* asgiref==3.2.10  # https://asgi.readthedocs.io/en/latest/
* Django==3.1.2
* mysqlclient==2.0.1  # Necessary if user is using their locally installed MySQL server database to read/write to DB
* Pillow==8.0.1  # Necessary for image viewing and zooming
* pytz==2020.1  # Cross-platform timezone
* sqlparse==0.4.1  # Necessary for multiline SQL statements and migrations

## Usage instructions

1. Ensure Python3 and pip are installed (I use a venv in PyCharm)
2. Run ```python pip install -r requirements.txt```
3. Run ```python manage.py makemigrations```
4. Run ```python manage.py migrate```
5. Create a superuser ```python manage.py createsuperuser```
6. Start the app ```python manage.py runserver```

Open a browser and visit http://localhost:8000/

### Database

This application is set up to use a MySQL/MariaDB server running on the same machine. NOT sqlite3
______________________________________

To change the database back to sqlite3 change the DATABASES array in verkkokauppa/settings.py to:

```DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Then repeat above steps 3 and 4.

Open a browser and visit http://localhost:8000/