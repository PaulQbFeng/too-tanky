MAPPING_CHAMPION_STANDARD = {
    "hp": "health",
    "hpperlevel": "health_perlevel",
    "mp": "mana",
    "mpperlevel": "mana_perlevel",
    "movespeed": "move_speed",
    "armor": "armor",
    "armorperlevel": "armor_perlevel",
    "spellblock": "magic_resist",
    "spellblockperlevel": "magic_resist_perlevel",
    "attackrange": "attack_range",
    "hpregen": "health_regen",
    "hpregenperlevel": "health_regen_perlevel",
    "mpregen": "mana_regen",
    "mpregenperlevel": "mana_regen_perlevel",
    "crit": "crit_chance",
    "critperlevel": "crit_chance_perlevel",
    "attackdamage": "attack_damage",
    "attackdamageperlevel": "attack_damage_perlevel",
    "attackspeedperlevel": "attack_speed_perlevel",
    "attackspeed": "attack_speed",
}

MAPPING_ITEM_STANDARD = {
    "FlatMovementSpeedMod": "move_speed_flat",
    "FlatHPPoolMod": "health",
    "FlatCritChanceMod": "crit_chance",
    "FlatMagicDamageMod": "ability_power",
    "FlatMPPoolMod": "mana",
    "FlatArmorMod": "armor",
    "FlatSpellBlockMod": "magic_resist",
    "FlatPhysicalDamageMod": "attack_damage",
    "PercentAttackSpeedMod": "attack_speed",
    "PercentLifeStealMod": "life_steal",
    "FlatHPRegenMod": "health_regen",
    "PercentMovementSpeedMod": "move_speed_percent",
    "gold": "gold",
}

STAT_SUM_BASE_BONUS = [
    "health",
    "mana",
    "attack_range",
    "health_regen",
    "mana_regen",
]

STAT_STANDALONE = [
    "lethality",
    "crit_chance",
    "crit_damage",
    "life_steal",
    "omni_vamp",
    "spell_vamp",
    "bonus_armor_pen_percent"
]

STAT_TOTAL_PROPERTY = [
    "armor",
    "magic_resist",
    "attack_damage",
    "attack_speed",
    "move_speed",
    "ability_power"
]

STAT_FLAT_PERCENT = [
    "armor_pen",
    "magic_resist_pen",
    "move_speed"
]

STAT_UNDERLYING_PROPERTY = []


def normalize_champion_name(name):
    """Champion name are different in champion / spell / item json files"""
    # TODO: normalize everything
    return name.replace(" ", "")
