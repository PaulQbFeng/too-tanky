from tootanky.champion import BaseChampion


class Alistar(BaseChampion):
    champion_name = "Alistar"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
