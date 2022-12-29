from tootanky.champion import BaseChampion


class Zed(BaseChampion):
    name = "Zed"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
