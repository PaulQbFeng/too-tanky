from tootanky.champion import BaseChampion


class Akshan(BaseChampion):
    champion_name = "Akshan"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
