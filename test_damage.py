import math
from damage import damage_normal_auto_attack_no_crit
from damage import damage_normal_auto_attack_with_crit
from damage import damage_empowered_auto_attack_no_crit
from damage import damage_empowered_auto_attack_with_crit
from champion import Dummy


def tests_normal_auto_attack_cait_dummy_60():
    """
    Tests of caitlyn autoattacks (non-crits and crits) without her passive (Headshot) at different levels and with
    different items against a dummy with 60 bonus armor and 60 bonus mr
    Caitlyn has one adaptive force rune which gives 5.4 attack damage
    """
    dummy_60 = Dummy(1000, 60, 60)
    # Caitlyn level 1 with a doran's blade
    assert round(damage_normal_auto_attack_no_crit(attack_base_ad=62, attack_bonus_ad=13.4, attack_lethality=0,
                                                   attack_level=1, attack_armor_pen=0, attack_bonus_armor_pen=0,
                                                   defense_base_armor=dummy_60.armor,
                                                   defense_bonus_armor=dummy_60.bonus_armor)) == 47
    # Caitlyn level 11 with an infinity edge
    assert round(damage_normal_auto_attack_no_crit(attack_base_ad=95.345, attack_bonus_ad=75.4, attack_lethality=0,
                                                   attack_level=11, attack_armor_pen=0, attack_bonus_armor_pen=0,
                                                   defense_base_armor=dummy_60.armor,
                                                   defense_bonus_armor=dummy_60.bonus_armor)) == 107
    assert round(damage_normal_auto_attack_with_crit(attack_base_ad=95.345, attack_bonus_ad=75.4,
                                                     attack_bonus_crit_damage=0, attack_lethality=0,
                                                     attack_level=11, attack_armor_pen=0, attack_bonus_armor_pen=0,
                                                     defense_base_armor=dummy_60.armor,
                                                     defense_bonus_armor=dummy_60.bonus_armor)) == 187
    # Caitlyn level 11 with an infinity edge and a lord dominik's regards
    assert round(damage_normal_auto_attack_no_crit(attack_base_ad=95.345, attack_bonus_ad=105.4, attack_lethality=0,
                                                   attack_level=11, attack_armor_pen=0.3, attack_bonus_armor_pen=0,
                                                   defense_base_armor=dummy_60.armor,
                                                   defense_bonus_armor=dummy_60.bonus_armor)) == 141
    assert round(damage_normal_auto_attack_with_crit(attack_base_ad=95.345, attack_bonus_ad=105.4,
                                                     attack_bonus_crit_damage=0, attack_lethality=0,
                                                     attack_level=11, attack_armor_pen=0.3, attack_bonus_armor_pen=0,
                                                     defense_base_armor=dummy_60.armor,
                                                     defense_bonus_armor=dummy_60.bonus_armor)) == 247
    # Caitlyn level 11 with a duskblade of draktharr (and cloak of agility for crits)
    assert round(damage_normal_auto_attack_no_crit(attack_base_ad=95.345, attack_bonus_ad=65.4, attack_lethality=18,
                                                   attack_level=11, attack_armor_pen=0, attack_bonus_armor_pen=0,
                                                   defense_base_armor=dummy_60.armor,
                                                   defense_bonus_armor=dummy_60.bonus_armor)) == 111
    assert round(damage_normal_auto_attack_with_crit(attack_base_ad=95.345, attack_bonus_ad=65.4,
                                                     attack_bonus_crit_damage=0, attack_lethality=18, attack_level=11,
                                                     attack_armor_pen=0, attack_bonus_armor_pen=0,
                                                     defense_base_armor=dummy_60.armor,
                                                     defense_bonus_armor=dummy_60.bonus_armor)) == 194
    # Caitlyn level 11 with a duskblade of draktharr and lord dominik's regards
    assert round(damage_normal_auto_attack_no_crit(attack_base_ad=95.345, attack_bonus_ad=95.4, attack_lethality=18,
                                                   attack_level=11, attack_armor_pen=0.3, attack_bonus_armor_pen=0,
                                                   defense_base_armor=dummy_60.armor,
                                                   defense_bonus_armor=dummy_60.bonus_armor)) == 150
    assert round(damage_normal_auto_attack_with_crit(attack_base_ad=95.345, attack_bonus_ad=95.4,
                                                     attack_bonus_crit_damage=0, attack_lethality=18, attack_level=11,
                                                     attack_armor_pen=0.3, attack_bonus_armor_pen=0,
                                                     defense_base_armor=dummy_60.armor,
                                                     defense_bonus_armor=dummy_60.bonus_armor)) == 263
