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

    def __init__(self, transfer_type, duration_type, compatible_damage_type, compatible_spell_type):
        self.transfer_type = transfer_type  # 'to spell' if it buffs/debuffs the spell, 'to owner', 'to enemy'
        self.duration_type = duration_type  # 'indefinite', 'conditional', 'temporary'
        self.compatible_damage_type = compatible_damage_type  # 'physical', 'magical', 'true', 'all'
        self.compatible_spell_type = compatible_spell_type  # 'immobilize', 'slow', 'toggle', 'on-hit', 'shield, 'heal', 'all'


class ResistanceReduction(Buff):
    def __init__(self, flat_reduction, percent_reduction, duration_type, compatible_damage_type, compatible_spell_type):
        super(ResistanceReduction, self).__init__('to enemy', duration_type, compatible_damage_type, compatible_spell_type)
        self.flat_reduction = flat_reduction
        self.percent_reduction = percent_reduction

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def add_buff_to(self, champion):
        if any(isinstance(x, type(self)) for x in champion.buff_list):
            # If there is another buff of the same class, adds itself to it
            buff = champion.buff_list[next(i for i, x in enumerate(champion.buff_list) if isinstance(x, type(self)))]
            buff.flat_reduction += self.flat_reduction
            buff.percent_reduction = 1 - (1 - buff.percent_reduction) * (1 - self.percent_reduction)
        else:
            # If there isn't, simply add the buff
            champion.buff_list.append(self)
        champion.apply_buffs()  # Any time a buff is added to a champion, reapply every buff on that champion

    def apply_buff_to(self, champion):
        champion.base_stats.armor = (champion.orig_base_stats.armor - self.flat_reduction * champion.orig_base_stats.armor / champion.orig_total_stats.armor) * (1 - self.percent_reduction)
        champion.bonus_stats.armor = (champion.orig_bonus_stats.armor - self.flat_reduction * champion.orig_bonus_stats.armor / champion.orig_total_stats.armor) * (1 - self.percent_reduction)
