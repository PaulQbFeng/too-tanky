from tootanky.champion import BaseChampion


class Azir(BaseChampion):
    name = "Azir"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
