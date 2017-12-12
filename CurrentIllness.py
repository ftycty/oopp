from Illness import Illness


class CurrentIllness(Illness):
    def __init__(self,illness, startdate):
        super().__init__(illness, startdate)
