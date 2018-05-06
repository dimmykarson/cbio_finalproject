from scipy.spatial.distance import cosine

def cosine_similarity(base, target):
    evaluation = cosine(base, target)
    if evaluation==0:
        return 1
    else:
        j = ((1/evaluation))/100
        if j > 1:
            j = 0.99-evaluation
        return j

