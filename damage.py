# TODO: it seems that hp are ceiled while damage floored. (however it seems that the ad is rounded in the stat section ingame)

def damage_ad_armor(attack_ad: float, defense_armor: float):
    """
    Calculates the output damage of an auto attack from a champion with X amount of 
    attack damage on a champion with Y amount of armor.
    """
    return attack_ad * 100 / (100 + defense_armor)


def damage_normal_auto_attack_no_crit(attack_base_ad: float, attack_bonus_ad: float, attack_lethality: float,
                                      attack_level: int, attack_armor_pen: float, attack_bonus_armor_pen: float,
                                      defense_base_armor: float, defense_bonus_armor: float):
    """
    Calculates the output damage of an auto attack that doesn't crit
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mitigation_damage = attack_base_ad + attack_bonus_ad
    defense_armor = defense_base_armor + defense_bonus_armor
    if defense_armor < 0:
        return pre_mitigation_damage * (2 - 100 / (100 - defense_armor))
    else:
        attack_flat_armor_pen = attack_lethality * (0.6 + 0.4 * attack_level / 18)
        armor_eq = defense_base_armor * (1 - attack_armor_pen) + defense_bonus_armor * (1 - attack_armor_pen) * (
                1 - attack_bonus_armor_pen)
        armor_eq = armor_eq - attack_flat_armor_pen
        if armor_eq < 0:
            armor_eq = 0
        return pre_mitigation_damage * 100 / (100 + armor_eq)

def damage_normal_auto_attack_with_crit(attack_base_ad: float, attack_bonus_ad: float, attack_bonus_crit_damage: float,
                                        attack_lethality: float, attack_level: int, attack_armor_pen: float,
                                        attack_bonus_armor_pen: float, defense_base_armor: float,
                                        defense_bonus_armor: float):
    """
    Calculates the output damage of an auto attack that crits
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mitigation_damage = (attack_base_ad + attack_bonus_ad) * (1.75 + attack_bonus_crit_damage)
    defense_armor = defense_base_armor + defense_bonus_armor
    if defense_armor < 0:
        return pre_mitigation_damage * (2 - 100 / (100 - defense_armor))
    else:
        attack_flat_armor_pen = attack_lethality * (0.6 + 0.4 * attack_level / 18)
        armor_eq = defense_base_armor * (1 - attack_armor_pen) + defense_bonus_armor * (1 - attack_armor_pen) * (
                1 - attack_bonus_armor_pen)
        armor_eq = armor_eq - attack_flat_armor_pen
        if armor_eq < 0:
            armor_eq = 0
        return pre_mitigation_damage * 100 / (100 + armor_eq)

def avg_damage_normal_auto_attack(attack_base_ad: float, attack_bonus_ad: float, attack_crit_chance: float,
                                  attack_bonus_crit_damage: float, attack_lethality: float, attack_level: int,
                                  attack_armor_pen: float, attack_bonus_armor_pen: float, defense_base_armor: float,
                                  defense_bonus_armor: float):
    """
    Calculates the average output damage of an autoattack based on crit chance
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mitigation_damage = (attack_base_ad + attack_bonus_ad) * (
            1 + attack_crit_chance * (0.75 + attack_bonus_crit_damage))
    defense_armor = defense_base_armor + defense_bonus_armor
    if defense_armor < 0:
        return pre_mitigation_damage * (2 - 100 / (100 - defense_armor))
    else:
        attack_flat_armor_pen = attack_lethality * (0.6 + 0.4 * attack_level / 18)
        armor_eq = defense_base_armor * (1 - attack_armor_pen) + defense_bonus_armor * (1 - attack_armor_pen) * (
                1 - attack_bonus_armor_pen)
        armor_eq = armor_eq - attack_flat_armor_pen
        if armor_eq < 0:
            armor_eq = 0
        return pre_mitigation_damage * 100 / (100 + armor_eq)

def damage_empowered_auto_attack_no_crit(attack_base_ad: float, attack_bonus_ad: float, attack_lethality: float,
                                         attack_level: int, attack_armor_pen: float, attack_bonus_armor_pen: float,
                                         defense_base_armor: float, defense_bonus_armor: float,
                                         flat_AD_increase: float, percentage_AD_increase: float,
                                         percentage_bonus_AD_increase: float):
    """
    Calculates the output damage of a non-crit empowered auto attack (from a spell, passive or item)
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mitigation_damage = attack_base_ad * (1 + percentage_AD_increase) + attack_bonus_ad * (1 + percentage_AD_increase) * (1 + percentage_bonus_AD_increase) + flat_AD_increase
    defense_armor = defense_base_armor + defense_bonus_armor
    if defense_armor < 0:
        return pre_mitigation_damage * (2 - 100 / (100 - defense_armor))
    else:
        attack_flat_armor_pen = attack_lethality * (0.6 + 0.4 * attack_level / 18)
        armor_eq = defense_base_armor * (1 - attack_armor_pen) + defense_bonus_armor * (1 - attack_armor_pen) * (
                1 - attack_bonus_armor_pen)
        armor_eq = armor_eq - attack_flat_armor_pen
        if armor_eq < 0:
            armor_eq = 0
        return pre_mitigation_damage * 100 / (100 + armor_eq)

def damage_empowered_auto_attack_with_crit(attack_base_ad: float, attack_bonus_ad: float,
                                           attack_bonus_crit_damage: float, attack_lethality: float, attack_level: int,
                                           attack_armor_pen: float, attack_bonus_armor_pen: float,
                                           defense_base_armor: float, defense_bonus_armor: float,
                                           flat_AD_increase: float, percentage_AD_increase: float,
                                           percentage_bonus_AD_increase: float):
    """
    Calculates the output damage of a crit empowered auto attack (from a spell, passive or item)
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mitigation_damage = attack_base_ad * (1.75 + attack_bonus_crit_damage) * (1 + percentage_AD_increase) + attack_bonus_ad * (1.75 + attack_bonus_crit_damage) * (1 + percentage_AD_increase) * (1 + percentage_bonus_AD_increase) + flat_AD_increase
    defense_armor = defense_base_armor + defense_bonus_armor
    if defense_armor < 0:
        return pre_mitigation_damage * (2 - 100 / (100 - defense_armor))
    else:
        attack_flat_armor_pen = attack_lethality * (0.6 + 0.4 * attack_level / 18)
        armor_eq = defense_base_armor * (1 - attack_armor_pen) + defense_bonus_armor * (1 - attack_armor_pen) * (
                1 - attack_bonus_armor_pen)
        armor_eq = armor_eq - attack_flat_armor_pen
        if armor_eq < 0:
            armor_eq = 0
        return pre_mitigation_damage * 100 / (100 + armor_eq)

def avg_damage_empowered_auto_attack(attack_base_ad: float, attack_bonus_ad: float, attack_crit_chance: float,
                                     attack_bonus_crit_damage, attack_lethality: float, attack_level: int,
                                     attack_armor_pen: float, attack_bonus_armor_pen: float, defense_base_armor: float,
                                     defense_bonus_armor: float, flat_AD_increase: float, percentage_AD_increase: float,
                                     percentage_bonus_AD_increase: float):
    """
    Calculates the average output damage of an empowered auto attack (from a spell, passive or item) based on crit chance
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mitigation_damage = attack_base_ad * (1 + attack_crit_chance * (0.75 + attack_bonus_crit_damage)) * (1 + percentage_AD_increase) + attack_bonus_ad * (1 + attack_crit_chance * (0.75 + attack_bonus_crit_damage)) * (1 + percentage_AD_increase) * (1 + percentage_bonus_AD_increase) + flat_AD_increase
    defense_armor = defense_base_armor + defense_bonus_armor
    if defense_armor < 0:
        return pre_mitigation_damage * (2 - 100 / (100 - defense_armor))
    else:
        attack_flat_armor_pen = attack_lethality * (0.6 + 0.4 * attack_level / 18)
        armor_eq = defense_base_armor * (1 - attack_armor_pen) + defense_bonus_armor * (1 - attack_armor_pen) * (
                1 - attack_bonus_armor_pen)
        armor_eq = armor_eq - attack_flat_armor_pen
        if armor_eq < 0:
            armor_eq = 0
        return pre_mitigation_damage * 100 / (100 + armor_eq)