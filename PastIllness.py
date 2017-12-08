from Illness import Illness


class PastIllness(Illness):
    def __init__(self, illness, startdate, enddate):
        super().__init__(illness, startdate)
        self.enddate = enddate

    def get_enddate(self):
        return self.enddate

    def set_enddate(self, enddate):
        self.enddate = enddate
