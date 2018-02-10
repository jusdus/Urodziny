from flask import Flask, render_template, request
import datetime
app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)

slownik = {"Justyna": datetime.date(year=1987, month=6, day=17),
           "Filip": datetime.date(year=1987, month=3, day=26),
           "Stasio": datetime.date(year=2012, month=5, day=24),
           "Niunia": datetime.date(year=2016, month=2, day=25)}

def imie_w_bazie(name):
    if name in slownik:
        return ile_jeszcze(name)
    print("Jakie jest Twoje imię?")
    name = input()
    print("Podaj rok urodzenia")
    y = int(input())
    print("Podaj miesiąc urodzenia")
    m = int(input())
    print("Podaj dzień urodzenia")
    d = int(input())
    slownik[name] = datetime.date(year = y, month = m, day = d)

    return ile_jeszcze(name)

@app.route('/pytanie')
def ile_jeszcze():
    name = request.args.get('nazwa', '')
    today = datetime.date.today()
    bd = slownik[name]
    rok = today.year
    bd = bd.replace(year=rok)
    if today > bd:
        bd = bd.replace(year=rok+1)
    ile = bd - today
    days = ile.days
    return render_template('urodziny.html', days = days)

if __name__ == "__main__":
    app.run()







