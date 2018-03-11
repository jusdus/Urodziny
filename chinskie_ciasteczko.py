import random


def chinskie():
    with open('static/cytaty.txt', 'rU') as f:
        count = len(f.readlines())
    los = random.randint(0, (count - 1))

    with open('static/cytaty.txt', 'rU') as f:
        return f.readlines()[los]


print(chinskie())
