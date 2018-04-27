from scipy.spatial import distance
import sys
def euclidean_similarity(base_user_itens, target_user_itens):
    dst = distance.euclidean(base_user_itens, target_user_itens)
    if dst==0.0:
        return sys.float_info.max
    else:
        return 1/dst


print(euclidean_similarity([1, 2, 3, 5], [23, 58, 99, 1]))
print(euclidean_similarity([1, 2, 3, 5], [1, 2, 3,5]))