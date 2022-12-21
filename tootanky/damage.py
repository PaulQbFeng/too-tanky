# COMMENTS
# HP are ceiled, damage are floored.
# However damage displayed in white on dummys is rounded
# Champions stats are rounded


def pre_mitigation_auto_attack_damage(
    base_offensive_stats: float,
    bonus_offensive_stats: float,
    damage_modifier_flat: float = 0,
    damage_modifier_coeff: float = 1,
    crit: bool = False,
    crit_damage: float = 0,
):
    """
    Calculates the pre-mitigation damage of a spell or an autoattack
    All values regarding damage modifiers should include the buffs/debuffs coming from spells, summoner spells, or items
    from both the attacker AND the defender
    """
    tot_off_stats = base_offensive_stats + bonus_offensive_stats

    if crit:
        crit_multiplier = 1.75 + crit_damage
    else:
        crit_multiplier = 1

    return (tot_off_stats * crit_multiplier + damage_modifier_flat) * damage_modifier_coeff


def ratio_stat(champion, target, ratios, spell_level=1) -> float:
    """Get the damage dealt by the ratio part of a spell, taking into account multiple ratios"""
    stat = 0
    for stat_name, ratio in ratios:
        if "target_" in stat_name:
            stat_value = getattr(target, stat_name.replace("target_", ""))
        else:
            stat_value = getattr(champion, stat_name)
        if isinstance(ratio, list):
            ratio = ratio[spell_level - 1]
        stat += stat_value * ratio
    return stat


def pre_mitigation_spell_damage(
    base_spell_damage: float,
    ratio_damage: float,
    damage_modifier_flat: float = 0,
    damage_modifier_coeff: float = 1,
):
    """
    Calculates the pre-mitigation damage of a spell or an autoattack
    All values regarding damage modifiers should include the buffs/debuffs coming from spells, summoner spells, or items
    from both the attacker AND the defender.
    :param: ratio_damage is damage that scales with the champion's or target's stat
    """
    return (base_spell_damage + ratio_damage + damage_modifier_flat) * damage_modifier_coeff


def avg_pre_mitigation_auto_attack_damage(
    base_attack_damage: float,
    bonus_attack_damage: float,
    damage_modifier_flat: float = 0,
    damage_modifier_coeff: float = 1,
    crit_chance: float = 0,
    crit_damage: float = 0,
):
    """
    Calculates the pre-mitigation autoattack damage AVERAGE (based on crit chance) of a spell or an autoattack.
    This is only relevant for damage sources that can crit.
    All values regarding damage modifiers should include the buffs/debuffs coming from spells, summoner spells, or items
    from both the attacker AND the defender
    """
    tot_off_stats = base_attack_damage + bonus_attack_damage

    return tot_off_stats * damage_modifier_coeff * (1 + crit_chance * (0.75 + crit_damage)) + damage_modifier_flat


def damage_after_positive_resistance(pre_mitigation_auto_attack_damage: float, resistance: float):
    """
    Calculates the output damage if X amount of pre-mitigation physical damage is dealt to a champion with Y amount of
    armor (positive)
    """
    return pre_mitigation_auto_attack_damage * 100 / (100 + resistance)


def damage_after_negative_resistance(pre_mitigation_auto_attack_damage: float, resistance: float):
    """
    Calculates the output damage if X amount of pre-mitigation physical damage is dealt to a champion with negative
    armor.
    """
    return pre_mitigation_auto_attack_damage * (2 - 100 / (100 - resistance))


def get_flat_armor_pen_with_lethality(lethality, attacker_level):
    """Compute flat armor pen from lethality and attacker level."""
    return lethality * (0.6 + 0.4 * attacker_level / 18)


def damage_after_resistance(
    pre_mitigation_damage: float,
    base_resistance: float,
    bonus_resistance: float,
    flat_resistance_pen: float,
    resistance_pen: float = 0,
    bonus_resistance_pen: float = 0,
):
    """
    Calculates the output damage if X amount of pre-mitigation damage is dealt to a champion with Y amount of resistance.
    """
    defense_resistance = base_resistance + bonus_resistance
    res_pen_multiplier = 1 - resistance_pen
    bonus_res_pen_multiplier = 1 - bonus_resistance_pen

    if defense_resistance < 0:
        return damage_after_negative_resistance(pre_mitigation_damage, defense_resistance)
    else:
        resistance_eq = (
            base_resistance * res_pen_multiplier + bonus_resistance * res_pen_multiplier * bonus_res_pen_multiplier
        )
        resistance_eq -= flat_resistance_pen
        resistance_eq = max(resistance_eq, 0)
        return damage_after_positive_resistance(pre_mitigation_damage, resistance_eq)


def damage_physical_auto_attack(
    base_attack_damage: float,
    base_armor: float,
    bonus_attack_damage: float = 0,
    bonus_armor: float = 0,
    attacker_level: int = 1,
    lethality: float = 0,
    armor_pen: float = 0,
    bonus_armor_pen: float = 0,
    damage_modifier_flat: float = 0,
    damage_modifier_coeff: float = 1,
    crit: bool = False,
    crit_damage: float = 0,
):
    """
    Calculates the output damage of crit/non-crit, empowered/modified/normal auto attacks
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mtg_dmg = pre_mitigation_auto_attack_damage(
        base_attack_damage,
        bonus_attack_damage,
        damage_modifier_flat,
        damage_modifier_coeff,
        crit,
        crit_damage,
    )
    flat_armor_pen = get_flat_armor_pen_with_lethality(lethality, attacker_level)

    return damage_after_resistance(
        pre_mtg_dmg,
        base_armor,
        bonus_armor,
        flat_armor_pen,
        armor_pen,
        bonus_armor_pen,
    )


def avg_damage_physical_auto_attack(
    base_attack_damage: float,
    bonus_attack_damage: float,
    lethality: float,
    attacker_level: int,
    armor_pen: float,
    bonus_armor_pen: float,
    base_armor: float,
    bonus_armor: float,
    damage_modifier_flat: float,
    damage_modifier_coeff: float,
    crit_chance: float,
    crit_damage: float,
):
    """
    Calculates the average output damage of an autoattack based on crit chance
    The base armor and bonus armor of the champion being attacked should already take into account the flat or
    percentage armor reduction resulting from spells like Garen E, Trundle R, Olaf Q, Corki E, or items like Black Cleaver
    """
    pre_mtg_dmg = avg_pre_mitigation_auto_attack_damage(
        base_attack_damage,
        bonus_attack_damage,
        damage_modifier_flat,
        damage_modifier_coeff,
        crit_chance,
        crit_damage,
    )
    flat_armor_pen = get_flat_armor_pen_with_lethality(lethality, attacker_level)

    return damage_after_resistance(
        pre_mtg_dmg,
        base_armor,
        bonus_armor,
        flat_armor_pen,
        armor_pen,
        bonus_armor_pen,
    )


def get_resistance_type(damage_type: str) -> str:
    """Get resistance type based on spell damage type"""
    # TODO: Might be changed into a dict

    if damage_type == "magical":
        res_type = "magic_resist"
    elif damage_type == "physical":
        res_type = "armor"
    else:
        raise AttributeError(f"spell_damage type {damage_type} not taken into account")

    return res_type
