### Production server install instructions

These are all the steps I took to get this website set up on my production server. There are a lot of them and it requires running a lot of code for everything to work. If you get an error, search for info about it in Google. You will need to make minor changes yourself for everything to work.

Here's how to install this site from scratch (clean Ubuntu 20.04.1 LTS)

1. Use Debian or Ubuntu or something
2. Make a new usergroup, user and home dir for that user
3. ```apt get update && apt upgrade -y```
4. ```apt install python3 python3-virtualenv libmysqlclient-dev```
5. ```virtualenv venv```
6. ```cd env```
7. ```source bin/activate```
8. ```mkdir logs```
9. ```chown -R <user_you_created>:<group_you_created> .```
10. ```git clone https://github.com/pythonInRelay/Django-verkkokauppa.git```
11. ```cd Django-verkkokauppa```
12. ```sudo apt install mariadb-server```
13. ```sudo systemctl status mariadb```
14. ```sudo mysql_secure_installation```
15. ```Set up root password for MySQL```
16. ```sudo mysql -u root -p```
17. Enter root password
18. ```CREATE DATABASE verkkokauppa;```
19. ```SHOW DATABASES;```
20. Confirm that the **verkkokauppa** database exists
21. ```quit```
22. ```python manage.py makemigrations```
23. ```python manage.py migrate```
24. ```python manage.py createsuperuser```
25. ```ifconfig```
26. Take note of your IPv4 address
27. ```cd verkkokauppa```
28. ```nano settings.py```
29. ```ALLOWED_HOSTS = ['<yourserverip>']```
30. Save and exit the file
31. ```cd ..```
32. ```python manage.py runserver <yourserverip:8001>```
33. In a browser go to <yourserverip:8001>/admin and login

You now have the site set up with an account that has admin access.
Use the user you created on the machine for SSH access in the future and create another non-root user in the admin page.


Install ufw now.

1. ```ufw allow ssh```
2. ```ufw default deny incoming```
3. ```ufw default allow outgoing```
4. ```ufw allow 'Nginx Full'```
5. Your config should look like this:

```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere                  
Nginx HTTP                 ALLOW       Anywhere                  
OpenSSH (v6)               ALLOW       Anywhere (v6)             
Nginx HTTP (v6)            ALLOW       Anywhere (v6)
```

Now we switch to gunicorn becuase it's made for Django. We're then going to use Nginx to serve the images etc.

1. ```cp settings.py settingsprod.py``` this is to use with gunicorn in a production environment
2. ```nano /venv/bin/gunicorn_start```
3. Paste in the following and save (change the username and group to what you created in Linux):

```
#!/bin/sh

NAME='Django-verkkokauppa'
DJANGODIR=/daniel/venv/Django-verkkokauppa
SOCKFILE=/daniel/venv/Django-verkkokauppa/run/gunicorn.sock
USER=daniel
GROUP=webadmin
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=verkkokauppa.settingsprod
DJANGO_WSGI_MODULE=verkkokauppa.wsgi
TIMEOUT=120

cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-

```

4. ```chmod +x /venv/bin/gunicorn_start```
5. ```apt instsall supervisor```
6. ```cd /etc/supervisor/conf.d```
7. ```nano verkkokauppa.conf```
8. Paste in the following and save:

```
[program:verkkokauppa]
command = /<username>/venv/bin/gunicorn_start
user = <username>
stdout_logfile = /<username>/venv/logs/supervisor.log
redirect_stderr = true
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
```

9. ```supervisorctl reread```
10. ```supervisorctl update```
11. ```supervisorctl status``` check that the process is running
12. ```apt install nginx -y```
13. ```cd /etc/nginx/sites-available```
14. ```nano verkkokauppa.conf```
15. Paste in the following and save (change username and ip address as required)

```
upstream verkkokauppa_app_server {
	server unix:/<username>/venv/Django-verkkokauppa/run/gunicorn.sock fail_timeout=0;
}

server {
	listen 80;
	server_name <website_ip_address>;
	access_log /<username>/venv/logs/nginx-access.log;
	error_log /<username>/venv/logs/nginx-error.log;

	location /static/ {
		alias /<username>/venv/verkkokauppa/static/;
	}

	location /media/ {
		alias /<username>/venv/verkkokauppa/media/;
	}

	location / {
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

		proxy_set_header Host $http_host;

		proxy_redirect off;

		if (!-f $request_filename) {
			proxy_pass http://verkkokauppa_app_server;
		}
	}
}
```

16. ```cd ../sites-enabled/```
17. ```ln -s ../sites-available/Django-verkkokauppa.conf Django-verkkokauppa.conf```
18. ```service nginx restart```
19. ```cd Django-verkkokauppa```
19. ```chown -R <username>:<usergroup> .```
20. ```cd /venv/bin chown -R <username>:<usergroup> gunicorn_start```
21. ```supervisorctl restart verkkokauppa```

Reboot the server and you should be good to go. Any permissions or SQL related issues just change the necessary user permissions.