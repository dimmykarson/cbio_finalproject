class User(object):
    def __init__(self, cod, item_ratings):
        self.cod = cod
        self.item_ratings = item_ratings
        self.item_with_predictions = []
        self.similar_users = []

    def __repr__(self):
        return 'User '+str(self.cod)

    def avg(self):
        return sum(self.item_ratings[i] for i in range(len(self.item_ratings)) if self.item_ratings[i]>0)/sum(i>0 for i in self.item_ratings)
    pass