from tootanky.champion import BaseChampion


class BelVeth(BaseChampion):
    name = "Belveth"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
