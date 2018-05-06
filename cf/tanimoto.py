from scipy.spatial.distance import rogerstanimoto
def tanimoto_similarity(base, target):
    evaluation = rogerstanimoto(base, target)
    return evaluation
