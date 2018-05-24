import csv, random, sys, os
script_dir = os.path.dirname(__file__)
qt_users = 1000
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
    return users

def load_from_file():
    file = open("C:/temp/avaliacoes.csv", "r")
    reader = csv.reader(file, delimiter=";")
    users = []
    for r in reader:
        users.append([int(r[0]), [float(x) for x in r[1:]]])
    return users

def make_file():
    users = load_random()
    file = open("C:/temp/avaliacoes.csv", "w")
    for u in users:
        s = ""
        for f in u[1]:
            s = s+";"+str(f)
        file.write(str(u[0])+s+"\n")


##make_file()



avg_rmse_cosine = []
avg_rmse_euclidean_similarity = []
avg_rmse_pearson_similarity =[]
avg_rmse_spearman_similarity=[]

def init_pop_2(pop_size):
    pop=[]
    for i in range(pop_size):
        ind = [0, 0, [0, 0], [0, 0], [0, 0], [0, 0]]
        r = random.randint(0,10)
        ind[2][0] = r
        ind[2][1] = avg_rmse_cosine[r]
        ind[3][0] = r
        ind[3][1] = avg_rmse_euclidean_similarity[r]
        ind[4][0] = r
        ind[4][1] = avg_rmse_pearson_similarity[r]
        ind[5][0] = r
        ind[5][1] = avg_rmse_spearman_similarity[r]
        pop.append(ind)
    return pop


def load_rmses_aux(metodo):
    rel_path = "rmse"+metodo+"_k_1.csv"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "r")
    reader = csv.reader(file, delimiter=";")
    resultado = []
    for r in reader:
        c = []
        rmse = []
        c.append(int(r[0]))
        for i in range(1,11):
            rmse.append(float(r[i]))
        c.append(rmse)
        resultado.append(c)
    return resultado

def load_rmses():
    rmse_cosine_similarity = load_rmses_aux("cosine_similarity")
    rmse_euclidean_similarity = load_rmses_aux("euclidean_similarity")
    rmse_pearson_similarity = load_rmses_aux("pearson_similarity")
    rmse_spearman_similarity = load_rmses_aux("spearman_similarity")

    global avg_rmse_cosine
    avg_rmse_cosine = [0]*11
    for i in rmse_cosine_similarity:
        rmses = i[1]
        for j in range(len(rmses)):
            avg_rmse_cosine[j]=avg_rmse_cosine[j]+rmses[j]
    avg_rmse_cosine = [z/len(rmse_cosine_similarity) for z in avg_rmse_cosine]

    global avg_rmse_euclidean_similarity
    avg_rmse_euclidean_similarity = [0]*11
    for i in rmse_euclidean_similarity:
        rmses = i[1]
        for j in range(len(rmses)):
            avg_rmse_euclidean_similarity[j]=avg_rmse_euclidean_similarity[j]+rmses[j]
    avg_rmse_euclidean_similarity = [z/len(rmse_euclidean_similarity) for z in avg_rmse_euclidean_similarity]

    global avg_rmse_pearson_similarity
    avg_rmse_pearson_similarity = [0]*11
    for i in rmse_pearson_similarity:
        rmses = i[1]
        for j in range(len(rmses)):
            avg_rmse_pearson_similarity[j]=avg_rmse_pearson_similarity[j]+rmses[j]
    avg_rmse_pearson_similarity = [z/len(rmse_pearson_similarity) for z in avg_rmse_pearson_similarity]

    global avg_rmse_spearman_similarity
    avg_rmse_spearman_similarity = [0]*11
    for i in rmse_spearman_similarity:
        rmses = i[1]
        for j in range(len(rmses)):
            avg_rmse_spearman_similarity[j]=avg_rmse_spearman_similarity[j]+rmses[j]
    avg_rmse_spearman_similarity = [z/len(rmse_spearman_similarity) for z in avg_rmse_spearman_similarity]

def obter_gene(tech, qt):
    if tech == 2:
        return avg_rmse_cosine[qt]
    elif tech == 3:
        return avg_rmse_euclidean_similarity[qt]
    elif tech == 4:
        return avg_rmse_pearson_similarity[qt]
    elif tech == 5:
        return avg_rmse_spearman_similarity[qt]

load_rmses()