from Forum import Forum


class Nutrition(Forum):
    def __init__(self, title, content, type, ingredient, method):
        Forum.__init__(self, title, content, type)
        self.__ingredient = ingredient
        self.__method = method

    def get_ingredient(self):
        return self.__ingredient

    def get_method(self):
        return self.__method