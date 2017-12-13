from Forum import Forum

class Nutrition(Forum):
    def __init__(self, title, content, type, ingredient):
        Forum.__init__(self, title, content, type)
        self.__ingredient = ingredient

    def set_ingredient(self, ingredient):
        self.__ingredient = ingredient

    def get_ingredient(self):
        return self.__ingredient