rm /etc/systemd/system/github_calendar.service
echo -e "[Unit]\nDescription=Gunicorn instance to serve Github-Calendar\nAfter=network.target\n\n[Service]\nUser=root\nGroup=www-data\nWorkingDirectory=/home/Github-Calendar\nEnvironment=\"PATH=/home/Github-Calendar/env/bin\"\nExecStart=/home/Github-Calendar/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app\n\n[Install]\nWantedBy=multi-user.target" >> /etc/systemd/system/github_calendar.service
systemctl start github_calendar
systemctl enable github_calendar
rm /etc/nginx/sites-available/github_calendar
echo -e "server {\n    listen 80;\n    server_name 137.184.84.145 appacademycoaches.com www.appacademycoaches.com;\n\n    location / {\n        include proxy_params;\n        proxy_pass http://unix:/home/Github-Calendar/app.sock;\n    }\n}" >> /etc/nginx/sites-available/github_calendar
systemctl daemon-reload
