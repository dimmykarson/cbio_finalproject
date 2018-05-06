from scipy.stats import spearmanr
import sys
def spearman_similarity(base, target):
    evaluation = spearmanr(base, target)
    return evaluation[0]



