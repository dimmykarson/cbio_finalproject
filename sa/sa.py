import copy, random, math
from cbio_finalproject.core.users import *
from cbio_finalproject.util.Functions import *
import matplotlib.pyplot as plot

epsolon = 0.0001

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

def quality(ind):
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
    return fit

def tweak(S):
    r = random.randint(2, 5)
    r2 = random.randint(0, 10)
    S[r][1] = obter_gene(r, r2)
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
    bests = []

    while True:
        print("Temp: %f" %t)
        iterations=iterations+1
        R = tweak(copy.deepcopy(S))
        q_R = quality(R)
        q_S = quality(S)
        if q_R < q_S or delta(q_R, q_S, t):
            S = copy.deepcopy(R)
            bests.append([iterations, q_R])
        t = t*tx_decrease
        if q_S < q_Best:
            Best = copy.deepcopy(S)
            q_Best = q_S
        if is_ideal(Best) or t < epsolon:
            break
        file.write("%d;%f\n" % (iterations, quality(Best)))
    plot_array(plot, bests)
    return Best

with_ajust = True
same_seed = True
ind = random_ind()
t = 1000
decrease = 0.90
for i in range(0,1000):
    if not same_seed:
        ind = random_ind()
    Best = run(t, decrease, copy.deepcopy(ind))
plot.savefig("graph_sa"+str(same_seed)+".png")
plot.show()
