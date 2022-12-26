from tootanky.champion import BaseChampion


class Braum(BaseChampion):
    name = "Braum"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
