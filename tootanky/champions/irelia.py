from tootanky.champion import BaseChampion


class Irelia(BaseChampion):
    name = "Irelia"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
