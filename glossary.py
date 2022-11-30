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
    "attackspeed": "attack_speed"
}

MAPPING_ITEM_STANDARD = {
    'FlatMovementSpeedMod': 'move_speed',
    'FlatHPPoolMod':'health',
    'FlatCritChanceMod':'crit_chance',
    'FlatMagicDamageMod':'ability_power',
    'FlatMPPoolMod':'mana',
    'FlatArmorMod':'armor',
    'FlatSpellBlockMod': 'magic_resist',
    'FlatPhysicalDamageMod':  'attack_damage',
    'PercentAttackSpeedMod': 'attack_speed',
    'PercentLifeStealMod':'life_steal',
    'FlatHPRegenMod':  'health_regen',
    'PercentMovementSpeedMod':  'move_speed_percent',
    "gold": "gold"
}

DEFAULT_STAT_LIST = [
    "health",
    "mana",
    "movespeed",
    "armor",
    "magic_resist",
    "attack_range",
    "health_regen",
    "mana_regen",
    "attack_damage",
    "ability_power",
    "attack_speed",
]

EXTRA_STAT_LIST = [
    "lethality",
    "crit_damage", 
    "magic_pen_flat",
    "magic_pen_percent",
    "armor_pen_flat",
    "armor_pen_percent",
    "bonus_armor_pen_percent"
    "life_steal",
    "crit_chance",
]
