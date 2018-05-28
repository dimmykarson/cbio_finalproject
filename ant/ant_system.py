import random, copy
from cbio_finalproject.util.Functions import *
from cbio_finalproject.util.predition import *
from cbio_finalproject.core.users import *


best = 10
n = 0 #qt_componentes
C = [] #componentes
y = 0 #valor inicial do feromôneo
t = 10 #interações do hill-climbind
tx_tweak = 20


p_ = [y]*n #iniciando vetor de feromônio
L = 10

popsize = 100
interacoes = 1000


list_usuarios = load(0)
user = random.choice(list_usuarios)

def components():
    print("Load componentes")
    for t in range(2, 6):
        for z in range(0, 11):
            ##predicao = pred(user, list_usuarios, z, techs[t])
            feromonio = 0
            rmse = obter_gene(t, z)
            C.append([t, z, rmse, feromonio])

def isBest(sol):
    return fitness(sol)>best

def criar_c_(C, S):
    C_ = copy.deepcopy(C)
    to_remove = []
    l = get_L(S)
    for s in S:
        to_remove = []
        for c in C_:
            if c[0]==s[0]:
                to_remove.append(c)
                continue
            if (c[1]+l)>L:
                to_remove.append(c)
                continue

    if not empty(to_remove):
        for tr in to_remove:
            C_.remove(tr)
    return C_

def get_L(S):
    return sum([x[1] for x in S])


def selecionar(S, C_):
    i = len(S)+2
    x = [z for z in C_ if z[0]==i]
    avg = sum(h[3] for h in x)/len(x)
    x_ = [z for z in x if z[3]>avg]
    if empty(x_):
        return random.choice(x)
    else:
        return random.choice(x_)

def complete_trail(S):
    return len(S)==4

def hill_climb(S, t):
    q = 0
    while q < t:
        R = tweak(copy.deepcopy(S))
        if fitness(R)>fitness(S):
            S = R
        q=q+1
    return S

def select_random(cod):
    x = [z for z in C if C[0]==cod]
    return x


def tweak(S):
    r = random.randint(0,3)
    r2 = random.randint(0,10)
    S[r][1] = r2
    S[r][2] = obter_gene(S[r][0], r2)
    return S

def assess_fitness(S):
    return S

def fitness(S):
    fit = sum(r[2] for r in S)
    qt_itens = sum(r[1] for r in S)
    if fit == 0:
        return 0
    z = math.fabs(10-qt_itens)
    return (1/(fit*(z+1)))

components()

def zerar_componentes():
    for c in C:
        c[3] = 0


def run(pop_size, e):
    zerar_componentes()
    script_dir = os.path.dirname(__file__)
    rel_path = "result_ant_" + str(pop_size) + "_" + str(e) + "_.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "w")

    Best = None
    qt_interacoes = 0
    while True:
        qt_interacoes = qt_interacoes + 1
        P = []
        for i in range(popsize):
            S = []
            while True:
                C_ = criar_c_(C, S)
                if empty(C_):
                    S = []
                else:
                    S.append(selecionar(S, C_))
                if len(S)==4 and get_L(S)<10:
                    S = []
                if complete_trail(S):
                    break
            S = hill_climb(S, t)
            if Best == None or fitness(S) > fitness(Best):
                Best = S
            P.append(S)
        #evaporação
        for i in range(len(C)):
            p_i = C[i][3]
            p_i = (1 - e) * p_i
            C[i][3] = p_i

        for p_i in range(len(P)):
            for c_i in range(len(C)):
                if C[c_i] in P[p_i]:
                    f_i = C[c_i][3]
                    f_i = f_i+fitness(P[p_i])
                    C[c_i][3] = f_i

        file.write("%d;%f\n" % (qt_interacoes, fitness(Best)))
        if isBest(Best) or qt_interacoes > interacoes:
            break
    return Best

run(100, 0.1)
run(1000, 0.5)
run(5000, 0.1)
run(5000, 0.5)