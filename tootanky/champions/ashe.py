from tootanky.champion import BaseChampion


class Ashe(BaseChampion):
    name = "Ashe"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
