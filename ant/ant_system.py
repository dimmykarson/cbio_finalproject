import random
from cbio_finalproject.util.Functions import *
from cbio_finalproject.util.predition import *
from cbio_finalproject.core.users import load

best = 10
n = 0 #qt_componentes
C = [] #componentes
e = 0.01 #constante de evaporação
popsize = 10
y = 0 #valor inicial do feromôneo
t = 10 #interações do hill-climbind

L = 10

p_ = [y]*n #iniciando vetor de feromônio
interacoes = 100

list_usuarios = load(0)
user = random.choice(list_usuarios)

def components():
    print("Load componentes")
    for t in range(1, 5):
        for z in range(0, 11):
            predicao = pred(user, list_usuarios, z, techs[t])
            feromonio = 0
            C.append([t, z, predicao, feromonio])

def isBest(sol):
    return fitness(sol)>best

def criar_c_(C, S):
    C_ = C[:]
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
    i = len(S)+1
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
        s_cp = S[:]
        R = tweak(s_cp)
        if fitness(R)>fitness(S):
            S = R
        q=q+1
    return S

def select_random(cod):
    x = [z for z in C if C[0]==cod]
    return x


def tweak(S):
    r1 = random.randint(1, 4)
    r2 = random.randint(1, 4)
    z1 = S[r1-1][1]
    z2 = S[r2-1][1]


    #pegar aleatoriamente um item dos componentes de cod = r e adicionar na solução
    x1 = [z for z in C if z[0]==r1 and z[1]==z2]
    x2 = [z for z in C if z[0]==r2 and z[1]==z1]

    item1 = random.choice(x1)
    item2 = random.choice(x2)
    S[r1-1]=item1
    S[r2-1]=item2

    return S

def assess_fitness(S):
    return S

def fitness(S):
    fit = sum(r[2] for r in S)
    qt_itens = sum(r[1] for r in S)
    if fit == 0:
        return 0
    return (1/fit)*qt_itens

def run(pop_size):
    components()
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


        if isBest(Best) or qt_interacoes > interacoes:
            break
    return Best

for i in range(10):
    Best = run(popsize)
    print("Solução %d. Fitness: %f. dados: %s" % (i, fitness(Best), str(Best)))