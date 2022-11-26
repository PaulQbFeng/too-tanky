from champion import BaseChampion
    
class Brand(BaseChampion):
    champion_name = "Brand"

    def __init__(self, **kwargs):
        super().__init__(champion_name=__class__.champion_name, **kwargs)