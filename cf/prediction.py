#if user not define rating about item, then mark x as x<0 for to make a prediction about item

from cbio.cbio_finalproject.cf.matrix import user_correlation_matrix
import math
import numpy as np
from numpy import matrix

def prediction(rate, users, similarity_method):
    matrix = user_correlation_matrix(similarity_method, users)
    users = []
    for av in matrix:
        user = av[0][0]
        users.append(user)
        avg = av[0][1]
        for z in av[1:len(av)]:
            if z[1] >= avg:
                user.similar_users.append(z)
        ra_ = sum(user.item_ratings) / len(user.item_ratings)
        for i in range(len(user.item_ratings)):
            if user.item_ratings[i] > 0:
                continue
            num = 0.0
            den = 0.0
            for similar in user.similar_users:
                similar_user = similar[0]
                wau = similar[1]
                ru_su = sum(similar_user.item_ratings) / len(similar_user.item_ratings)
                rui_su = similar_user.item_ratings[i]
                num = num+((rui_su-ru_su)*wau)
                den = den+math.fabs(wau)
            pai = ra_+(num/den)
            if pai < 0:
                pai = 0
            user.item_with_predictions.append([i, pai])
        user.item_with_predictions = sorted(user.item_with_predictions, key=lambda row: row[1], reverse=True)
    return users


