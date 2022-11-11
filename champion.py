@dataclass
class BaseStat:
    armor 
    mana
    hp


class BaseChampion:
    def __init__(self, champion_name: str):
        self.champion_name = champion_name
        
    def get_base_state(self):
        return BaseStat

class Aatrox(BaseChampion):
    super().__init__()
    self.armor = 15
    self.ad = 85

    def get_level(self, level):
        self.ad

    def equip_item(self, item):
        ad = item.ad

    def attack_q(self, q_level):
        damage = get_damage_q_level(q_level)
        
        
aatrox = Aatrox(level=17)
aatrox.equip_item(["doran", ])


garen = Garen(level=17)
garen.equip_item(["doran", "goredrinker"])

total_damage = aatrox.attack(garen)
