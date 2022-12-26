from tootanky.champion import BaseChampion


class Akali(BaseChampion):
    champion_name = "Akali"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
