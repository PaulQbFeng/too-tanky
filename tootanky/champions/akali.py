from tootanky.champion import BaseChampion


class Akali(BaseChampion):
    champion_name = "Akali"
    champion_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)
