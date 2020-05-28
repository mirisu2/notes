#### Turn on authentication
```
sudo apt-get update
sudo apt-get install nginx apache2-utils

sudo htpasswd -c /etc/nginx/.htpasswd john

sudo nano /etc/nginx/sites-enabled/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location / {
        auth_basic "Restricted Content";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://192.168.198.101:5601;
    }
}
sudo systemctl restart nginx
```
