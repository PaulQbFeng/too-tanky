from tootanky.dummy import Dummy
from tootanky.champions import Yone
from tootanky.item_factory import CloakofAgility, InfinityEdge


def test_yone_passive():
    dummy = Dummy(bonus_resistance=20)
    yone = Yone(inventory=[CloakofAgility(), CloakofAgility(), InfinityEdge()])
    assert yone.crit_chance == 1
    assert round(yone.crit_damage, 2) == 0.89 - 0.75
    assert round(yone.attack_damage) == 140
    assert round(yone.auto_attack.damage(target=dummy, is_crit=True), 1) == 220.5
