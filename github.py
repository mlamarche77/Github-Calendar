import base64
import requests
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import numpy as np
import pandas as pd
from io import BytesIO
from time import sleep
import csv
from pathlib import Path


def csv_data(file: Path):
    assert file.exists(), f"File doesn't exist: {file}"
    with open(file, newline='') as csvfile:
        return list(csv.reader(csvfile, delimiter=','))


def save_csv(file_name, data):
    path = Path.cwd() / Path('static') / Path(file_name)
    with open(path, 'w') as w:
        w.write(data)


def upload_csv(data):
    try:
        save_csv('temp.csv', data)
        data = csv_data('temp.csv')
        save_csv('github.csv')
        path = Path.cwd() / Path('static') / Path('temp.csv')
        path.unlink()
    except Exception as e:
        print(f'\033[31m{e}\033[0m')
        print("Error trying to save file: github.csv")


def extract(file: Path):
    if not file or not file.exists():
        return []
    contents = csv_data(file)
    data = contents[1:]
    return [line for line in data]


def extract_usernames(file: str):
    contents = csv_data(file)
    headers = contents[0]
    data = contents[1:]
    return [dict(zip(headers, line))['github'] for line in data]


def get_api_key():
    path = Path.cwd() / Path('static') / Path('github_api_key.txt')
    assert path.exists(), f"File doesn't exist: {path}"
    try:
        with open(path, 'r') as r:
            return r.read().strip().replace("\n", "")
    except Exception:
        if not path.exists():
            print('\033[93mWarning: github_token.txt is not found in current working directory.\033[0m')
            print('\033[34mCreate the file and paste your GitHub API token to use GitHubs GraphQL API.\033[0m')


class Cohorts:
    def __init__(self, file: str = None):
        self.root = {}
        self.students = {}
        if file is None:
            return
        path = Path.cwd() / Path('static') / Path(file)
        for line in extract(path):
            self.add(line)
        self.add_all()

    def add(self, data: list):
        base = self.root
        while len(data) > 0:
            top = data.pop(0)
            if len(data) == 1:
                base[top] = data.pop(0)
            else:
                if top not in base:
                    base[top] = {}
                base = base[top]

    def add_all(self):
        self.root['all'] = {'all': {}}
        for coach, coh_tree in self.root.items():
            if coach == 'all':
                continue
            self.root[coach]['all'] = {}
            for dates, student_tree in coh_tree.items():
                if dates == 'all':
                    continue
                self.root[coach]['all'].update(student_tree)
                if dates not in self.root['all']:
                    self.root['all'][dates] = student_tree
                else:
                    self.root['all'][dates].update(student_tree)
                self.root['all']['all'].update(student_tree)
                for name, username in student_tree.items():
                    self.students[username] = {'name': name, 'coach': coach, 'username': username, 'cohort': dates}

    def coaches(self):
        return self.root.keys()

    def cohorts(self, coach):
        return self.root[coach].keys()

    def filter(self, coach, cohort):
        if cohort in self.root[coach]:
            return self.root[coach][cohort]
        return self.all(coach)

    def all(self, coach):
        return [val for arr in self.root[coach].values() for val in arr]

    def __str__(self):
        return str(self.root)


class Contribution:
    QUEUE = []
    UID = 0
    CURRENT = 0
    GIT = None

    def __init__(self, data):
        self.data = data
        self.weekday = []
        self.contributions = []
        self.week = []
        self.activity = []
        self.months = []
        self.__skip = None
        self.id = self.UID
        Contribution.UID += 1

    def embed(self):
        Contribution.QUEUE.append(self.id)
        while Contribution.CURRENT != self.id:
            sleep(0.05)
        fig = self.plot()
        tmpfile = BytesIO()
        plt.savefig(tmpfile, format='png', transparent=True)
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        plt.close(fig)
        Contribution.CURRENT += 1
        return f'data:image/png;base64,{encoded}'

    def calculate(self):
        for i, w in enumerate(self.data):
            for day in w:
                d = day['date']
                self.save_week(d)
                self.week.append(i)
                self.save_month(d)
                self.contributions.append(day['count'])
        for count in self.contributions:
            if count == 0:
                self.activity.append(0)
            elif count < 5:
                self.activity.append(1)
            elif count < 10:
                self.activity.append(2)
            elif count < 20:
                self.activity.append(3)
            elif count >= 20:
                self.activity.append(4)
            else:
                self.activity.append(0)

    def save_month(self, d: date):
        if d.month not in self.months or d.month != self.months[-1]:
            self.months.append(d.month)

    def save_week(self, date):
        week_day = date.weekday()
        if week_day == 6:
            self.weekday.append(7)
        else:
            self.weekday.append(6 - week_day)

    def plot(self):
        self.calculate()
        self.months = [val for i, val in enumerate(self.months[1:]) if i % 2 != 0] + [0]
        df = pd.DataFrame({"weekday": self.weekday, "week": self.week, "activity": self.activity})
        df.drop_duplicates(subset=["weekday", "week"], inplace=True)

        # reshape the data and plot it
        df2 = df.pivot(columns="week", index="weekday", values="activity")
        df2.fillna(0, inplace=True)

        Weekday, Week = np.mgrid[:df2.shape[0] + 1, :df2.shape[1] + 1]
        masked = np.ma.masked_array(df2.values, df2.values <= 0)

        fig, ax = plt.subplots(figsize=(20, 3))
        ax.set_aspect("equal")

        plt.pcolormesh(Week, Weekday, masked, cmap="Greens", edgecolor="#1F2836", vmin=0, vmax=4, rasterized=True)
        plt.xlim(0, df2.shape[1])
        week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', ''][::-1]
        ax = plt.gca()
        font_properties = {'family': 'sans-serif', 'weight': 'bold', 'size': '15'}

        yticks_loc = ax.get_yticks().tolist()
        ax.yaxis.set_major_locator(mticker.FixedLocator(yticks_loc))
        ax.set_yticklabels(week, fontdict=font_properties)
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='y', colors='white')

        xticks_loc = ax.get_xticks().tolist()
        ax.xaxis.set_major_locator(mticker.FixedLocator(xticks_loc))
        ax.set_xticklabels(self.months, fontdict=font_properties)
        ax.xaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.axes.xaxis.set_visible(False)

        return fig


class GitHub:
    KEY = None

    def __init__(self, username):
        if GitHub.KEY is None:
            GitHub.KEY = get_api_key()
        self.__headers = {'Authorization': f"Bearer {GitHub.KEY}"}
        self.__url = "https://api.github.com/graphql"
        self.username = username
        self.contribution = None
        self.profile_image = None
        self.url = None
        self.data = None
        self.graph = None

    def contribution_query(self):
        return """query { 
                  user(login: "%s"){
                    avatarUrl
                    url
                    contributionsCollection {
                      contributionCalendar {
                        weeks {
                          contributionDays {
                            contributionCount
                            date
                          }
                        }
                      }
                    }
                  }
                }""" % self.username

    def query(self, query):
        resp = requests.post(self.__url, headers=self.__headers, json={"query": query})
        if resp.status_code == 200:
            data = resp.json()
            if "errors" in data:
                return data["errors"]
            return data['data']
        else:
            raise ConnectionError(resp.reason)

    def fetch(self):
        query = self.contribution_query()
        data = self.query(query)
        user = data['user']
        self.profile_image = user['avatarUrl']
        self.url = user['url']
        contr = user['contributionsCollection']['contributionCalendar']
        weeks = contr['weeks']
        contributions = []
        for week in weeks:
            week_data = []
            for contri in week['contributionDays']:
                week_data.append({
                    'count': contri['contributionCount'],
                    'date': datetime.strptime(contri['date'], '%Y-%m-%d')
                })
            contributions.append(week_data)
        self.data = Contribution(contributions)
        self.graph = self.data.embed()

    def __str__(self):
        return f"Username: '{self.username}', url: '{self.url}'"

    def __repr__(self):
        return f"<GitHub"


if __name__ == "__main__":
    username = "mjlomeli"
    git = GitHub(username)
    git.fetch()
    print(git)
    print(git.contribution)
