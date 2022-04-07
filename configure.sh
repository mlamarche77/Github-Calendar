rm /etc/nginx/sites-available/github_calendar
rm /etc/nginx/sites-enabled/github_calendar
printf "server {\n    listen 80;\n    server_name 137.184.84.145 appacademycoaches.com www.appacademycoaches.com;\n\n    location / {\n        include proxy_params;\n        proxy_pass http://unix:/home/Github-Calendar/github_calendar.sock;\n    }\n}" >> /etc/nginx/sites-available/github_calendar
ln -s /etc/nginx/sites-available/github_calendar /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx
ufw allow 'Nginx Full'