from tootanky.champion import BaseChampion


class Blitzcrank(BaseChampion):
    name = "Blitzcrank"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
