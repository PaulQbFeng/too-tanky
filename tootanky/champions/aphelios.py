from tootanky.champion import BaseChampion


class Aphelios(BaseChampion):
    name = "Aphelios"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
