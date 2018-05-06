import random
from cbio_finalproject.util.Functions import *
from cbio_finalproject.util.predition import *
from cbio_finalproject.core.users import load


n = 0 #qt_componentes
C = [] #componentes
e = random.uniform(0,1) #constante de evaporação
popsize = 0
y = 0 #valor inicial do feromôneo
t = 0 #interações do hill-climbind

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
    return sol[0]>1

def criar_c_(C, S):
    C_ = C[:]
    for s in S:
        to_remove = []
        for c in C_:
            if c[0]==s[0]:
                to_remove.append(c)
    for tr in to_remove:
        C_.remove(tr)
    return C_


def selecionar(S, C_):
    i = len(S)
    Best = None
    for c in C_:
        if not c[0]==i:
            continue
        if Best[2]==0 or c[2]==0:
            continue
        if Best == None or (c[3]*1/c[2])>(Best[3]*1/Best[2]):
            Best = c
    return Best

def complete_trail(S):
    return len(S)==4

def hill_climb(S, t):
    q = 0
    while q < t:
        s_cp = S[:]
        R = tweak(s_cp[0])
        if fitness(R)>fitness(S):
            S = R
    return S

def select_random(cod):
    x = [z for z in C if C[0]==cod]
    return x


def tweak(S):
    r = random.randint(0, 3)

    return S

def assess_fitness(S):
    return S

def fitness(S):
    return S[4]

def run():
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
                if complete_trail(S):
                    break
            S = hill_climb(S, t)
            assess_fitness(S)
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
