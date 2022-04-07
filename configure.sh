ln -s /etc/nginx/sites-available/github_calendar /etc/nginx/sites-enabled
systemctl restart nginx
ufw allow 'Nginx Full'