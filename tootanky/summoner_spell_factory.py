from tootanky.summoner_spell import BaseSummonerSpell


class Ignite(BaseSummonerSpell):
    """
    Ignite Summoner spell. Total damage is the n * tick damage.
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
