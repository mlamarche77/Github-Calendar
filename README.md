# Github-Calendar


## Config File
In the static folder you can edit a file called ```config.json``` with the following in it:
```json
{
  "updates": "",
  "password": "aacoaches",
  "github_api_key": "YOUR-GITHUB-API-TOKEN",
  "github_username": "mlamarche77"
}
```
Note: leave "updates" with a blank. The program will update it when it receives a file.


## Github API Token

on your github settings -> developer settings (last option) -> personal access tokens -> generate new token
Expire the token: no expiration
Click on the checkboxes:
repo
read:org
read:public_key
read:repo_hook
user
read:gpg:key

Then generate the token.


## Creating the project on your own

1. Log into the terminal on digital ocean and type in the commands to install programs to run the project
```shell
root@ubuntu:~# apt install git curl
```

2. Type in the commands to download the project
```shell
root@ubuntu:~# cd /home
root@ubuntu:~# git clone https://github.com/mlamarche77/Github-Calendar.git
Username:~#: mlamarche77
Password:~# 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
```
3. Setup the project settings
```shell
root@ubuntu:~# sh /home/Github-Calendar/installation.sh
root@ubuntu:~# source /home/Github-Calendar/env/bin/activate
(env):~# pip3 install wheel gunicorn flask matplotlib numpy requests pandas
(env):~# pip install wheel gunicorn flask matplotlib numpy requests pandas
(env):~# deactivate 
```

5. Start the service which will run the app indefinitely in the background or whenever the computer gets restarted

Start the service
```shell
root@ubuntu:~# sh /home/Github-Calendar/setup.sh
```

Check the status to make sure it was installed correctly.
```shell
root@ubuntu:~# systemctl status github_calendar
```

Output should look like this:
```text
● myproject.service - Gunicorn instance to serve myproject
     Loaded: loaded (/etc/systemd/system/myproject.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2020-05-20 14:15:18 UTC; 1s ago
   Main PID: 46430 (gunicorn)
      Tasks: 4 (limit: 2344)
     Memory: 51.3M
     CGroup: /system.slice/myproject.service
             ├─46430 /home/sammy/myproject/myprojectenv/bin/python3 /home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app
             ├─46449 /home/sammy/myproject/myprojectenv/bin/python3 /home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app
             ├─46450 /home/sammy/myproject/myprojectenv/bin/python3 /home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app
             └─46451 /home/sammy/myproject/myprojectenv/bin/python3 /home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app
```


8. Proxy the requests: the service which connects a url to the program

Find your IP Address at your droplet account. It's labeled as ipv4.
- sign in to DigitalOcean
- On the left side menu click on Droplets
- Select the droplet for this project
- Copy the ipv4 ip address

\[IPV4_ADDRESS] = 137.184.84.145

The IPV4 address will need to be pasted into the editor with the boiler plate code. Replace the IP address below with your IPV4 address:
```shell
root@ubuntu:~# vi /etc/nginx/sites-available/github_calendar
```

```text
server {
    listen 80;
    server_name 137.184.84.145 appacademycoaches.com www.appacademycoaches.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/Github-Calendar/app.sock;
    }
}
```

Write and Exit the editor
```shell
press ESC
press shift + :
type wq
press enter
```

Enable the configuration you just pasted
```shell
root@ubuntu:~# sh /home/Github-Calendar/configure.sh
```

The following will add a certificate to your project. You can only use this 
command up to 5 times total within 7 days. Otherwise, it will lock you out.

Choose:
- No redirects
```shell
root@ubuntu:~# certbot --nginx -d appacademycoaches.com -d www.appacademycoaches.com 
```


Reboot your system
```shell
root@ubuntu:~# reboot 
```