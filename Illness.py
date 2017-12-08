class Illness:
    def __init__(self, illness, startdate):
        self.illness = illness
        self.startdate = startdate

    def get_illness(self):
        return self.illness

    def get_startdate(self):
        return self.startdate

    def set_illness(self, illness):
        self.illness = illness

    def set_startdate(self, startdate):
        self.startdate = startdate
