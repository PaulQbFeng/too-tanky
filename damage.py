# TODO: it seems that hp are ceiled while damage floored. (however it seems that the ad is rounded in the stat section ingame)

def pre_mitigation_physical_damage(base_attack_damage: float, bonus_attack_damage: float, damage_modifier_flat: float,
                                   damage_modifier_percent_mult_factor: float, crit: 'bool', crit_damage: float):
    """
    Calculates the pre-mitigation physical damage of a spell or an autoattack
    All values regarding damage modifiers should include the buffs/debuffs coming from spells, summoner spells, or items
    from both the attacker AND the defender
    """
    if crit:
        return (base_attack_damage + bonus_attack_damage) * damage_modifier_percent_mult_factor * (
                    1.75 + crit_damage) + damage_modifier_flat
    return (base_attack_damage + bonus_attack_damage) * damage_modifier_percent_mult_factor + damage_modifier_flat


def avg_pre_mitigation_physical_damage(base_attack_damage: float, bonus_attack_damage: float,
                                       damage_modifier_flat: float, damage_modifier_percent_mult_factor: float,
                                       crit_chance: float, crit_damage: float):
    """
    Calculates the pre-mitigation physical damage AVERAGE (based on crit chance) of a spell or an autoattack.
    This is only relevant for damage sources that can crit.
    All values regarding damage modifiers should include the buffs/debuffs coming from spells, summoner spells, or items
    from both the attacker AND the defender
    """
    return (base_attack_damage + bonus_attack_damage) * damage_modifier_percent_mult_factor * (
                1 + crit_chance * (0.75 + crit_damage)) + damage_modifier_flat


def damage_after_positive_resistance(pre_mitigation_damage: float, resistance: float):
    """
    Calculates the output damage if X amount of pre-mitigation physical damage is dealt to a champion with Y amount of
    armor (positive)
    """
    return pre_mitigation_damage * 100 / (100 + resistance)


def damage_after_negative_resistance(pre_mitigation_damage: float, resistance: float):
    """
    Calculates the output damage if X amount of pre-mitigation physical damage is dealt to a champion with negative
    armor.
    """
    return pre_mitigation_damage * (2 - 100 / (100 - resistance))


def physical_damage_after_armor(pre_mitigation_damage: float, lethality: float, attacker_level: int,
                                armor_pen_percent: float, bonus_armor_pen_percent: float,
                                base_armor: float, bonus_armor: float):
    """
    Calculates the output damage if X amount of pre-mitigation physical damage is dealt to a champion with Y amount of armor
    """
    defense_armor = base_armor + bonus_armor
    if defense_armor < 0:
        return damage_after_negative_resistance(pre_mitigation_damage, defense_armor)
    else:
        flat_armor_pen = lethality * (0.6 + 0.4 * attacker_level / 18)
        armor_eq = base_armor * (1 - armor_pen_percent) + bonus_armor * (1 - armor_pen_percent) * (1 - bonus_armor_pen_percent)
        armor_eq -= flat_armor_pen
        armor_eq = max(armor_eq, 0)
        return damage_after_positive_resistance(pre_mitigation_damage, armor_eq)


def damage_auto_attack(base_attack_damage: float, bonus_attack_damage: float, lethality: float, attacker_level: int,
                       armor_pen_percent: float, bonus_armor_pen_percent: float, base_armor: float,
                       bonus_armor: float, damage_modifier_flat: float, damage_modifier_percent_mult_factor: float,
                       crit: 'bool', crit_damage: float):
    """
    Calculates the output damage of crit/non-crit, empowered/modified/normal auto attacks
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mitigation_damage = pre_mitigation_physical_damage(base_attack_damage, bonus_attack_damage,
                                                           damage_modifier_flat, damage_modifier_percent_mult_factor,
                                                           crit, crit_damage)
    return physical_damage_after_armor(pre_mitigation_damage, lethality, attacker_level,
                                       armor_pen_percent, bonus_armor_pen_percent,
                                       base_armor, bonus_armor)


def avg_damage_auto_attack(base_attack_damage: float, bonus_attack_damage: float, lethality: float,
                           attacker_level: int, armor_pen_percent: float, bonus_armor_pen_percent: float,
                           base_armor: float, bonus_armor: float, damage_modifier_flat: float,
                           damage_modifier_percent_mult_factor: float, crit_chance: float, crit_damage: float):
    """
    Calculates the average output damage of an autoattack based on crit chance
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mitigation_damage = avg_pre_mitigation_physical_damage(base_attack_damage, bonus_attack_damage,
                                                               damage_modifier_flat, damage_modifier_percent_mult_factor
                                                               , crit_chance, crit_damage)
    return physical_damage_after_armor(pre_mitigation_damage, lethality, attacker_level,
                                       armor_pen_percent, bonus_armor_pen_percent,
                                       base_armor, bonus_armor)

