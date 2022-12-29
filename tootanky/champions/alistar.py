from tootanky.champion import BaseChampion


class Alistar(BaseChampion):
    name = "Alistar"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
