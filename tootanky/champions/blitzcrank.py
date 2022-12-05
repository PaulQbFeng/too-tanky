from tootanky.champion import BaseChampion


class Blitzcrank(BaseChampion):
    champion_name = "Blitzcrank"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)