from scipy.spatial.distance import cosine
import sys
def cosine_similarity(base, target):
    evaluation = cosine(base, target)
    if evaluation <= 0.0:
        return sys.float_info.max
    else:
        return 1/evaluation

