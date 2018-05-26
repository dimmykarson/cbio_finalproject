import math, copy
from cbio_finalproject.util.predition import *
from cbio_finalproject.core.users import load, init_pop_2, obter_gene



L = 10 #tamanho da lista de predições
tournament_size = 2
pop_size = 50
elitism_n = 2
generations = 5000
mutate_tax = 10
crossover_tax = 70

def assess_fitness(ind):
    rmse_t = 0.0
    qt = 0
    t = 0
    for i in range(2, 6):
        if ind[i][0]>0:
            rmse_aux = obter_gene(i, ind[i][0])
            ind[i][1] = rmse_aux
            rmse_t=rmse_t+rmse_aux
            t=t+1
            qt=qt+ind[i][0]
    fit = 0
    if t == 0 or rmse_t==0.0:
        fit = sys.float_info.max
    else:
        z = math.fabs(10-qt)
        fit = (rmse_t/t)*(z+1)
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
    r = random.uniform(1, 100)
    if crossover_tax >= r:
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

def mutate(a):
    for i in range(2,6):
        r = random.randint(1, 100)
        if mutate_tax > r:
            r2 = random.randint(0, 10)
            a[i][0] = r2
    return a



def run():

    rel_path = "result_"+str(generations)+"_"+str(pop_size)+"_"+str(crossover_tax)+"_"+str(mutate_tax)+"_"+str(elitism_n)+"_.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "w")

    pop = init_pop_2(pop_size)
    best = None
    gen = 0
    qt_elemt = 0
    while True:
        gen = gen + 1
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
        print("%d geração. Melhor elemento (RMSE): %s" %(gen, str(best[0]) + ": " + str(best)))
        file.write("%d;%f\n" %(gen, best[0]))
        if gen > generations:
            break
    return best



run()
rel_path = "result_"+str(generations)+"_"+str(pop_size)+"_"+str(crossover_tax)+"_"+str(mutate_tax)+"_"+str(elitism_n)+"_.txt"
plot(rel_path)