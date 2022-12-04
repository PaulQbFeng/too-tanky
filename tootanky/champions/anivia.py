from tootanky.champion import BaseChampion

class Anivia(BaseChampion):
    champion_name = "Anivia"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
