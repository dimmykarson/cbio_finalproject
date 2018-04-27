class User(object):
    def __init__(self, cod, item_ratings):
        self.cod = cod
        self.item_ratings = item_ratings
        self.item_with_predictions = []
    pass