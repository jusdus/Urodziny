from flask import Flask, render_template
import datetime
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('html/index.html')

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

@app.route('/name/<name>')
def ile_jeszcze(name):
    today = datetime.date.today()
    bd = slownik[name]
    rok = today.year
    bd = bd.replace(year=rok)
    if today > bd:
        bd = bd.replace(year=rok+1)
    ile = bd - today
    return "Do Twoich urodzin zostało już tylko {} dni!!!".format(ile.days)

if __name__ == "__main__":
    app.run()







