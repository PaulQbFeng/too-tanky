from tootanky.champion import BaseChampion


class Amumu(BaseChampion):
    name = "Amumu"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
