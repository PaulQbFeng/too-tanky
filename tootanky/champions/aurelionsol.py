from tootanky.champion import BaseChampion


class AurelionSol(BaseChampion):
    champion_name = "AurelionSol"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)