class Stats:
    """
    Champions, items, and rune shards can all be considered to have stats.
    Stats in league all have a fixed way of being stacked, hence why it makes sense to define a class.
    """
    def __init__(self):
        self.health = 0
        self.mana = 0
        self.health_regen = 0
        self.mana_regen = 0
        self.attack_damage = 0
        self.ability_power = 0
        self.attack_speed = 0
        self.armor = 0
        self.magic_resist = 0
        self.lethality = 0
        self.armor_pen_percent = 0
        self.bonus_armor_pen_percent = 0
        self.magic_pen_flat = 0
        self.magic_pen_percent = 0
        self.crit_chance = 0
        self.crit_damage = 0
        self.life_steal = 0
        self.omni_vamp = 0
        self.spell_vamp = 0
        self.debuff_list = []

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def add_stats(self, stats):
        self.health += stats.health
        self.mana += stats.mana
        self.health_regen += stats.health_regen
        self.mana_regen += stats.mana_regen
        self.attack_damage += stats.attack_damage
        self.ability_power += stats.ability_power
        self.attack_speed += stats.attack_speed
        self.armor += stats.armor
        self.magic_resist += stats.magic_resist
        self.lethality += stats.lethality
        self.armor_pen_percent = 1 - (1 - self.armor_pen_percent) * (1 - stats.armor_pen_percent)
        self.bonus_armor_pen_percent = 1 - (1 - self.bonus_armor_pen_percent) * (1 - stats.bonus_armor_pen_percent)
        self.magic_pen_flat += stats.magic_pen_flat
        self.magic_pen_percent = 1 - (1 - self.magic_pen_percent) * (1 - stats.magic_pen_percent)
        self.crit_chance += stats.crit_chance
        self.crit_damage += stats.crit_damage
        self.life_steal += stats.life_steal
        self.omni_vamp += stats.omni_vamp
        self.spell_vamp += stats.spell_vamp