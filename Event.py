class Event:
    def __init__(self, event, date):
        self.__event = event
        self.__date = date

    def get_event(self):
        return self.__event

    def get_date(self):
        return self.__date

    def set_event(self, event):
        self.__event = event

    def set_date(self, date):
        self.__date = date
