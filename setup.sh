chmod 0755 /home/Github-Calendar
rm /etc/systemd/system/github_calendar.service
rm /etc/systemd/system/multi-user.target.wants/github_calendar.service
printf "[Unit]\nDescription=Gunicorn instance to serve Github-Calendar\nAfter=network.target\n\n[Service]\nUser=root\nGroup=www-data\nWorkingDirectory=/home/Github-Calendar\nEnvironment=\"PATH=/home/Github-Calendar/env/bin\"\nExecStart=/home/Github-Calendar/bin/gunicorn --workers 3 --bind unix:github_calendar.sock -m 007 wsgi:app\n\n[Install]\nWantedBy=multi-user.target" >> /etc/systemd/system/github_calendar.service
rm /etc/systemd/system/multi-user.target.wants/github_calendar.service
systemctl start github_calendar
systemctl enable github_calendar
systemctl daemon-reload
systemctl status github_calendar