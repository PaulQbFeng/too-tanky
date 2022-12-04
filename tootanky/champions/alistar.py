from tootanky.champion import BaseChampion

class Alistar(BaseChampion):
    champion_name = "Alistar"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)