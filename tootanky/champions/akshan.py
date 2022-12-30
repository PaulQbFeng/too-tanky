from tootanky.champion import BaseChampion


class Akshan(BaseChampion):
    name = "Akshan"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
