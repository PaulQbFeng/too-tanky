from tootanky.champion import BaseChampion


class MissFortune(BaseChampion):
    champion_name = "MissFortune"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
