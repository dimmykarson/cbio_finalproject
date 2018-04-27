
def user_correlation_matrix(similarity_method, users):
    matrix = [[0 for x in range(len(users))] for y in range(len(users))]
    i = 0
    for user_base in users:
        j = 0
        for user_target in users:
            if user_target.cod == user_base.cod:
                matrix[i][j] = None
            else:
                matrix[i][j]= similarity_method(user_base.item_ratings, user_target.item_ratings)
            j=j+1
        i = i+1
    return matrix

'''from cbio.cbio_finalproject.model.user import  User


u1 = User(1, [1, 0, 2, 3])
u2 = User(2, [0, 1, 1, 3])
u3 = User(3, [12, 0, 7, 8])
u4 = User(4, [1, 0, 2, 3])


users = []
users.append(u1)
users.append(u2)
users.append(u3)
users.append(u4)


from cbio.cbio_finalproject.cf.pearson_correlation import pearson_similarity
matrix = user_correlation_matrix(pearson_similarity, users)
print(matrix)


from cbio.cbio_finalproject.cf.spearman_rank import spearman_similarity
matrix = user_correlation_matrix(spearman_similarity, users)
print(matrix)'''
