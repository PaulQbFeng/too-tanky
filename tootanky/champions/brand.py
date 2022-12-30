from tootanky.champion import BaseChampion


class Brand(BaseChampion):
    name = "Brand"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
