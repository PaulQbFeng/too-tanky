from tootanky.champion import BaseChampion


class Bard(BaseChampion):
    champion_name = "Bard"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)