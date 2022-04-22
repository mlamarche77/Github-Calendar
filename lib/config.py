from datetime import datetime
from pathlib import Path
import json


def github_api_key():
    path = Path.cwd() / Path('static') / Path('config.json')
    assert path.exists(), f"File doesn't exist: {path}"
    try:
        with open(path, 'r') as r:
            config = json.load(r)
            return config['github_api_key']
    except Exception:
        if not path.exists():
            print(f'\033[93mWarning: {path} is not found in current working directory.\033[0m')
            print('\033[34mCreate the file and paste your GitHub API token to use GitHubs GraphQL API.\033[0m')


def is_password(password):
    path = Path.cwd() / Path('static') / Path('config.json')
    if not path.exists():
        raise FileNotFoundError("Can't find the config.json file to authenticate password.")
    with open(path, 'r') as r:
        config = json.load(r)
        return config['password'] == password


def latest_updates():
    path = Path.cwd() / Path('static') / Path('config.json')
    with open(path, 'r') as r:
        config = json.load(r)
        return config['updates']


def save_update():
    path = Path.cwd() / Path('static') / Path('config.json')
    config = {}
    with open(path, 'r') as r:
        config = json.load(r)
    config['updates'] = str(datetime.now())
    with open(path, 'w') as w:
        json.dump(config, w)


