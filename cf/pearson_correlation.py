from scipy.stats import pearsonr
import sys



def pearson_similarity(base, target):
    evaluation = pearsonr(base, target)
    if evaluation[0] == 1.0:
        return sys.float_info.max
    else:
        return evaluation[0]


