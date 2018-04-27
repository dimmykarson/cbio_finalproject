from scipy.stats import spearmanr
import sys
def spearman_similarity(base, target):
    evaluation = spearmanr(base, target)
    if evaluation[0]==1.0:
        return sys.float_info.max
    else:
        return evaluation[0]


