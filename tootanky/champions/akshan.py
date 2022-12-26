from tootanky.champion import BaseChampion


class Akshan(BaseChampion):
    champion_name = "Akshan"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
