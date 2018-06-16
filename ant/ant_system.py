import random, copy
from cbio_finalproject.util.Functions import *
from cbio_finalproject.util.predition import *
from cbio_finalproject.core.users import *
from operator import itemgetter

best = 10
n = 0 #qt_componentes
C = [] #componentes
y = 0 #valor inicial do feromôneo
tx_tweak = 20


p_ = [y]*n #iniciando vetor de feromônio
L = 10

popsize = 20


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

def criar_c_(C, Solution):
    s_ = [z[0] for z in Solution]
    C_ = [c_ for c_ in C if not c_[0] in s_]
    return C_

def selecionar(C_, i):
    z = [c for c in C_ if c[0] == (i+2)]
    ph = np.median([x[3] for x in z])
    choosed = random.choice([a for a in z if a[3] >= ph])
    if choosed==None:
        choosed = random.choice([a for a in z if a[0] == (i+2)])
    return choosed

def complete_trail(Solution):
    return len(Solution)==4

def hill_climb(Solution, t):
    t = int(t)
    q = 0
    q_S = fitness(Solution)
    while q < t:
        temp_r = copy.deepcopy(Solution)
        temp_r = tweak(temp_r)
        q_R = fitness(temp_r)
        if q_R < q_S:
            Solution = copy.deepcopy(temp_r)
            q_S = q_R
        q=q+1
    return Solution

def select_random(cod):
    x = [z for z in C if C[0]==cod]
    return x


def tweak(temp_r):
    r = random.randint(0,3)
    r2 = random.randint(0,10)
    temp_r[r][1] = r2
    temp_r[r][2] = obter_gene(temp_r[r][0], r2)
    return temp_r


def fitness(ind):
    rmse_t = 0.0
    qt = 0
    t = 0
    if with_ajust:
        ind = adjust(ind)
    for i in range(0, 4):
        if ind[i][1] > 0:
            rmse_aux = obter_gene(ind[i][0], ind[i][1])
            ind[i][2] = rmse_aux
            rmse_t = rmse_t + rmse_aux
            t = t + 1
            qt = qt + ind[i][1]
    fit = 0
    if t == 0 or rmse_t == 0.0:
        fit = sys.float_info.max
    else:
        z = math.fabs(10 - qt)
        fit = (rmse_t / t) * math.pow((z + 1), 2)
    ind[4]=fit
    return fit

def zerar_componentes():
    for c in C:
        c[3] = 0

def adjust(s):
    e = sum(s[i][1] for i in range(0, 4))
    z = 10 - e
    while z!=0:
        for i in range(0, 4):
            if 0 <= s[i][1] < 10 and z > 0:
                s[i][1]+=1
                z-=1
            elif 0 < s[i][1] and z < 0:
                s[i][1] -= 1
                z += 1
    return s

components()

def run(pop_size, e):
    zerar_componentes()
    script_dir = os.path.dirname(__file__)
    rel_path = "result_ant_" + str(pop_size) + "_" + str(e) + "_.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "w")

    Best = None
    qt_interacoes = 0
    bests = []
    while True:
        qt_interacoes += 1
        #print("Interação %d" % qt_interacoes)
        P = []
        for i in range(popsize):
            s_p = None
            s_p = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], 0]
            for i in range(0, 4):
                s_p[i] = selecionar(C, i)
            s_p = hill_climb(s_p[:], t)
            if Best == None or fitness(s_p) < fitness(Best):
                Best = copy.deepcopy(s_p[:])
            P.append(s_p)
        #evaporação
        for i in range(len(C)):
            p_i = C[i][3]
            p_i = (1 - e) * p_i
            C[i][3] = p_i

        for p_i in range(len(P)):
            for c_i in range(len(C)):
                if C[c_i] in P[p_i]:
                    f_i = C[c_i][3]
                    f_i = f_i+P[p_i][4]
                    C[c_i][3] = f_i
        fit_best = fitness(Best)
        file.write("%d;%f\n" % (qt_interacoes, fit_best))
        bests.append([qt_interacoes, fit_best])
        if isBest(Best) or qt_interacoes > interacoes:
            break
    print(fit_best)
    plot_array(plt, bests)
    return bests

t = 5#interações do hill-climb
interacoes = 100
popsize = 10
e = 0.3
with_ajust = True



all_bests = []
import time
for i in range(100):
    ini = time.time()
    bests = run(popsize, e)
    fin = time.time()
    all_bests.append([fin-ini, bests])


script_dir = os.path.dirname(__file__)
rel_path = "better_config_ant.txt"
abs_file_path = os.path.join(script_dir, rel_path)
file = open(abs_file_path, "w")
for ab in all_bests:
    file.write("%f;"%ab[0])
    for z in ab[1]:
        file.write("[%d;%f];" %(z[0], z[1]))
    file.write("\n")


plt.title("ANT")
plt.suptitle("int:"+str(interacoes)+", pop_size:"+str(popsize)+", e:"+str(e)+", with ajust:"+ str(with_ajust)+".png")
plt.savefig("graph_ga_wa_"+str(with_ajust)+"_pop_"+str(popsize)+"_gen_"+str(interacoes)+"_"+str(e*10)+".png")
plt.show()

