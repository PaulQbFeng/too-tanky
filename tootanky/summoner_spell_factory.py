from tootanky.summoner_spell import BaseSummonerSpell


class Ignite(BaseSummonerSpell):
    """
    Some class variables that can be overwritten in the subclasses:
        - spell_key: q, w, e, r (default=None)
        - damage_type: physical, magical (default=None)
        - apply_on_hit: If the spell can apply on_hit (default=False)
        - can_trigger_spellblade: If the spell can activate spellblade effect (default=True)

    Not all spell specifications are included in the data file which means there is a need to double check
    the current specs + add the missing ones inside the subclass of BaseSpell.
    """

    name = "ignite"
    damage_type = "true"
    base_cooldown = 180
    range = 600
    ratios = []

    def __init__(self, champion):
        self.champion = champion

    def get_base_damage(self):
        return 10 + 4 * self.champion.level

    def damage(self, target, number_of_ticks=5):

        total_damage = 0

        for _ in range(number_of_ticks):
            damage_modifier_flat = self.get_damage_modifier_flat()
            damage_modifier_coeff = self.get_damage_modifier_coeff()
            total_damage += self._compute_damage(target, damage_modifier_flat, damage_modifier_coeff)

        return total_damage


ALL_SUMMONER_SPELLS = {cls.name: cls for cls in BaseSummonerSpell.__subclasses__()}
