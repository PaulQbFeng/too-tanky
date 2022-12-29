from tootanky.champion import BaseChampion


class Azir(BaseChampion):
    name = "Azir"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
