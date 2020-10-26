# Verkkokauppa using Django

### Description

A simple verkkokauppa made in Django, using Vue.js/Vuex, AJAX and a background API and Bulma .css framework. This project was done as part of a job interview for FNS.
The project was almost entirely written by hand and designed from the ground up to incorporate best practices. The design works on mobile devices also.

Time taken: Approx 5½ hours incl. testing, diagrams, readme explanation, deploying to production server, payment integration and setting up domain and SSL etc.

______________________________________

### FAQ

Q: What technologies did you use?

A: *Quite a few by the end...*

* Python/Django
* Vue.js for ajax and the cart logic
* Vuex to store the quantity of items in the cart (outside of a variable)
* Bulma to handle the .css
* JSonResponse as a serializer to convert data to json and MariaDB (HeidiSQL frontend) to handle the database.
* Unraid (Slackware) to test the first deployment in a VM with LetsEncrypt and DyDNS (reverse proxy)
* Linode to host the project
* ufw, and SSL (Certbot) for security
* Nginx for displaying and GUnicorn for serving the webpage.
* Stripe handles the payment and currency conversion via their API

______________________________________

Q: Why did you use Vue.js and not React or Angular?
A: It plays nicer with Django, allows building business logic into the verkkokauppa from the beginning and scales far more easily for business related projects anyway.
I'm far faster at splitting sites into reusable components with Vue.js and it means I don't have to waste literally hours of my life updating each page manually. I've started using Vue.js for anything I used React for earlier. FWIW: I've barely touched Angular and its global interest has been decreasing for soem time anyway.

Q: Why did you use Bulma for CSS?

A: Because everyone should be using it. I'm not much of a frontend person, so if I can let Bulma take care of that then all the better.

Q: Why did you use MariaDB?

A: I'm not much of a fan of Oracle's software and HeidiSQL has a dark theme.

Q: Why did you use Stripe for payment, and why doesn't it work when I build the source code?

A: I used it because Stripe is amazing. It doesn't work because you need to make your own account and use your own keys.
Ensure that you have at the minimum, a test business name and add your keys in the settings.py and secrets.py where directed.

Q: How did you do the "design?"

A: It's just a simple bootstrap. Work was obviously focused elsewhere. I added all the containers, elements and so on and set up the logic for the data that moves between them (aka, the backend). It looks simple because it should be. Anywhere I didn't have to reinvent the wheel, I didn't.

Q: Can I use your source to continue building my own site?

A: Of course.

Q: Could I charge people for this?

A: Check the LICENSE.md

### Improvements I'd make if I did this project again
1. Auto generate random int for each new product ID
2. User accounts and reviews
3. Newsletter
4. PDF Receipts
5. Prettier front-end

______________________________________

Application requirements:

* asgiref==3.2.10  # https://asgi.readthedocs.io/en/latest/
* Django==3.1.2
* mysqlclient==2.0.1  # Necessary if user is using their locally installed MySQL server database to read/write to DB
* Pillow==8.0.1  # Necessary for image viewing and zooming
* pytz==2020.1  # Cross-platform timezone
* sqlparse==0.4.1  # Necessary for multiline SQL statements and migrations

______________________________________

## Local machine installation instructions

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

## Server installation instructions

Here's how to install this site from scratch (clean Ubuntu 20.04.1 LTS)

1. Use Debian or Ubuntu or something
2. Make a new usergroup, user and home dir for that user
3. ```apt get update && apt upgrade -y```
4. ```apt install python3 python3-virtualenv libmysqlclient-dev```
5. ```virtualenv venv```
6. ```cd env```
7. ```source bin/activate```
8. ```pip install -r requirements.txt```
9. ```mkdir logs```
10. ```chown -R <user_you_created>:<group_you_created> .```
11. ```git clone https://github.com/pythonInRelay/Django-verkkokauppa.git```
12. ```cd Django-verkkokauppa```
13. ```sudo apt install mariadb-server```
14. ```sudo systemctl status mariadb```
15. ```sudo mysql_secure_installation```
16. ```Set up root password for MySQL```
17. ```sudo mysql -u root -p```
18. Enter root password
19. ```CREATE DATABASE verkkokauppa;```
20. ```SHOW DATABASES;```
21. Confirm that the **verkkokauppa** database exists
22. ```quit```
23. ```python manage.py makemigrations```
24. ```python manage.py migrate```
25. ```python manage.py createsuperuser```
26. ```ifconfig```
27. Take note of your IPv4 address
28. ```cd verkkokauppa```
29. ```nano settings.py```
30. ```ALLOWED_HOSTS = ['<yourserverip>']```
31. Save and exit the file
32. ```cd ..```
33. ```python manage.py runserver <yourserverip:8001>```
34. In a browser go to <yourserverip:8001>/admin and login

You now have the site set up with an account that has admin access.
Use the user you created on the machine for SSH access in the future and create another non-root user in the admin page.

______________________________________