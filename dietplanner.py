class diet:
    def __init__(self, total_cal, proteins, carbs, fats):
        self.__totalcalories = total_cal
        self.__proteins = proteins
        self.__carbs = carbs
        self.__fats = fats

    def get_totalcalories(self):
        return self.__totalcalories

    def get_proteins(self):
        return self.__proteins

    def get_carbs(self):
        return self.__carbs

    def get_fats(self):
        return self.__fats