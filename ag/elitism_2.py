
from cbio_finalproject.util.predition import *
from cbio_finalproject.core.users import load, init_pop_2, obter_gene


L = 10
tournament_size = 2
pop_size = 500
elitism_n = 0
generations = 100
mutate_tax = 20
crossover_tax = 70

def assess_fitness(ind):
    r = 0.0
    qt = 0
    for i in range(2, 6):
        r = r+ind[i][1]
        qt = qt+ind[i][0]
    if r==0:
        r = sys.float_info.max
    if qt>10:
        r = r*qt
    ind[0] = (1/r)
    ind[1] = qt
    return ind

def fitness(p):
    return p[0]

#torunament
def select_with_replacement(pop):
    best = random.choice(pop)
    for i in range(1, tournament_size):
        next_p = random.choice(pop)
        if (fitness(next_p) > fitness(best)):
            best = next_p
    return best


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
        r = random.randint(0, 100)
        if mutate_tax > r:
            qt = random.randint(0,10)
            a[i] = [qt, obter_gene(i, qt)]

    return a




def run():
    pop = init_pop_2(pop_size)
    best = None
    gen = 0
    qt_elemt = 0
    while True:
        gen = gen + 1
        for p in pop:
            assess_fitness(p)
            qt_elemt=qt_elemt+1
            if best == None or fitness(p) > fitness(best):
                best = p
        q = heapq.nlargest(elitism_n, pop)
        for z in range(int((pop_size - elitism_n) / 2)):
            pa = select_with_replacement(pop)
            pb = select_with_replacement(pop)
            pa_c = pa[:]
            pb_c = pb[:]
            children = crossover(pa_c, pb_c)
            q.append(mutate(children[0]))
            q.append(mutate(children[1]))
        p = q
        print("%d geração. Melhor elemento (RMSE): %s" %(gen, str(best[0]) + ": " + str(best)))
        if gen > generations:
            break
    return best



run()