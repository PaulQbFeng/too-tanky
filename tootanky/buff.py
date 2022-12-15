from abc import ABC, abstractmethod


class Buff(ABC):
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
        self.transfer_type = transfer_type  # 'to spell' if it buffs/debuffs the spell,'to owner','to enemy'
        self.duration_type = duration_type  # 'indefinite', 'conditional', a number if it's temporary
        self.compatible_damage_type = compatible_damage_type  # 'physical','magical','true','all'
        self.compatible_spell_type = compatible_spell_type  # 'immobilize','slow','toggle','on-hit','shield,'heal','all'

    def add_buff_to(self, champion):
        champion.buff_list.append(self)
        if self.transfer_type == 'to owner':
            # Any time a buff is added to a champion, apply it (only when it is directed to the owner)
            self.apply_buff_to(champion)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    @abstractmethod
    def apply_buff_to(self, champion):
        pass


class StackableBuff(Buff):
    """
    For buffs/debuffs that can stack with themselves (a limited number of times). Since they stack with themselves, they
    need a name.
    This class is also abstract. A subclass has to be created for every stackable buff/debuff.
    """

    def __init__(self, name, transfer_type, duration_type, stack_number, compatible_damage_type, compatible_spell_type):
        super().__init__(transfer_type, duration_type, compatible_damage_type, compatible_spell_type)
        self.name = name
        self.stack_number = stack_number  # how many times it can stack
        self.stack_count = 0  # how many times it has already stacked

    def add_buff_to(self, champion):
        if any(isinstance(x, type(self)) for x in champion.buff_list):
            # If there is already the same buff, just apply it
            buff = champion.buff_list[next(i for i, x in enumerate(champion.buff_list) if isinstance(x, type(self)))]
            if buff.name == self.name and buff.transfer_type == 'to owner':
                buff.apply_buff_to(champion)
        else:
            # If there isn't, add the buff
            champion.buff_list.append(self)
            if self.transfer_type == 'to owner':
                self.apply_buff_to(champion)


class ArmorReduction(Buff):
    def __init__(self, flat_reduction, percent_reduction, duration_type, compatible_damage_type, compatible_spell_type):
        super(ArmorReduction, self).__init__('to enemy', duration_type, compatible_damage_type, compatible_spell_type)
        self.flat_reduction = flat_reduction
        self.percent_reduction = percent_reduction

    def apply_buff_to(self, champion):
        champion.flat_armor_reduction += self.flat_reduction
        champion.percent_armor_reduction = 1 - (1 - champion.percent_armor_reduction) * (1 - self.percent_reduction)


class StackableArmorReduction(StackableBuff):
    def __init__(self, name, flat_reduction, percent_reduction, stack_number, duration_type,
                 compatible_damage_type, compatible_spell_type):
        super().__init__(name, 'to enemy', duration_type, stack_number, compatible_damage_type, compatible_spell_type)
        self.flat_reduction = flat_reduction
        self.percent_reduction = percent_reduction

    def apply_buff_to(self, champion):
        if self.stack_count < self.stack_number:
            champion.armor_reduction_flat += self.flat_reduction[self.stack_count]
            champion.armor_reduction_percent = 1 - (1 - champion.armor_reduction_percent) * (1 - self.percent_reduction[self.stack_count])
            self.stack_count += 1
