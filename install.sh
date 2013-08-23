#!/bin/bash

# -----------------------------------------------------
# Config Vars
# -----------------------------------------------------

PROJECT_NAME=EstLan
VENV_DIR=venv
INSTALL_DIR=/srv/estlan
USERNAME=ubuntu
USERGROUP=ubuntu
DOMAIN=estlan.eu
PORT=9001

# -----------------------------------------------------
# Ability to change $PROJECT_NAME
# -----------------------------------------------------

echo -n "Enter Project Name [$PROJECT_NAME]: "
read input1

PROJECT_NAME=${input1:-$PROJECT_NAME}

echo "Project: $PROJECT_NAME"

# -----------------------------------------------------
# Ability to change $INSTALL_DIR
# -----------------------------------------------------

echo -n "Enter Install Dir [$INSTALL_DIR]: "
read input2

INSTALL_DIR=${input2:-$INSTALL_DIR}

echo "Installation directory: $INSTALL_DIR"

# -----------------------------------------------------
# Ability to change $USERNAME
# -----------------------------------------------------

echo -n "Enter Username [$USERNAME]: "
read input3

USERNAME=${input3:-$USERNAME}

echo "Username: $USERNAME"

# -----------------------------------------------------
# Ability to change $USERGROUP
# -----------------------------------------------------

echo -n "Enter Usergroup [$USERGROUP]: "
read input4

USERNAME=${input4:-$USERGROUP}

echo "Usergroup: $USERGROUP"

# -----------------------------------------------------
# Ability to change $DOMAIN
# -----------------------------------------------------

echo -n "Enter Domain [$DOMAIN]: "
read input5

DOMAIN=${input5:-$DOMAIN}

echo "Domain: $DOMAIN"

# -----------------------------------------------------
# Ability to change $PORT
# -----------------------------------------------------

echo -n "Enter Port [$PORT]: "
read input6

PORT=${input6:-$PORT}

echo "Port: $PORT"

# -----------------------------------------------------
# cd $INSTALL_DIR
# -----------------------------------------------------

echo "-----------------------------------------------------"
echo "Begin Install"
echo "-----------------------------------------------------"
cd $INSTALL_DIR
mkdir -p $INSTALL_DIR/log

# -----------------------------------------------------
# INSTALL PACKAGES
# -----------------------------------------------------

echo -n "* Installing setuptools, virtualenv, pip, libjpeg and libpng...   "
apt-get update >/dev/null && apt-get install python-setuptools python-virtualenv python-pip libjpeg-dev libpng-dev nginx -y >/dev/null
echo "Done."

# -----------------------------------------------------
# Creating venv
# -----------------------------------------------------

if [ -f $INSTALL_DIR/$VENV_DIR/bin/activate ];
then
   echo "* Found virtual environment...   Done."
else
    echo -n "* Creating virtual environment...   "
    virtualenv --system-site-packages $INSTALL_DIR/$VENV_DIR >/dev/null
    echo "Done."
fi

# -----------------------------------------------------
# Create update script
# -----------------------------------------------------

echo -n "* Creating update script...   " 
echo "# Update script" > $INSTALL_DIR/update.sh
echo "service $PROJECT_NAME stop" >> $INSTALL_DIR/update.sh
echo ". ./venv/bin/activate" >> $INSTALL_DIR/update.sh
echo "cd $PROJECT_NAME" >> $INSTALL_DIR/update.sh
echo "python manage.py migrate" >> $INSTALL_DIR/update.sh
echo "python manage.py compilemessages" >> $INSTALL_DIR/update.sh
echo "service $PROJECT_NAME start" >> $INSTALL_DIR/update.sh
chmod +x $INSTALL_DIR/update.sh
echo "Done."

# -----------------------------------------------------
# Create start script
# -----------------------------------------------------

echo -n "* Creating update script...   " 

echo "#!/bin/bash" > $INSTALL_DIR/start.sh
echo "cd $INSTALL_DIR" >> $INSTALL_DIR/start.sh
echo ". ./venv/bin/activate" >> $INSTALL_DIR/start.sh
echo "cd $PROJECT_NAME" >> $INSTALL_DIR/start.sh
echo "exec gunicorn --workers=3 -t 30 --log-level debug --log-file $INSTALL_DIR/log/server.log -b 0.0.0.0:$PORT --user=$USERNAME --group=$USERGROUP $PROJECT_NAME.wsgi:application >> $INSTALL_DIR/log/gunicorn.log" >> $INSTALL_DIR/start.sh
chmod +x $INSTALL_DIR/update.sh
echo "Done."

# -----------------------------------------------------
# Create nginx conf
# -----------------------------------------------------

echo -n "* Creating nginx conf...   " 

echo "server {" > /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    listen         80;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    server_name    $DOMAIN;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    root $INSTALL_DIR/$PROJECT_NAME;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    location /media/ {" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    }" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    location /static/ {" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    }" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    location /robots.txt {" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "        alias $INSTALL_DIR/$PROJECT_NAME/static/robots.txt;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    }" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    ## Deny illegal Host headers" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    if ($host !~* ^($DOMAIN)$ ) {" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "        return 444;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    }" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    location / {" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "        proxy_read_timeout      30s;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "        proxy_pass              http://127.0.0.1:$PORT;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "        proxy_set_header        Host                 $host;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "        proxy_set_header        User-Agent           $http_user_agent;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "        proxy_set_header        X-Real-IP            $remote_addr;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "        #auth_basic 'Restricted';" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "        #auth_basic_user_file $INSTALL_DIR/$PROJECT_NAME/.htpasswd;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    }" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "    error_page 500 502 503 504 /media/50x.html;" >> /etc/nginx/conf.d/$PROJECT_NAME.conf
echo "}" >> /etc/nginx/conf.d/$PROJECT_NAME.conf

echo "Done."

# -----------------------------------------------------
# Create upstart job
# -----------------------------------------------------

echo -n "* Creating upstart job...   " 

echo "description 'start and stop the $PROJECT_NAME server'" > /etc/init/$PROJECT_NAME.conf
echo "start on runlevel [2345]" >> /etc/init/$PROJECT_NAME.conf
echo "stop on runlevel [!2345]" >> /etc/init/$PROJECT_NAME.conf
echo "respawn" >> /etc/init/$PROJECT_NAME.conf
echo "respawn limit 10 5" >> /etc/init/$PROJECT_NAME.conf
echo "exec $INSTALL_DIR/start.sh" >> /etc/init/$PROJECT_NAME.conf

echo "Done."

# -----------------------------------------------------
# Chown & Chmod
# -----------------------------------------------------

echo -n "* Setting files owner($USERNAME:$USERGROUP) and permissions...   "
chown -R $USERNAME:$USERGROUP $INSTALL_DIR
chmod -R 0700 $INSTALL_DIR
echo "Done."

# -----------------------------------------------------
# Git Pull
# -----------------------------------------------------

echo -n "* Updating repository...   "
git pull >/dev/null
echo "Done."

# -----------------------------------------------------
# Update dependencies
# -----------------------------------------------------

echo -n "* Installing dependencies...   " 
source $INSTALL_DIR/$VENV_DIR/bin/activate && pip install -r requirements.txt >/dev/null
echo "Done."

# -----------------------------------------------------
# Create DB
# -----------------------------------------------------

echo -n "* Creating database...   " 
cd $PROJECT_NAME
python manage.py syncdb >/dev/null
echo "Done."

# Reload nginx
# start service

echo "-----------------------------------------------------"
echo " "
echo "* Everything complete, installed $PROJECT_NAME. Use service $PROJECT_NAME start to run server."