from tootanky.champion import BaseChampion


class AurelionSol(BaseChampion):
    name = "AurelionSol"
    range_type = "Ranged"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
