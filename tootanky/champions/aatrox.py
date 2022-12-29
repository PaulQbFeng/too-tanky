from tootanky.champion import BaseChampion


class Aatrox(BaseChampion):
    name = "Aatrox"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
