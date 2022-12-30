from tootanky.champion import BaseChampion


class Anivia(BaseChampion):
    name = "Anivia"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
