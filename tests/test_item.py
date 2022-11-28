from champion import Dummy
from champions import Ahri, Annie
from damage import damage_after_positive_resistance
from item import ALL_ITEM_CLASSES, DoranBlade, Sheen


def test_DoranBlade():
    doranblade = DoranBlade()
    assert doranblade.stats._dict == {"attack_damage": 8, "health": 80}


def test_Sheen():
    sheen = Sheen()
    annie = Annie()
    dummy = Dummy(health=1000, bonus_resistance=50)
    assert sheen.spellblade(annie, dummy) == damage_after_positive_resistance(
        annie.base_attack_damage, dummy.bonus_armor
    )


def test_serrated_unique_passive():
    item_names = ["Serrated Dirk", "Last Whisper"]
    inventory = [ALL_ITEM_CLASSES[item_name]() for item_name in item_names]
    ahri = Ahri(level=7, inventory=inventory)

    assert ahri.orig_bonus_stats.attack_damage == 50
    assert ahri.orig_bonus_stats.lethality == 10
    assert ahri.orig_bonus_stats.armor_pen_percent == 18

    ahri.equip_item(ALL_ITEM_CLASSES["Serrated Dirk"]())

    assert ahri.orig_bonus_stats.attack_damage == 80
    assert ahri.orig_bonus_stats.lethality == 10
    assert ahri.orig_bonus_stats.armor_pen_percent == 18
