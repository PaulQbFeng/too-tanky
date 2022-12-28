from tootanky.champion import BaseChampion


class Braum(BaseChampion):
    champion_name = "Braum"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
