from tootanky.champion import BaseChampion


class Aphelios(BaseChampion):
    champion_name = "Aphelios"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)