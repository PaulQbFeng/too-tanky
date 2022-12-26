from tootanky.champion import BaseChampion


class Azir(BaseChampion):
    champion_name = "Azir"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
