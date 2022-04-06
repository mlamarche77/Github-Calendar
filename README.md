# Github-Calendar


## Config File
In the static folder create a file called ```config.json``` with the following in it:
```json
{
  "updates": "",
  "password": "aacoaches",
  "github_api_key": "YOUR-GITHUB-API-TOKEN",
  "github_username": "mlamarche77"
}
```
Note: leave "updates" with a blank.


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
root@ubuntu:~# apt update
root@ubuntu:~# apt upgrade
root@ubuntu:~# apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
root@ubuntu:~# apt install python3-venv nginx
root@ubuntu:~# apt install git curl build-essential
root@ubuntu:~# pip3 install wheel gunicorn flask matplotlib numpy requests pandas
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
root@ubuntu:~# cd /home/Github-Calendar
root@ubuntu:~# python3 -m venv env
root@ubuntu:~# source env/bin/activate
(env):~# pip3 install wheel gunicorn flask matplotlib numpy requests pandas
(env):~# deactivate 
```
4. Configure the project
```shell
root@ubuntu:~# vi /home/Github-Calendar/static/config.json
```
Enter the following into the editor
```json
{
  "updates": "",
  "password": "aacoaches",
  "github_api_key": "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",
  "github_username": "mlamarche77"
}
```

Write and Exit the editor
```shell
press ESC
press shift + :
type wq
press enter
```


5. Add the HTTP service

root@ubuntu:~# 
root@ubuntu:~# 
root@ubuntu:~# 
root@ubuntu:~# 
root@ubuntu:~# 
root@ubuntu:~# 
 
```