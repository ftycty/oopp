from Forum import Forum


class Fitness(Forum):
    def __int__(self, title, content, type, exercise, reps, time, sets):
        Forum.__init__(self, title, content, type)
        self.__exercise = exercise
        self.__reps = reps
        self.__time = time
        self.__sets = sets


    #setter
    def set_exercise(self, exercise):
        self.__exercise = exercise

    def set_reps(self,reps):
        self.__reps = reps

    def set_time(self, time):
        self.__time = time

    def set_sets(self, sets):
        self.__sets = sets


    #getter
    def get_exercise(self):
        return self.__exercise

    def get_reps(self):
        return self.__reps

    def get_time(self):
        return self.__time

    def get_sets(self):
        return self.__sets