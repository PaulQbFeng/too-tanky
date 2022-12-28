from tootanky.champion import BaseChampion


class Ashe(BaseChampion):
    champion_name = "Ashe"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
