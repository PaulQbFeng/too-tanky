import math

from champion import Ahri, Annie, Dummy
from damage import damage_after_positive_resistance
from item import DoranBlade, Sheen


def test_DoranBlade():
    doranblade = DoranBlade()
    assert doranblade.stats == {"attack_damage": 8, "health": 80, "gold": 450}


def test_Sheen():
    sheen = Sheen()
    annie = Annie()
    dummy = Dummy(health=1000, bonus_resistance=50)
    assert sheen.spellblade(annie, dummy) == damage_after_positive_resistance(
        annie.orig_base_stats["attack_damage"], dummy.orig_bonus_stats["armor"]
    )


def test_serrated_unique_passive():
    items = ["Serrated Dirk", "Last Whisper"]
    ahri = Ahri(level=7, item_names=items)

    assert ahri.orig_bonus_stats["attack_damage"] == 50
    assert ahri.orig_bonus_stats["lethality"] == 10
    assert ahri.orig_bonus_stats["armor_pen_percent"] == 18

    ahri.equip_item("Serrated Dirk")

    assert ahri.orig_bonus_stats["attack_damage"] == 80
    assert ahri.orig_bonus_stats["lethality"] == 10
    assert ahri.orig_bonus_stats["armor_pen_percent"] == 18
