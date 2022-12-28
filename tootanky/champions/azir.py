from tootanky.champion import BaseChampion


class Azir(BaseChampion):
    champion_name = "Azir"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
