chmod 0755 /home/Github-Calendar
systemctl stop github_calendar.service
systemctl daemon-reload
rm /etc/systemd/system/github_calendar.service
rm /etc/systemd/system/multi-user.target.wants/github_calendar.service
systemctl daemon-reload
printf "[Unit]\nDescription=Gunicorn instance to serve Github-Calendar\nAfter=network.target\n\n[Service]\nUser=root\nGroup=www-data\nWorkingDirectory=/home/Github-Calendar\nEnvironment=\"PATH=/home/Github-Calendar/env/bin\"\nExecStart=/home/Github-Calendar/env/bin/gunicorn --workers 3 --bind unix:github_calendar.sock -m 007 wsgi:app\n\n[Install]\nWantedBy=multi-user.target" >> /etc/systemd/system/github_calendar.service
rm /etc/systemd/system/multi-user.target.wants/github_calendar.service
systemctl start github_calendar
systemctl enable github_calendar
systemctl daemon-reload
rm /etc/nginx/sites-available/github_calendar
rm /etc/nginx/sites-enabled/github_calendar
printf "server {\n    listen 80;\n    server_name 137.184.84.145 appacademycoaches.com www.appacademycoaches.com;\n\n    location / {\n        include proxy_params;\n        proxy_pass http://unix:/home/Github-Calendar/github_calendar.sock;\n    }\n}" >> /etc/nginx/sites-available/github_calendar
systemctl status github_calendar
reboot
