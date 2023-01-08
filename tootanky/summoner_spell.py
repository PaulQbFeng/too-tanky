from tootanky.attack import BaseDamageMixin


class BaseSummonerSpell(BaseDamageMixin):
    """
    Some class variables that can be overwritten in the subclasses:
        - spell_key: q, w, e, r (default=None)
        - damage_type: physical, magical (default=None)
        - apply_on_hit: If the spell can apply on_hit (default=False)
        - can_trigger_spellblade: If the spell can activate spellblade effect (default=True)

    Not all spell specifications are included in the data file which means there is a need to double check
    the current specs + add the missing ones inside the subclass of BaseSpell.
    """

    name = None
    base_cooldown = None
    range = None

    def __init__(self, champion):
        self.champion = champion

    @property
    def cooldown(self):
        return self.base_cooldown * 100 / (100 + self.champion.ability_haste)
