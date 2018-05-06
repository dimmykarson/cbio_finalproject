import numpy as np
import heapq, random, copy, math, sys

k = 0

def sum_sm(rating_matrix):
    total_matrix = sum(rating_matrix[i][1] for i in range(len(rating_matrix)) if rating_matrix[i][1]>0)
    ll = sum(x[1] > 0 for x in rating_matrix)
    if ll <= 0:
        return 0
    avg = total_matrix / ll
    return avg

def remove_k_ratings(user):
    c = 0
    while c<k:
        x = random.randint(0, len(user[1]) - 1)
        if user[1][x] <= 0:
            continue
        else:
            user[1][x] = 0
            c=c+1
    return user


def calc_similaridades_u(user, method, mt):
    l = len(mt)
    rating_matrix = []
    for u_m in mt:
        if user[0] == u_m[0]:
            continue
        sm = method(user[1], u_m[1])
        if sm < 0:
            sm = 0
        rating_matrix.append([u_m[0], sm])
    return rating_matrix


def best_similar_u(rating_matrix, l):
    high_similars = []
    avg_ = sum_sm(rating_matrix)
    if avg_==0:
        return high_similars
    for s in rating_matrix:
        if s[1] >= avg_:
            high_similars.append([s[0], s[1]])
    return high_similars


def get_best_predictions(qt, predicoes):
    if len(predicoes)==0:
        return []

    bests = []
    for p in range(len(predicoes)):
        if predicoes[p]<=0:
            continue
        bests.append([p, predicoes[p]])
    if len(bests)<qt:
        qt = len(bests)
    return sorted(bests, key=lambda tup: tup[1], reverse=True)[0:qt]

def calcular_rmse(user, preds):
    num = 0.0
    x = 0.0
    if len(preds) == 0:
        return sys.float_info.max
    for p in range(len(preds)):
        p_i = preds[p][1]
        if p_i <= 0:
            continue
        r_i = user[1][preds[p][0]]
        num = num + math.pow(p_i - r_i, 2)
        x = x + 1
    if x == 0:
        return sys.float_info.max
    rmse = math.sqrt(num / x)
    return rmse

def get(mt, cod):
    return next(x for x in mt if x[0]==cod)


def avg_(arr):
    sum = 0.0
    count = 0
    for i in arr:
        if i > 0:
            count = count+1
            sum = sum+i
    if count == 0:
        return 0
    else:
        return sum/count

def predicao_u(user_a, mt, high_similars):
    if len(high_similars)==0:
        return []
    rat_a = user_a[1]
    ra = avg_(rat_a)
    pred_u = [0]*len(rat_a)
    for rat in range(len(rat_a)):
        num = 0.0
        x = 0.0
        for s in high_similars:
            u = get(mt, s[0])
            rat_u_i = u[1]
            ru = avg_(rat_u_i)
            ru_i = rat_u_i[rat]
            if ru_i == 0:
                continue
            num = num + ((ru_i - ru) * s[1])
            x = x + math.fabs(s[1])
        if x == 0:
            p_a_i = -1
        else:
            p_a_i = ra + (num / x)
        if p_a_i > 5:
            p_a_i = 5
        pred_u[rat] = p_a_i
    return pred_u

def pred(user, list_usuarios, qt, tech):
    if qt <= 0:
        return 0
    user_copy = copy.deepcopy(user)
    user_copy = remove_k_ratings(user_copy)
    rating_matrix = calc_similaridades_u(user_copy, tech, list_usuarios)
    high_similar = best_similar_u(rating_matrix, len(rating_matrix))
    predicoes = predicao_u(user_copy, list_usuarios, high_similar)
    bests = get_best_predictions(qt, predicoes)
    rmse = calcular_rmse(user, bests)
    return rmse


