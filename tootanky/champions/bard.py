from tootanky.champion import BaseChampion


class Bard(BaseChampion):
    name = "Bard"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
