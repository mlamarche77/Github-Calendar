import base64
import requests
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors

import numpy as np
import pandas as pd
from io import BytesIO
from time import sleep
import csv
from pathlib import Path


def csv_data(file: str):
    assert Path(file).exists(), f"File doesn't exist: {file}"
    with open(file, newline='') as csvfile:
        return list(csv.reader(csvfile, delimiter=','))


def extract(file: str):
    contents = csv_data(file)
    data = contents[1:]
    return [line for line in data]


def extract_usernames(file: str):
    contents = csv_data(file)
    headers = contents[0]
    data = contents[1:]
    return [dict(zip(headers, line))['github'] for line in data]


def get_api_key():
    file = Path.cwd() / Path('github_api_key.txt')
    try:
        with open(file, 'r') as r:
            return r.read().strip().replace("\n", "")
    except Exception:
        if not file.exists():
            print('\033[93mWarning: github_token.txt is not found in current working directory.\033[0m')
            print('\033[34mCreate the file and paste your GitHub API token to use GitHubs GraphQL API.\033[0m')


class Cohorts:
    def __init__(self, file: str):
        self.root = {}
        for line in extract(file):
            self.add(line)

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

    def coaches(self):
        return self.root.keys()

    def cohorts(self, coach):
        return self.root[coach].keys()

    def filter(self, coach, cohort):
        return self.root[coach][cohort]

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
        print(self.months)
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
            return {resp.status_code: resp.reason}

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
    users = ['Jummies', 'ClaytonJones839', 'AbbyTunes', 'tompdriscoll', 'benthere914', '12Starlight', 'asafmohammad5', 'guw005', 'cjbreezey', 'josephjyang', 'Chloe-Baylock', '030820acc', 'hyunalee625', 'henryhannn', 'douglasryu', 'A-Qudsi', 'NR481', 'woodsywisdom', '87danielbradley', 'nevinchow', 'alex-pober', 'pierrenav13', 'msineath', 'jdaniel01', 'subinc1633', 'mattswedin', 'sparsons808', 'greg-nice', 'jurrel', 'walkerwilliamsx', 'scollier87', 'JortzFromSchool', 'Twprcntmlk', 'jasonkim0105', 'alpvyas', 'canberkvarli', 'jimsonm', 'sonwuana1', 'austin-from-tx', 'b-chai', 'pcampbell42', 'JayceeMagpusao', 'AmMonsoon', 'TheGuilbotine', 'crslpz', 'nichathong', 'Efren707', 'enomilan', 'Khiienu', 'ShawnBoyle7', 'jangcla', 'FremaAwuku', 'chloebarber', 'PeterMace', 'davidoh14', 'anvarov', 'annieyang1993', 'lemlooma', 'arwensookim', 'Kristianmartinw', 'sunnymallick', 'brandonforster822', 'jyih', 'conneru', 'andru17urdna', 'Emmay-Alam', 'alyoung1991', 'C-Bridge17', 'flatout007', 'penced0513', 'ycherradi', 'thesavoyard77', 'mickeysaddai', 'snigdhabanda', 'rollingferret', 'AlexanderDGeorge', 'lynnqueue', 'Requiem-of-Zero', 'justinnnnnnnn', 'ckyle6300', 'Machaelmus', 'sguttbinder', 'Bergan404', 'asiddiki98', 'greiter18', 'tkenned2020', 'Run5', 'KevinKaras', 'montoya1256', 'Feifeiyang5177', 'goldeneye5671', 'thedaebu', 'Abir-Al-Mahamud', 'cmwinner89', 'minwang2022', 'scrub1737', 'boromeot', 'zpreudhomme', 'ddgiovinazzo', 'Schploink', 'TroyD9241', 'virgknight', 'helloroos', 'fportin', 'JosefSipi', 'JanaeCui', 'jaewooklim1', 'ggharsha', 'vernchao91', 'brandonfang', 'bxue2', 'imvincenth', 'jessicaUP', 'tkla', 'tjtaylorjr', 'Onaconnapuna', 'JimmyKuangg', 'Sisysphus', 'rcreadii', 'estanob', 'bparsons17', 'CalebAmes', 'KyleHere', 'tkoh13', 'TastySatang', 'Bsnernier', 'BTCBlade', 'lemikee', 'WesTrinhKL', 'Jomix-13', 'MRossant', 'Omstachu', 'amandac3600', 'alex-pezzati', 'chrisbh4', 'valeriareynososf', 'LifeJunkieRaj', 'euniceparkk', 'ji-k', 'Concrete18', 'eric-tran2', 'BrandonMohan', 'Kirti-Harode', 'crisMtech95', 'NoahNim', 'nasanov', 'Skulllady', 'equan1090', 'Felmallakh', 'davezig', 'alex-therookie', 'Marshall-Diffey', 'aDerocher', 'MayUWish', 'jborja-one', 'Woods-Trevin', 'hnrywltn', 'sergeveli', '88joonyc', 'itsjoonie', 'LamarP', 'Cris415', 'sneakblue', 'oli223lopez', 'ethan-kaseff', 'MaxwellWehner', 'hechtoid', 'paulkwchoi92', 'AnoushSaroyan', 'charliepsheppard', 'ray-leun1', 'kchhak', 'AlbertgitC', 'SethUllman', 'jon-wehner', 'cowfish813', 'gobugi', 'js4484', 'heyarnold23', 'MCE-Design', 'BaselHassan8', 'Vazhac', 'cpark04', 'RyanGonzalezUSA', 'reynier25', 'MikaEleFant', 'blwishom', 'taylor-b-02', 'cfo8473', 'marstrong', 'jjzhang329', 'ahans1607', 'mjfung1', 'langston7', 'rlachivirus', 'guticode04', 'briannguyen4', 'sdkag', 'Steve530', 'rhaubenstock', 'solracdelsol', 'Changh341', 'smclaughlan', 'AChen414', 'tynan415', 'seanscott23', 'OussamaElar', 'aivnerrad', 'fanny-chan', 'Robert-Kauth', 'brianko90', 'egarbi123', 'elizabethqdang', 'justinrusso', 'jerryphan1', 'meeke198', 'ShenQi1996', 'mustafaomousa', 'mkellydevv', 'justinchore', 'stkterry', 'JoshuaJDevine', 'AlwynGrant', 'Jc-008', 'MasterGrant137', 'GilBu', 'glenpark00', 'spacegray', 'estherhrkang', 'JosueLugaro', 'Mtolentin', 'taylorbhogan', 'humormee', 'AdamHGuan', 'Arebiter', 'winterfreddy', 'sdipietro', 'isaacsungpak', 'HelenEdwards', 'thepshay', 'alex-ciminillo', 'JDBorges187', 'MatthewTaylor9758', 'alvinc90', 'paulobocanegra', 'tsbernstein', 'goosey-goose', 'juancattaneo92', 'David7Mejia', 'dennis-25', 'VictorHeDev', 'philling83', 'MattMores', 'WellerJay118', 'ccy1563', 'JonYu87', 'j-tomasik', 'pauulkim', 'migs-dc', 'presleyoreed3', 'shirleytang0121', 'VPilipenko334', 'jaguitart', 'AdeshPawaroo', 'SilentNN', 'DylanWelzel', 'depash', 'sezder', 'JamesRR91', 'ChristopherCFleming', 'JhonathanAde', 'Sirpeter89', 'Muz-98', 'yangc95', 'HiThereImCam', 'chrismann809', 'zackalsiday', 'anthonym313', 'dblonc', 'mordes89', 'priyeshshah147', 'GeniusSniper', 'pongdanny', 'hankc97', 'nhsb00', 'Joemanf', 'KingApe714', 'anyqx', 'jwily', 'IanDMcGrath', 'kennyxli', 'cfthorne83', 'per-pro', 'kaizhu94', 'dezadkins', 'KevLin2358', 'jsadsad', 'Bman2386', 'Prescottiec', 'charmuwu', 'AritonS', 'tozhang665', 'johnshivers3', 'parks14', 'IsoVoyd', 'djangothesolarboy', 'ryan031391', 'iethan-h', 'hansaem-kim', 'Alsm867', 'sunmeiappprep', 'ElephantTalk', 'yungcai', 'lefuller', 'grantc00', 'JoeZhang229', 'Juka1031', 'yunasty', 'ROTBOW', 'patschramm', 'zaminku', 'jay5375', 'Andrewcodes12', 'Huan4Ai', 'gmiddle', 'nkfrs3', 'cvhcvhcvh', 'mothwork', 'Thereal-victorhou', 'NoahSharretts', 'aryan151', 'wylin94', 'LakshmiPriyaPrakash', 'joeypeterson15', 'wziller', 'brandonlaursen', 'tharpercp', 'ecbell', 'anndonnelly', 'nebbb', 'pawan087', 'emmetthe', 'efremporter', 'CroissantAhhh', 'Lee6413', 'HGerdes', 'Vour123', 'abisfong', 'kelseysry', 'tannerhladek', 'rcwhite96', 'CamTangalakis', 'mehendaleo', 'EricGartner47', 'ashleighctucker', 'ad-sw', 'snakedreamz', 'suchimohan', 'yosefalan', 'gavinfitch', 'cloudiosx', 'a-sugawara', 'PatrickWellman', 'codenamerick', 'lytravis', 'Chocoloco123', 'juniporous', 'span9692', 'HowDidIGitHere', 'jshin720', 'alexlolas', 'kenthiroi', 'jas0123uah', 'Sumit-dey', 'christopher-hauser', 'devinjuley', 'JacobNicotra', 'mkoerner570', 'jburnt17', 'tforde4623', 'NawalJAhmed', 'andyrose507', 'nummyrice', 'LaterBlackBird', 'robstrass', 'Payneless', 'cBrownSF', 'NRaff', 'aroellig', 'jackychen6825', 'rytmercado', 'darothmedia', 'mattpettenato', 'HendrickSimonR', 'wesleycheungg', 'MalachiCoberley', 'cjc473', 'woahwinzeler', 'nicoletademaru', 'dreamdivine', 'kcheng16', 'shuangzsy', 'lyhourlay1', 'dchaan', 'RobertT122', 'kw-8', 'Geoffst3r', 'Williamsliam23', 'ms0372631', 'ThiagoDe', 'mjlomeli', 'JD-Fermin', 'hauck29', 'NJSim', 'nick-barr', 'linb1', 'alvitovitch', 'ashes4trees', 'MackZumarraga', 'StevenSookhai', 'keginzburg', 'chayacohen', 'calebjo', 'ypeikes18', 'kvh8899', 'marcocountryman', 'AlexD89', 'jdtavarez', 'enochtan17', 'sonja-ng', 'AnnaYTH', 'AlexDoes', 'ShuaLaik', 'tasangpo', 'em-ng', 'tc8appdevelo', 'sgelernter', 'apgupta3091', 'Jasonchu94', 'stellalc7', 'Corbin-Arcus', 'AndyAYu', 'rickythewriter', 'leech92', 'arleenpandher', 'manjoeso', 'hellodanielbai', 'susanzea', 'michelleahuang', 'laneyNL']
    username = "mjlomeli"
    git = GitHub(username)
    git.fetch()
    print(git)
    print(git.contribution)

