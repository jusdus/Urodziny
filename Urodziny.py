from flask import Flask, render_template, request, redirect, url_for
import datetime

from flask_zodb import ZODB, Object, List

import sys
path = '/home/justde/mysite'
if path not in sys.path:
   sys.path.insert(0, path)



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
    print(imiona())
    return render_template('index.html', name=name)


def baza_print():
    return render_template('baza.html')


@app.route('/baza')
def baza():
    name = request.args.get('nazwa', '')
    d = int(request.args.get('dzien', ''))
    m = int(request.args.get('miesiac', ''))
    y = int(request.args.get('rok', ''))
    slownik = db['imiona']
    slownik[name] = datetime.date(year=y, month=m, day=d)
    db['imiona'] = slownik
    return redirect(url_for("hello"))


def dzien_tyg(data):
    if (data.isoweekday()) == 1:
        return "Poniedziałek"
    if (data.isoweekday()) == 2:
        return "Wtorek"
    if (data.isoweekday()) == 3:
        return "Środa"
    if (data.isoweekday()) == 4:
        return "Czwartek"
    if (data.isoweekday()) == 5:
        return "Piątek"
    if (data.isoweekday()) == 6:
        return "Sobota"
    if (data.isoweekday()) == 7:
        return "Niedziela"

@app.route('/pytanie')
def ile_jeszcze():
    name = request.args.get('nazwa', '')
    today = datetime.date.today()
    names = imiona()
    if name not in names:
        return render_template('baza.html', name=name)
    option = request.args.get('option', '')
    if option == "o2":
        bd = names[name]
        rok = today.year
        bd = bd.replace(year=rok)
        if today > bd:
            bd = bd.replace(year=rok + 1)
        ile = bd - today
        days = ile.days
        return render_template('urodziny.html', days=days, day=dzien_tyg(bd))
    else:
        return redirect(url_for("ile_mam_lat_form", nazwa=name)) #'/ile_lat?nazwa=' + name)


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
    return rok - rok_ur + juz_bylo(bd)


@app.route('/ile_lat')
def ile_mam_lat_form():
    name = request.args.get('nazwa', '')
    names = imiona()
    if name not in names:
        return baza_print()
    else:
        wiek = ile_mam_lat(name)
        if wiek == 1:
            x = "rok"
        elif "2" <= str(wiek)[-1] <= "4":
            x = "lata"
        else:
            x = "lat"
        return render_template('ile_lat.html', name=name, years=wiek, x=x)



if __name__ == "__main__":
    app.run()
