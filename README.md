# Verkkokauppa using Django

### Description

A simple verkkokauppa made in Django, using Vue.js/Vuex, AJAX and a background API and Bulma .css framework. This project was done as part of a job interview for FNS.
The project was almost entirely written by hand and designed from the ground up to incorporate best practices.

Time taken: Approx 5½ hours incl. testing, diagrams, readme explanation, deploying to production server and setting up domain and SSL etc.

### FAQ

Q: What technologies did you use?
A: Python/Django, Vue.js for ajax and the cart logic, Vuex to store the quantity of items in the cart (outside of a variable), Bulma to handle the .css, JSonResponse as a serializer to convert data to json and MariaDB (HeidiSQL frontend) to handle the database. Linode handles the server, with ufw and SSL (Certbot) for security and Nginx for displaying and GUnicorn for serving the webpage.

Q: Why did you use Vue.js and not React or Angular?
A: It plays nicer with Django, allows building business logic into the verkkokauppa from the beginning and scales far more easily for business related projects anyway.
I'm far faster at splitting sites into reusable components with Vue.js and it means I don't have to waste literally hours of my life updating each page manually. I've started using Vue.js for anything I used React for earlier. FWIW: I've barely touched Angular and its global interest has been decreasing for soem time anyway.

Q: Why did you use Bulma for CSS?
A: Because everyone should be using it. I'm not much of a frontend person, so if I can let Bulma take care of that then all the better.

Q: Why did you use MariaDB?
A: I'm not much of a fan of Oracle's software and HeidiSQL has a dark theme.

Q: How did you do the "design?"
A: It's just a simple bootstrap. Work was obviously focused elsewhere. I added all the containers, elements and so on and set up the logic for the data that moves between them (aka, the backend). It looks simple because it should be.



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
5. Create a superuser to access admin page and add products to site ```python manage.py createsuperuser```
6. Start the app ```python manage.py runserver```

Open a browser and visit http://localhost:8000/

### Database

This application is set up to use a MySQL/MariaDB server, and a database called "verkkokauppa" running on the same machine. NOT sqlite3
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
Project is then storing database data inside an sqlite3 file in the root directory

Open a browser and visit http://localhost:8000/