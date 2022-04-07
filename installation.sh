apt update
apt upgrade
apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
apt install python3-venv nginx
apt install git curl build-essential python3-certbot-nginx
pip3 install wheel gunicorn flask matplotlib numpy requests pandas
pip install wheel gunicorn flask matplotlib numpy requests pandas
apt autoremove
python3 -m venv /home/Github-Calendar/env
source /home/Github-Calendar/env/bin/activate
pip3 install wheel gunicorn flask matplotlib numpy requests pandas
pip install wheel gunicorn flask matplotlib numpy requests pandas
deactivate
