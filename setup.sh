rm /etc/systemd/system/github_calendar.service
printf "[Unit]\nDescription=Gunicorn instance to serve Github Calendar\nAfter=network.target\n\n[Service]\nUser=root\nGroup=www-data\nWorkingDirectory=/home/github_calendar\nEnvironment=\"PATH=/home/github_calendar/env/bin\"\nExecStart=/home/github_calendar/bin/gunicorn --workers 3 --bind unix:github_calendar.sock -m 007 wsgi:app\n\n[Install]\nWantedBy=multi-user.target" >> /etc/systemd/system/github_calendar.service
rm /etc/systemd/system/multi-user.target.wants/github_calendar.service
systemctl start github_calendar
systemctl enable github_calendar
systemctl daemon-reload
systemctl status github_calendar
rm /etc/nginx/sites-available/github_calendar
printf "server {\n    listen 80;\n    server_name 137.184.84.145 appacademycoaches.com www.appacademycoaches.com;\n\n    location / {\n        include proxy_params;\n        proxy_pass http://unix:/home/github_calendar/app.sock;\n    }\n}" >> /etc/nginx/sites-available/github_calendar
