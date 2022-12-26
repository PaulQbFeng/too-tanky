from tootanky.champion import BaseChampion


class Amumu(BaseChampion):
    champion_name = "Amumu"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
