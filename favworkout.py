class f_workout:
    def __init__(self, favwork, freq, duration):
        self.__favwork = favwork
        self.__freq = freq
        self.__duration = duration

    def get_favwork(self):
        return self.__favwork

    def get_freq(self):
        return self.__freq

    def get_duration(self):
        return self.__duration