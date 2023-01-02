from tootanky.champion import Dummy
from tootanky.champions import Yasuo
from tootanky.item_factory import CloakofAgility, InfinityEdge


def test_yasuo_passive():
    dummy = Dummy(bonus_resistance=20)
    yasuo = Yasuo(inventory=[CloakofAgility(), CloakofAgility(), InfinityEdge()])
    assert yasuo.crit_chance == 1
    assert round(yasuo.crit_damage, 2) == 0.89 - 0.75
    assert round(yasuo.attack_damage) == 140
    assert round(yasuo.auto_attack.damage(target=dummy, is_crit=True), 1) == 220.5

