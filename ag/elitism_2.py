import math, copy
from cbio_finalproject.util.predition import *
from cbio_finalproject.core.users import load, init_pop_2, obter_gene
import matplotlib.pyplot as plot



L = 10 #tamanho da lista de predições


def assess_fitness(ind):
    rmse_t = 0.0
    qt = 0
    t = 0
    aj = 0
    if with_ajust:
        ind = adjust(ind)
    for i in range(2, 6):
        if ind[i][0] > 0:
            rmse_aux = obter_gene(i, ind[i][0])
            ind[i][1] = rmse_aux
            rmse_t = rmse_t + rmse_aux
            t = t + 1
            qt = qt + ind[i][0]

    fit = 0
    if t == 0 or rmse_t == 0.0:
        fit = sys.float_info.max
    else:
        z = math.fabs(10 - qt)
        fit = (rmse_t / t) * math.pow((z + 1), 2)
    ind[0] = fit
    ind[1] = qt


def fitness(p):
    return p[0]

#tournament
def select_with_replacement(pop):
    best = random.choice(pop)
    for i in range(1, tournament_size):
        next_p = random.choice(pop)
        if (fitness(next_p) < fitness(best)):
            best = next_p
    return best

#one point
def crossover(pa_c, pb_c):

    point = random.randint(3, 4)
    aux_1 = pa_c[2:point]
    aux_2 = pa_c[point:6]
    aux_3 = pb_c[2:point]
    aux_4 = pb_c[point:6]
    res_1 = aux_1 + aux_4
    res_2 = aux_3 + aux_2
    pa_c[2:6] = res_1
    pb_c[2:6] = res_2

    return pa_c, pb_c

def mutate(S):
    for i in range(2, 6):
        r = random.randint(0, 100)
        if mutate_tax > r:
            r1 = random.randint(2, 5)
            S[r1][0] = random.randint(0, 10)
            S[r1][1] = obter_gene(i, S[r1][0])

    return S

def adjust(S):
    e = sum(S[i][0] for i in range(2, 6))
    z = 10 - e
    unid = 0
    h = z
    while z!=0:
        for i in range(2,6):
            if 0 <= S[i][0] < 10 and z > 0:
                S[i][0]+=1
                z-=1
            elif 0 < S[i][0] and z < 0:
                S[i][0] -= 1
                z += 1
    return S

def run():
    script_dir = os.path.dirname(__file__)
    rel_path = "result_ag_"+str(generations)+"_"+str(pop_size)+"_"+str(crossover_tax)+"_"+str(mutate_tax)+"_"+str(elitism_n)+"_"+str(with_ajust)+"_.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "w")
    pop = init_pop_2(pop_size)
    best = None
    gen = 0
    qt_elemt = 0
    bests = []
    while True:
        gen+=1
        #print("Interation: %d" % gen)
        for p in pop:
            assess_fitness(p)
            qt_elemt=qt_elemt+1
            if best == None or fitness(p) < fitness(best):
                best = copy.deepcopy(p)
        q = heapq.nsmallest(elitism_n, pop)
        for z in range(int((pop_size - elitism_n) / 2)):
            pa = select_with_replacement(pop)
            pb = select_with_replacement(pop)
            children = crossover(copy.deepcopy(pa), copy.deepcopy(pb))
            q.append(mutate(children[0]))
            q.append(mutate(children[1]))
        pop = copy.deepcopy(q)
        #print("%d geração. Melhor elemento (RMSE): %s" %(gen, str(best[0]) + ": " + str(best)))
        file.write("%d;%f\n" %(gen, best[0]))
        bests.append([gen, best[0]])
        if gen > generations:
            break
    print(fitness(best))
    plot_array(plot, bests)
    return bests

tournament_size = 2
pop_size = 10
elitism_n = 2
generations = 200
mutate_tax = 30
crossover_tax = 70
with_ajust = True


all_bests = []
import time
for i in range(100):
    ini = time.time()
    bests = run()
    fin = time.time()
    all_bests.append([fin-ini, bests])


script_dir = os.path.dirname(__file__)
rel_path = "better_config.txt"
abs_file_path = os.path.join(script_dir, rel_path)
file = open(abs_file_path, "w")
for ab in all_bests:
    file.write("%f;"%ab[0])
    for z in ab[1]:
        file.write("[%d;%f];" %(z[0], z[1]))
    file.write("\n")


plot.title("GA")
plot.suptitle("T_size:"+str(tournament_size)+", gen:"+str(generations)+", pop_size:"
              +str(pop_size)+", mutate_tax:"+str(mutate_tax/100)+", crossover:"+str(crossover_tax/100)+
              ", with ajust:"+ str(with_ajust)+".png")
plot.savefig("graph_ga_wa_"+str(with_ajust)+"_pop_"+str(pop_size)+"_gen_"+str(generations)+" ("+str(mutate_tax)+" "+str(crossover_tax)+").png")
plot.show()