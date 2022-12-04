from tootanky.champion import BaseChampion

class Aatrox(BaseChampion):
    champion_name = "Aatrox"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
