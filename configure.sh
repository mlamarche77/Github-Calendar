ln -s /etc/nginx/sites-available/github_calendar /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx
ufw allow 'Nginx Full'