
def user_correlation_matrix(similarity_method, users):
    matrix = [[0 for x in range(len(users))] for y in range(len(users))]
    i = 0
    for user_base in users:
        j = 1
        total_sm = 0.0
        c = 0
        for user_target in users:
            if user_target.cod != user_base.cod:
                print("Calc similary by % d and %d" %(user_base.cod, user_target.cod))
                sm = similarity_method(user_base.item_ratings, user_target.item_ratings)
                if sm < 0:
                    sm = 0
                total_sm = total_sm+sm
                c=c+1
                matrix[i][j] = [user_target, sm]
                j=j+1
        matrix[i][0] = [user_base, total_sm/c]
        i=i+1
    return matrix

