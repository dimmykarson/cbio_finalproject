from scipy.stats import pearsonr
import sys, math


#quanto mais próximo de 1, melhor!
#0.0 para quando não consegue definir similaridade
def pearson_similarity(base, target):
    evaluation = pearsonr(base, target)
    if math.isnan(float(evaluation[0])):
        return 0.0
    if evaluation[0] < 0.0:
        return 0.0
    else:
        return evaluation[0]



