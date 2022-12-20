from tootanky.champions import Caitlyn
from tootanky.item import FiendishCodex, CaulfieldsWarhammer, WatchfulWardstone, YoumuusGhostblade, CosmicDrive, VigilantWardstone


def test_ability_haste():
    caitlyn = Caitlyn(level=9, inventory=[
        CaulfieldsWarhammer(),
        FiendishCodex(),
        FiendishCodex(),
        YoumuusGhostblade(),
        WatchfulWardstone(),
        CosmicDrive()
    ])
    assert caitlyn.ability_haste == 85
    assert caitlyn.spell_q.level == 5
    assert round(caitlyn.spell_q.cooldown, 2) == 3.24
    assert round(caitlyn.spell_w.cooldown, 2) == 0.27
    assert round(caitlyn.spell_e.cooldown, 2) == 8.65
    assert round(caitlyn.spell_r.cooldown, 2) == 48.65
