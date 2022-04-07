# Github-Calendar

## Create a Droplet

### 1. Sign into DigitalOcean.
### 2. On the left hand panel click on Droplets
### 3. Click create Droplet
### 4. Choose these configurations

| Name               | Plan                                              |
|--------------------|---------------------------------------------------|
| Distributions      | Ubuntu 20.04                                      |
| Plan               | Basic                                             |
| CPU Options        | Regular with SSD                                  |
| Data Center Region | Any of preference (closer to audience the better) |

### 5. On the left hand panel click on Droplets again
### 6. Click on your droplet
### 7. Click on Networking
### 8. Edit Firewalls
### 9. Create a Firewall called AppAcademyCoachesFirewall 

#### Inbound Rules
| Type   | Plan | Port Range | Plan              |
|--------|------|------------|-------------------|
| SSH    | TCP  | 22         | All IPv4 All IPv6 |
| HTTP   | TCP  | 80         | All IPv4 All IPv6 |
| HTTPS  | TCP  | 433        | All IPv4 All IPv6 |
| Custom | TCP  | 5000       | All IPv4 All IPv6 |
| Custom | TCP  | 5001       | All IPv4 All IPv6 |

#### Outbound Rules
| Type    | Plan | Port Range | Plan              |
|---------|------|------------|-------------------|
| ICMP    | ICMP |            | All IPv4 All IPv6 |
| All TCP | TCP  | All ports  | All IPv4 All IPv6 |
| All UDP | UDP  | All ports  | All IPv4 All IPv6 |


#### Apply the firewall to the droplet
Search for Droplet or tag: appacademycoaches

#### Click Create Firewall


## Config File

If you need to change the password or other keys, in the Github static folder you can edit a file called ```config.json``` with the following in it:

```json
{
  "updates": "",
  "password": "aacoaches",
  "github_api_key": "YOUR-GITHUB-API-TOKEN",
  "github_username": "mlamarche77"
}
```

Note: leave "updates" with a blank. The program will update it when it receives a file.

The file is located [here](https://github.com/mlamarche77/Github-Calendar/blob/main/static/config.json)

To edit click on the pencil icon to change the data. Then commit your changes.

## Github API Token

on your github settings 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> developer settings (last option)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> personal access tokens

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> generate new token 

Expire the token: no expiration 
   

| Checkbox                              |
|---------------------------------------|
| <ul><li>[x] repo</li></ul>            |
| <ul><li>[x] read:org</li></ul>        |
| <ul><li>[x] read:public_key</li></ul> |
| <ul><li>[x] read:repo_hook</li></ul>  |
| <ul><li>[x] user</li></ul>            |
| <ul><li>[x] read:gpg:key</li></ul>    |

Then generate the token.

## Hosting the project on your own

1. Log into Digital Ocean
2. Click on Droplets on the left hand panel
3. Click on your droplet: appacademycoaches
4. Click on Console
5. In the console/terminal type in the commands to install programs that run the project

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
> Your username above for the command "git clone" is your GitHub username
> 
> Your password above for the command "git clone" is your GitHub api key


3. Setup the project settings

```shell
root@ubuntu:~# sh /home/Github-Calendar/installation.sh
root@ubuntu:~# source /home/Github-Calendar/env/bin/activate
(env):~# pip3 install wheel gunicorn flask matplotlib numpy requests pandas
(env):~# pip install wheel gunicorn flask matplotlib numpy requests pandas
(env):~# deactivate 
```

5. Start the service which will run the app indefinitely in the background or whenever the computer gets restarted. The system will reboot at the end of the installation.

```shell
root@ubuntu:~# sh /home/Github-Calendar/setup.sh
```

Log back into the console/terminal.

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

To exit press
```shell
press CTRL + C
press CTRL + C
press CTRL + C
```

8. Proxy the requests: the service which connects a url to the program

Find your IP Address at your droplet account. It's labeled as ipv4.

- sign in to DigitalOcean
- On the left side menu click on Droplets
- Select the droplet for this project
- Copy the ipv4 ip address

[IPV4_ADDRESS] = 137.184.84.145

The IPV4 address will need to be pasted into the editor with the boiler plate code. Replace the IP address below with
your IPV4 address:

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

Enable the configuration you just pasted. The system will reboot again.

```shell
root@ubuntu:~# sh /home/Github-Calendar/configure.sh
```

9. Go to Domain.com
10. On the left hand panel click on Pointers & Subdomains
11. Change Pointer Type and Directory

| Pointer Type | Directory              |
|--------------|------------------------|
| URL Stealth  | http://137.184.84.145  | <- The IPv4 address of your Droplet 

14. On your browser type in the url. If you access the website with: www.appacademycoaches.com in your browser, move to the next step. Otherwise, wait until the domain registers the IP address. It can take an hour sometimes or even a day.

15. Add a certificate to your website. Go back to the terminal/console.

You can only use this command up to 5 times total within 7 days. Otherwise, it will lock you out.

Choose:

- No redirects

```shell
root@ubuntu:~# certbot --nginx -d appacademycoaches.com -d www.appacademycoaches.com
```

Reboot your system

```shell
root@ubuntu:~# reboot 
```


If anything isn't working. It's likely a step was missed. Start all over again until changes are reflected.
Here are some commands you can type whenever you want to reboot the internals.

```shell
root@ubuntu:~# chmod 0755 /home/Github-Calendar
root@ubuntu:~# systemctl restart github_calendar
root@ubuntu:~# systemctl daemon-reload
root@ubuntu:~# systemctl restart nginx
root@ubuntu:~# ufw allow 'Nginx Full'
```