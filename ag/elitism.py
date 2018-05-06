import heapq, random, copy, math
from cbio_finalproject.cf.pearson_correlation import pearson_similarity
from cbio_finalproject.cf.spearman_rank import spearman_similarity
from cbio_finalproject.cf.cosine import cosine_similarity
from cbio_finalproject.cf.euclidean import euclidean_similarity
from cbio_finalproject.ag.predition import *
from cbio_finalproject.core.users import load


pop_size=1000
elitism_n=5
gen=5000
crossover_tax = 50
mutate_tax = 10
L = 10
tournament_size = 4
techs = [None, pearson_similarity, spearman_similarity, cosine_similarity, euclidean_similarity]
list_usuarios = load(0)

def random_individual(user):
    # ind = [fit, [a] , [b], [c], [d]]
    # a = [na, error_na]
    # b = [nb, error_nb]
    # c = [nc, error_nc]
    # d = [nd, error_nd]
    ind = [0, [0, 0], [0, 0], [0, 0], [0, 0]]
    k = L
    for i in range(1, 5):
        if k <= 0:
            x = 0
        else:
            x = random.randint(1, k)
        ind[i][0]=x
        k = k - x
    if k > 0:
        j = random.randint(1, 4)
        ind[j][0] = ind[j][0] + k
    #calcular predições
    rmse_ind = 0.0
    for i in range(1, 5):
        if ind[i][0]==0:
            continue
        else:
            tech = techs[i]
            #pred = [error]
            predicao = pred(user, list_usuarios, ind[i][0], tech)
            rmse_ind = rmse_ind+predicao
            ind[i][1] = predicao
    if rmse_ind==0:
        ind[0] = 1/sys.float_info.max
    else:
        ind[0] = 1/rmse_ind
    return ind

def init_pop(user, pop_size):
    print("Montando pop %d" % pop_size)
    pop = []
    for i in range(pop_size):
        pop.append(random_individual(user))
    print("Fim [Montando pop]")
    return pop

def assess_fitness(ind):
    r = 0.0
    for i in range(1, 5):
        r = r+ind[i][1]
    ind[0] = 1/r
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
    for i in range(1, 5):
        r = random.uniform(1, 100)
        if crossover_tax > r:
            aux = pa_c[i]
            pa_c[i] = pb_c[i]
            pb_c[i] = aux
    return pa_c, pb_c

def mutate(user, a):
    r = random.randint(1, 100)
    if mutate_tax > r:

        r1 = random.randint(1, 4)
        r2 = random.randint(1, 4)

        gene1 = a[r1][0]
        gene2 = a[r2][0]

        if gene1 == 0 and gene2 == 0:
            return a

        predicao1 = pred(user, list_usuarios, gene2, techs[r1])
        predicao2 = pred(user, list_usuarios, gene1, techs[r2])

        a[r1] = [gene2, predicao1]
        a[r2] = [gene1, predicao2]

    return a

def is_best(best):
    return best[0]>1

def run(user, pop_size, elitism_n, generations):
    pop = init_pop(user, pop_size)
    best = None
    gen = 0
    qt_elemt = 0
    while True:
        gen = gen+1
        print("Gen %s" % str(gen))
        print("Qt Elementos avaliados %s" % str(qt_elemt))
        print("Calc ASSESS")
        for p in pop:
            assess_fitness(p)
            qt_elemt=qt_elemt+1
            if best == None or fitness(p) > fitness(best):
                best = p
        print("Fim [Calc ASSESS]")
        q = heapq.nlargest(elitism_n, pop)
        for z in range(int((pop_size-elitism_n)/2)):
            pa = select_with_replacement(pop)
            pb = select_with_replacement(pop)
            pa_c = pa[:]
            pb_c = pb[:]
            children = crossover(pa_c, pb_c)
            q.append(mutate(user, children[0]))
            q.append(mutate(user, children[1]))
        p = q
        print("Best elemento (RMSE): "+str(best[0])+": "+str(best))
        if is_best(best) or gen > generations:
            break
    return best


user = random.choice(list_usuarios)
best = run(user, pop_size, elitism_n, gen)
print(str(best))