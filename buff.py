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

    def __init__(self, transfer_type, duration_type, stack_number, compatible_damage_type, compatible_spell_type):
        self.transfer_type = transfer_type  # 'to spell' if it buffs/debuffs the spell,'to owner','to enemy'
        self.duration_type = duration_type  # 'indefinite', 'conditional', a number if it's temporary
        self.stack_number = stack_number  # how many times it can stack
        self.stack_count = 0  # how many times it has already stacked
        self.compatible_damage_type = compatible_damage_type  # 'physical','magical','true','all'
        self.compatible_spell_type = compatible_spell_type  # 'immobilize','slow','toggle','on-hit','shield,'heal','all'


class ArmorReduction(Buff):
    def __init__(self, flat_reduction, percent_reduction, duration_type, stack_number, compatible_damage_type,
                 compatible_spell_type):
        super(ArmorReduction, self).__init__('to enemy', duration_type, stack_number, compatible_damage_type,
                                                  compatible_spell_type)
        self.flat_reduction = flat_reduction
        self.percent_reduction = percent_reduction

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def add_buff_to(self, champion):
        if any(isinstance(x, type(self)) for x in champion.buff_list):
            # If there is another buff of the same class, adds itself to it
            buff = champion.buff_list[next(i for i, x in enumerate(champion.buff_list) if isinstance(x, type(self)))]
            if buff.stack_count < buff.stack_number:
                buff.stack_count += 1
        else:
            # If there isn't, simply add the buff
            champion.buff_list.append(self)
        champion.apply_buffs()  # Any time a buff is added to a champion, reapply every buff on that champion

    def apply_buff_to(self, champion):
        if self.duration_type == 'indefinite':
            champion.base_stats.armor = champion.orig_base_stats.armor
            champion.bonus_stats.armor = champion.orig_bonus_stats.armor
            for flat_reduction in self.flat_reduction[0:self.stack_count+1]:
                champion.base_stats.armor -= flat_reduction * champion.orig_base_stats.armor / champion.orig_total_stats.armor
                champion.bonus_stats.armor -= flat_reduction * champion.orig_bonus_stats.armor / champion.orig_total_stats.armor
            for percent_reduction in self.percent_reduction[0:self.stack_count+1]:
                champion.base_stats.armor = champion.base_stats.armor * (1 - percent_reduction)
                champion.bonus_stats.armor = champion.bonus_stats.armor * (1 - percent_reduction)
