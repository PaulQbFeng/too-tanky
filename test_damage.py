import math
from damage import damage_normal_auto_attack_no_crit
from damage import damage_normal_auto_attack_with_crit
from damage import damage_empowered_auto_attack_no_crit
from damage import damage_empowered_auto_attack_with_crit


def test_auto_attack_cait_lvl11_ie():
    assert math.floor(damage_normal_auto_attack_no_crit(attack_base_ad=75, attack_bonus_ad=95, attack_lethality=0,
                                                        attack_level=11, attack_armor_pen=0, attack_bonus_armor_pen=0,
                                                        defense_base_armor=60, defense_bonus_armor=0)) == 107
    assert math.floor(damage_normal_auto_attack_with_crit(attack_base_ad=75, attack_bonus_ad=95,
                                                          attack_bonus_crit_damage=0, attack_lethality=0,
                                                          attack_level=11, attack_armor_pen=0, attack_bonus_armor_pen=0,
                                                          defense_base_armor=60, defense_bonus_armor=0)) == 187