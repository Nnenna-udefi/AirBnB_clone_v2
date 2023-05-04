#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

# install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get update
    sudo apt-get install -y nginx
fi
# create the folders
sudo mkdir -p /data/web_static/shared /data/web_static/releases/test /data/web_static/current
# create a fake html file
sudo echo '<html><title>Test page</title><body><p>Welcome to Nginx test page</p></body></html>' | sudo tee /data/web_static/releases/test/index.html
# create a symbolic link
sudo ln -sf /data/web_static/current /data/web_static/releases/test/
# Give ownership of the /data/ folder to the ubuntu user
sudo chown -R ubuntu:ubuntu /data/
sudo chgrp -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    
    location /redirect_me {
        return 301 https://google.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" | sudo tee /etc/nginx/sites-available/default

# restart nginx
sudo service nginx restart
