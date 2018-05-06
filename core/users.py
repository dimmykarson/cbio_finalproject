import csv, random

qt_users = 100
qt_films = 20
qt_avaliacoes = 10

def load(tipo):
    if tipo==0:
        return load_random()
    else:
        return load_from_file()

def load_random():
    users = []
    for i in range(qt_users):
        films = [0] * qt_films
        qt = 0
        while qt < qt_avaliacoes:
            r = random.randint(0,qt_films-1)
            if not films[r]==0:
                continue
            else:
                rat = float(random.randint(10, 50)/10)
                films[r] = rat
                qt=qt+1
        users.append([i, films])
    return random.sample(users, qt_films)

def load_from_file():
    file = open("C:/temp/avaliacoes.csv", "r")
    reader = csv.reader(file, delimiter=";")
    users = []
    for r in reader:
        users.append([int(r[0]), [float(x) for x in r[1:]]])
    return random.sample(users, qt_users)

def make_file():
    users = load_random()
    file = open("C:/temp/avaliacoes.csv", "w")
    for u in users:
        s = ""
        for f in u[1]:
            s = s+";"+str(f)
        file.write(str(u[0])+s+"\n")



