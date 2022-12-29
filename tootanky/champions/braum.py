from tootanky.champion import BaseChampion


class Braum(BaseChampion):
    name = "Braum"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
