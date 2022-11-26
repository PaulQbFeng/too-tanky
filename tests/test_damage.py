import math

from champion import Dummy
from damage import damage_physical_auto_attack


def tests_normal_auto_attack_cait_dummy_60():
    """
    Tests of caitlyn autoattacks (non-crits and crits) without her passive (Headshot) at different levels and with
    different items against a dummy with 60 bonus armor and 60 bonus mr
    Caitlyn has one adaptive force rune which gives 5.4 attack damage
    """
    dummy_60 = Dummy(health=1000, bonus_resistance=60)
    # Caitlyn level 1 with a doran's blade
    # No headshot no crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=62,
                bonus_attack_damage=13.4,
                lethality=0,
                attacker_level=1,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_60.orig_base_stats.armor,
                bonus_armor=dummy_60.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 47
    )
    # Caitlyn level 11 with an infinity edge
    # No headshot no crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=75.4,
                lethality=0,
                attacker_level=11,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_60.orig_base_stats.armor,
                bonus_armor=dummy_60.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 107
    )
    # No headshot with crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=75.4,
                lethality=0,
                attacker_level=11,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_60.orig_base_stats.armor,
                bonus_armor=dummy_60.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=True,
                crit_damage=0,
            )
        )
        == 187
    )
    # Caitlyn level 11 with an infinity edge and a lord dominik's regards
    # No headshot no crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=105.4,
                lethality=0,
                attacker_level=11,
                armor_pen=30,
                bonus_armor_pen=0,
                base_armor=dummy_60.orig_base_stats.armor,
                bonus_armor=dummy_60.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 141
    )
    # No headshot with crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=105.4,
                lethality=0,
                attacker_level=11,
                armor_pen=30,
                bonus_armor_pen=0,
                base_armor=dummy_60.orig_base_stats.armor,
                bonus_armor=dummy_60.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=True,
                crit_damage=0,
            )
        )
        == 247
    )
    # Caitlyn level 11 with a duskblade of draktharr (and cloak of agility for crits)
    # No headshot no crit no duskblade effect
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=65.4,
                lethality=18,
                attacker_level=11,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_60.orig_base_stats.armor,
                bonus_armor=dummy_60.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 111
    )
    # No headshot with crit no duskblade effect
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=65.4,
                lethality=18,
                attacker_level=11,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_60.orig_base_stats.armor,
                bonus_armor=dummy_60.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=True,
                crit_damage=0,
            )
        )
        == 194
    )
    # Caitlyn level 11 with a duskblade of draktharr and lord dominik's regards
    # No headshot no crit no duskblade effect
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=95.4,
                lethality=18,
                attacker_level=11,
                armor_pen=30,
                bonus_armor_pen=0,
                base_armor=dummy_60.orig_base_stats.armor,
                bonus_armor=dummy_60.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 150
    )
    # No headshot with crit no duskblade effect
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=95.4,
                lethality=18,
                attacker_level=11,
                armor_pen=30,
                bonus_armor_pen=0,
                base_armor=dummy_60.orig_base_stats.armor,
                bonus_armor=dummy_60.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=True,
                crit_damage=0,
            )
        )
        == 263
    )


def tests_normal_auto_attack_cait_dummy_10():
    """
    Same against a dummy with 10 bonus armor and 10 bonus mr (to test what happens when lethality is higher than armor)
    Caitlyn has one adaptive force rune which gives 5.4 attack damage
    """
    dummy_10 = Dummy(health=1000, bonus_resistance=10)
    # Caitlyn level 1 with a doran's blade
    # No headshot no crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=62,
                bonus_attack_damage=13.4,
                lethality=0,
                attacker_level=1,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_10.orig_base_stats.armor,
                bonus_armor=dummy_10.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 69
    )
    # Caitlyn level 11 with an infinity edge
    # No headshot no crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=75.4,
                lethality=0,
                attacker_level=11,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_10.orig_base_stats.armor,
                bonus_armor=dummy_10.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 155
    )
    # No headshot with crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=75.4,
                lethality=0,
                attacker_level=11,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_10.orig_base_stats.armor,
                bonus_armor=dummy_10.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=True,
                crit_damage=0,
            )
        )
        == 272
    )
    # Caitlyn level 11 with an infinity edge and a lord dominik's regards
    # No headshot no crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=105.4,
                lethality=0,
                attacker_level=11,
                armor_pen=30,
                bonus_armor_pen=0,
                base_armor=dummy_10.orig_base_stats.armor,
                bonus_armor=dummy_10.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 188
    )
    # No headshot with crit
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=105.4,
                lethality=0,
                attacker_level=11,
                armor_pen=30,
                bonus_armor_pen=0,
                base_armor=dummy_10.orig_base_stats.armor,
                bonus_armor=dummy_10.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=True,
                crit_damage=0,
            )
        )
        == 328
    )
    # Caitlyn level 11 with a duskblade of draktharr (and cloak of agility for crits)
    # No headshot no crit no duskblade effect
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=65.4,
                lethality=18,
                attacker_level=11,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_10.orig_base_stats.armor,
                bonus_armor=dummy_10.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 161
    )
    # No headshot with crit no duskblade effect
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=65.4,
                lethality=18,
                attacker_level=11,
                armor_pen=0,
                bonus_armor_pen=0,
                base_armor=dummy_10.orig_base_stats.armor,
                bonus_armor=dummy_10.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=True,
                crit_damage=0,
            )
        )
        == 281
    )
    # Caitlyn level 11 with a duskblade of draktharr and lord dominik's regards
    # No headshot no crit no duskblade effect
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=95.4,
                lethality=18,
                attacker_level=11,
                armor_pen=30,
                bonus_armor_pen=0,
                base_armor=dummy_10.orig_base_stats.armor,
                bonus_armor=dummy_10.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=False,
                crit_damage=0,
            )
        )
        == 191
    )
    # No headshot with crit no duskblade effect
    assert (
        round(
            damage_physical_auto_attack(
                base_attack_damage=95.345,
                bonus_attack_damage=95.4,
                lethality=18,
                attacker_level=11,
                armor_pen=30,
                bonus_armor_pen=0,
                base_armor=dummy_10.orig_base_stats.armor,
                bonus_armor=dummy_10.orig_bonus_stats.armor,
                damage_modifier_flat=0,
                damage_modifier_percent=0,
                crit=True,
                crit_damage=0,
            )
        )
        == 334
    )
