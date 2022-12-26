from tootanky.champion import BaseChampion


class Brand(BaseChampion):
    name = "Brand"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
