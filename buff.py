from stats import Stats


class Buff:
    """
    Buffs/debuffs are status effect that can affect all the damage dealt or taken by a unit, or other stats. They can be
    provided by items, spells, summoner spells, champion abilities.
    In general, positive values indicate a buff, negative values indicate a debuff.
    This includes:
        - stats reduction (spells: corki E, j4 Q, kogmaw Q, trundle Q/R,... items: Black Cleaver)
        - damage modification (spells: amumu passive, vlad R,... summoner spells: exhaust, items: anathema's chains, evenshroud, ...)
        - damage over time as negative health_regen (spells: brand passive, cassio Q, darius passive,... summoner spells: ignite)
    This does not include:
        - crowd control
        - marks (zed R, lux passive, leona passive, nida passive, ...)
    This should later include buff durations, because some buffs are indefinite like amumu E that gives him damage
    damage reduction against physical damage, some last until a certain condition is met like garen passive that stops
    whenever he's hit by a champion, some last only for a precise number of instances (master yi E gives him additional
    true damage for his next auto).
    Most buffs/debuffs are unique and do not stack, however some of them can like Black Cleaver (stacks additively
    despite it being percent armor reduction which stacks multipliticavely in other instances)
    """

    def __init__(self):
        self.base_stats = Stats()
        self.bonus_stats = Stats

    def add_buff(self, buff):
        self.base_stats.add_stats(buff.base_stats)
        self.bonus_stats.add_stats(buff.bonus_stats)

    def apply_buff(self, champion):
        champion.base_stats.add_stats(self.base_stats)
        champion


class ResistanceReduction(Buff):
    def ___init__(self, flat_reduction, percent_reduction, target_champion):
        super().__init__()
        self.flat_reduction = flat_reduction
        self.percent_reduction = percent_reduction
        self.base_stats.armor = - (target_champion.base_stats.armor * self.percent_reduction + self.flat_reduction * (1 - self.percent_reduction) * target_champion.base_stats.armor / target_champion.total_stats.armor)
        self.bonus_stats.armor = - (target_champion.bonus_stats.armor * self.percent_reduction + self.flat_reduction * (1 - self.percent_reduction) * target_champion.bonus_stats.armor / target_champion.total_stats.armor)

    def add_buff(self, buff):
        # needs to be overwritten
        a = 0
