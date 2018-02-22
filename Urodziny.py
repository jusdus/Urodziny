from flask import Flask, render_template, request, redirect
import datetime



from flask.ext.zodb import ZODB, Object, List

class User(Object):

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.shoutouts = List()

app = Flask(__name__)
app.config['ZODB_STORAGE'] = 'file://app.fs'
db = ZODB(app)


slownik = {"Justyna": datetime.date(year=1987, month=6, day=17),
           "Filip": datetime.date(year=1987, month=3, day=26),
           "Stasio": datetime.date(year=2012, month=5, day=24),
           "Niunia": datetime.date(year=2016, month=2, day=25)}

def imiona():
    if 'imiona' not in db:
        db['imiona'] = slownik
    return db['imiona']

@app.route('/')
def hello(name=None):
    imiona()
    return render_template('index.html', name=name)


def baza_print():
    return render_template('baza.html')

@app.route('/dane')
def baza():
    name = request.args.get('nazwa', '')
    d = int(request.args.get('dzien', ''))
    m = int(request.args.get('miesiac', ''))
    y = int(request.args.get('rok', ''))
    slownik = db['imiona']
    slownik[name] = datetime.date(year = y, month = m, day = d)
    db['imiona'] = slownik
    return ile_jeszcze()

@app.route('/pytanie')
def ile_jeszcze():
    name = request.args.get('nazwa', '')
    today = datetime.date.today()
    names = imiona()
    if name not in names:
        return baza_print()
    bd = names[name]
    rok = today.year
    bd = bd.replace(year=rok)
    if today > bd:
        bd = bd.replace(year=rok+1)
    ile = bd - today
    days = ile.days
    return render_template('urodziny.html', days = days)

def juz_bylo(data):
    today = datetime.date.today()
    rok = today.year
    data = data.replace(year=rok)
    if today > data:
        return 0
    return -1

def ile_mam_lat(name):
    today = datetime.date.today()
    names = imiona()
    if name not in names:
        return baza_print()
    bd = names[name]
    rok = today.year
    rok_ur = bd.year
    return rok-rok_ur+juz_bylo(bd)


if __name__ == "__main__":
    app.run()







