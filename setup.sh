sudo chmod 0755 /home/Github-Calendar
sudo systemctl stop github_calendar.service
sudo systemctl daemon-reload
sudo rm /etc/systemd/system/github_calendar.service
sudo rm /etc/systemd/system/multi-user.target.wants/github_calendar.service
sudo systemctl daemon-reload
sudo bash -c 'echo -e "[Unit]\nDescription=Gunicorn instance to serve Github-Calendar\nAfter=network.target\n\n[Service]\nUser=root\nGroup=www-data\nWorkingDirectory=/home/Github-Calendar\nEnvironment=\"PATH=/home/Github-Calendar/env/bin\"\nExecStart=/home/Github-Calendar/env/bin/gunicorn --workers 3 --bind unix:github_calendar.sock -m 007 wsgi:app\n\n[Install]\nWantedBy=multi-user.target" > /etc/systemd/system/github_calendar.service'
sudo rm /etc/systemd/system/multi-user.target.wants/github_calendar.service
sudo systemctl start github_calendar
sudo systemctl enable github_calendar
sudo systemctl daemon-reload
sudo rm /etc/nginx/sites-available/github_calendar
sudo rm /etc/nginx/sites-enabled/github_calendar
sudo bash -c 'echo -e "server {\n    listen 80;\n    listen [::]:80;\n    server_name 137.184.84.145 appacademycoaches.com www.appacademycoaches.com;\n\n    location / {\n        include proxy_params;\n        proxy_pass http://unix:/home/Github-Calendar/github_calendar.sock;\n    }\n}" > /etc/nginx/sites-available/github_calendar'
sudo reboot
