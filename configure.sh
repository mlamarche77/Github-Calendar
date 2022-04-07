sudo ln -s /etc/nginx/sites-available/github_calendar /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo reboot
