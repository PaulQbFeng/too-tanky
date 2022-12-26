from tootanky.champion import BaseChampion


class Bard(BaseChampion):
    name = "Bard"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
