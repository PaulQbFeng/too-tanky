from tootanky.attack import BaseDamageMixin


class BaseSummonerSpell(BaseDamageMixin):
    """
    Some class variables that can be overwritten in the subclasses:
        - name: name of the summoner spell
        - base_cooldown
        - sum spell range

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
