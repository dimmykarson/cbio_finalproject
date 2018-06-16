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
    if crossover_type=='one_point':

        point = random.randint(3, 4)
        aux_1 = pa_c[2:point]
        aux_2 = pa_c[point:6]
        aux_3 = pb_c[2:point]
        aux_4 = pb_c[point:6]
        res_1 = aux_1 + aux_4
        res_2 = aux_3 + aux_2
        pa_c[2:6] = res_1
        pb_c[2:6] = res_2

    elif crossover_type=='two_point':
        point1 = 3
        point2 = 4
        aux_1 = pa_c[2:point1]
        aux_2 = pa_c[point1:point2]
        aux_3 = pa_c[point2:6]

        aux_4 = pb_c[2:point1]
        aux_5 = pb_c[point1:point2]
        aux_6 = pb_c[point2:6]

        res_1 = aux_1 + aux_5 + aux_3
        res_2 = aux_4 + aux_2 + aux_6

        pa_c[2:6] = res_1
        pb_c[2:6] = res_2

    elif crossover_type=='uniform':
        for i in range(2, 6):
            r = random.randint(0,100)
            if crossover_tax>r:
                aux = pa_c[i]
                pa_c[i] = pb_c[i]
                pb_c[i] = aux

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
    file = None
    if write_files:
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
        print("Interation: %d" % gen)
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
        if write_files:
            file.write("%d;%f\n" %(gen, best[0]))
        bests.append([gen, best[0]])
        if gen > generations:
            break
    plot_array(plot, bests)
    return bests

tournament_size = 2
pop_size = 10
elitism_n = 2
generations = 200
mutate_tax = 30
crossover_tax = 70
with_ajust = True
crossover_type = 'one_point'
be_plot = False
executions = 100
write_files = True

import json

def load_config():
    fh = open("config.json", 'r')
    db = json.load(fh)

    global tournament_size
    tournament_size = db['tournament_size']
    global pop_size
    pop_size = db['pop_size']
    global elitism_n
    elitism_n = db['elitism_n']
    global generations
    generations = db['generations']
    global mutate_tax
    mutate_tax = db['mutate_tax']
    global crossover_tax
    crossover_tax = db['crossover_tax']
    global with_ajust
    with_ajust = db['with_ajust']
    global crossover_type
    crossover_type = db['crossover_type']
    global be_plot
    be_plot = db['be_plot']
    global executions
    executions = db['executions']
    global write_files
    write_files = db['write_files']


load_config()
all_bests = []
import time
best_time = sys.float_info.max
sum_time = 0
avg_time = 0
worst_time = 0

best_rmse = sys.float_info.max
sum_rmse = 0
avg_rmse = 0
worst_rmse = 0


for i in range(executions):
    ini = time.time()
    bests = run()
    fin = time.time()
    final_time = fin - ini
    if final_time<best_time:
        best_time = final_time
    if final_time>worst_time:
        worst_time = final_time
    sum_time += final_time

    best_aux = min(bests, key=lambda item:item[1])[1]
    worst_aux = max(bests, key=lambda item: item[1])[1]
    if best_aux<best_rmse:
        best_rmse = best_aux
    if worst_aux>worst_rmse:
        worst_rmse=worst_aux


    sum_rmse += (sum(x[1] for x in bests)/len(bests))

    all_bests.append([final_time, bests])

avg_time = sum_time/executions
avg_rmse = sum_rmse/executions

experiment = str(time.time())

if write_files:
    script_dir = os.path.dirname(__file__)
    rel_path = "result_"+experiment+"_ag.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "w")
    for ab in all_bests:
        file.write("%f;"%ab[0])
        for z in ab[1]:
            file.write("[%d;%f];" %(z[0], z[1]))
        file.write("\n")

    rel_path = "data_result_"+experiment+"_ag.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "w")
    file.write("Time: %f; %f; %f\n"%(best_time, worst_time, avg_time))
    file.write("RMSE: %f; %f; %f" % (best_rmse, worst_rmse, avg_rmse))

if be_plot:
    plot.title("GA")
    plot.suptitle("T_size:" + str(tournament_size) + ", gen:" + str(generations) + ", pop_size:"
                  + str(pop_size) + ", mutate_tax:" + str(mutate_tax / 100) + ", crossover:" + str(
        crossover_tax / 100) +
                  ", with ajust:" + str(with_ajust) + ".png")
    plot.savefig("graph_ga_wa_" + str(with_ajust) + "_pop_" + str(pop_size) + "_gen_" + str(generations) + " (" + str(
        mutate_tax) + " " + str(crossover_tax) + ").png")
    plot.show()