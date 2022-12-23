from tootanky.damage import damage_after_resistance, pre_mitigation_damage, ratio_damage, get_resistance_type


class BaseDamageMixin:
    """
    Base damage class that represents the basic mechanisms during a damage instance:
         - attacks's base damage(s)
         - damage_type
         - damage_modifier_flat
         - damage_modifier_coeff
         - damage method
         - do_damage method
         - etc...

    Several league objects need this attack system:
        - Champion spells ---> BaseSpell(BaseDamageMixin)
        - Item actives / on-hits ---> ActiveItem(BaseDamageMixin, BaseItem)
        - Runes ---> TODO
        - Champion auto-attack ---> TODO

    BaseDamageMixin does not have a __init__ method, always put it as the left argument when creating
    a class with multiple inheritance. Eg. class ActiveItem(BaseDamageMixin, BaseItem).
    """

    def get_base_damage(self):
        """Gets the base damage of the damage instance"""
        return 0

    def _compute_damage(self, target, damage_modifier_flat=0, damage_modifier_coeff=1) -> float:
        """Calculates the damage dealt to the target. (private)"""

        ratio_dmg = ratio_damage(champion=self.champion, target=target, ratios=self.ratios, spell_leve1=self.level)

        pre_mtg_dmg = pre_mitigation_damage(
            base_damage=self.get_base_damage(),
            ratio_damage=ratio_dmg,
            damage_modifier_flat=damage_modifier_flat,
            damage_modifier_coeff=damage_modifier_coeff,
        )

        res_type = self.target_res_type
        if res_type == "armor":
            bonus_resistance_pen = self.champion.bonus_armor_pen_percent
        else:
            bonus_resistance_pen = 0
        # TODO: Can be refactored once we know more about bonus res pen
        post_mtg_dmg = damage_after_resistance(
            pre_mitigation_damage=pre_mtg_dmg,
            base_resistance=getattr(target, f"base_{res_type}"),
            bonus_resistance=getattr(target, f"bonus_{res_type}"),
            flat_resistance_pen=getattr(self.champion, f"{res_type}_pen_flat"),
            resistance_pen=getattr(self.champion, f"{res_type}_pen_percent"),
            bonus_resistance_pen=bonus_resistance_pen,
        )

        return post_mtg_dmg

    def get_damage_modifier_flat(self, **kwargs):
        """Get damage modifier flat from different sources."""
        return 0

    def get_damage_modifier_coeff(self, **kwargs):
        """Get damage modifier coefficients from different sources."""
        return 1

    def on_attack_state_change(self):
        """Change internal attribute e.g cait w and e"""
        pass

    def damage(self, target, **kwargs):
        """Computes the damage dealt to the target."""
        damage_modifier_flat = self.get_damage_modifier_flat(**kwargs)
        damage_modifier_coeff = self.get_damage_modifier_coeff(**kwargs)
        damage = self._compute_damage(target, damage_modifier_flat, damage_modifier_coeff)

        return damage

    def do_damage(self, target, **kwargs):
        """Computes the damage dealt and inflict the damage to the target."""

        damage = self.damage(target, **kwargs)
        target.take_damage(damage)
        return damage
