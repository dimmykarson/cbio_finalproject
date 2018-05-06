from scipy.spatial import distance
import sys
def euclidean_similarity(base_user_itens, target_user_itens):
    dst = distance.euclidean(base_user_itens, target_user_itens)
    if dst==0.0:
        return 1
    else:
        j = 1/dst
        if j > 1:
            return dst
        else:
            return j

