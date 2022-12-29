from tootanky.champion import BaseChampion


class Akali(BaseChampion):
    name = "Akali"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
