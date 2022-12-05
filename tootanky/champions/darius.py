from tootanky.champion import BaseChampion


class Darius(BaseChampion):
    champion_name = "Darius"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
