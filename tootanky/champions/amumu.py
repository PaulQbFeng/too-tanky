from tootanky.champion import BaseChampion


class Amumu(BaseChampion):
    name = "Amumu"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
