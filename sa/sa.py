import copy, random, math
from cbio_finalproject.core.users import *
from cbio_finalproject.util.Functions import *

epsolon = 0.0001

def quality(ind):
    rmse_t = 0.0
    qt = 0
    t = 0
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
    fit = fit/1000
    ind[0] = fit
    ind[1] = qt
    return fit

def tweak(S):
    r1 = random.randint(2, 5)
    r2 = random.randint(2, 5)

    aux = S[r1][0]
    S[r1][0] = S[r2][0]
    S[r1][1] = obter_gene(r1, S[r1][0])

    S[r2][0] = aux
    S[r2][1] = obter_gene(r2, S[r2][0])

    return S

def delta(q_R, q_S, t):
    r = random.uniform(0, 1)
    try:
        return r<math.exp((q_R-q_S)/t)
    except:
        return False

def is_ideal(S):
    return quality(S)==0

def run(t,tx_decrease, S):
    script_dir = os.path.dirname(__file__)
    rel_path = "result_sa_" + str(t) +"_"+ str(tx_decrease)+ "_.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    file = open(abs_file_path, "w")

    Best = copy.deepcopy(S)
    q_Best = quality(Best)
    iterations = 0
    while True:
        print("Temp: %f" %t)
        iterations=iterations+1
        R = tweak(copy.deepcopy(S))
        q_R = quality(R)
        q_S = quality(S)
        if quality(R) < quality(S) or delta(q_R, q_S, t):
            S = copy.deepcopy(R)
        t = t*tx_decrease
        if q_S < q_Best:
            Best = copy.deepcopy(S)
            q_Best = q_S
        if is_ideal(Best) or t < epsolon:
            break
        file.write("%d;%f\n" % (iterations, quality(Best)))
    plot(abs_file_path)
    print("Interações %d"%iterations)
    return Best


ind = random_ind()
Best = run(2000, 0.99, copy.deepcopy(ind))
