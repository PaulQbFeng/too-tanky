from champion import BaseChampion

class Amumu(BaseChampion):
    champion_name = "Amumu"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)