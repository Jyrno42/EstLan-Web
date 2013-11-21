Deploy guide
============

To deploy:

- Checkout source code to /srv/EstLan
- Create virtualenv 'venv' and install production requirements

- Create EstLan/media/ dir and ensure it's writable by server process (usually this means www-data user)
- Create database and user
- Add local settings
- syncdb, migrate, collectstatic

- Copy gunicorn.conf to /etc/init/gunicorn-EstLan.conf
- Copy nginx.conf to /etc/nginx/sites-enabled/EstLan.conf
- start the service and reload nginx


Files in this directory:

- gunicorn.conf - upstart script to start the gunicorn server process.
- nginx.conf - Nginx site configuration
