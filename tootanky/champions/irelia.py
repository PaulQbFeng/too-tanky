from tootanky.champion import BaseChampion


class Irelia(BaseChampion):
    champion_name = "Irelia"
    champion_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
