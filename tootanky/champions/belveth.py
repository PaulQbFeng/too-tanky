from tootanky.champion import BaseChampion


class BelVeth(BaseChampion):
    champion_name = "Belveth"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
