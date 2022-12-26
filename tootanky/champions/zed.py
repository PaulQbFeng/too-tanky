from tootanky.champion import BaseChampion


class Zed(BaseChampion):
    name = "Zed"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
