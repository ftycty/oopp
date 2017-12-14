import Forum as f

class Fitness(f.Forum):
    def __init__(self, title, content, type, exercise, time):
        f.Forum.__init__(self,title, content, type)
        self.__exercise = exercise
        self.__time = time

    def get_exercise(self):
        return self.__exercise

    def get_time(self):
        return self.__time
