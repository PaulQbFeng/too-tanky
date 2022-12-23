from abc import ABC, abstractmethod
from dataclasses import dataclass

from tootanky.damage import damage_after_resistance, ratio_stat, pre_mitigation_spell_damage, get_resistance_type
from tootanky.data_parser import ALL_ITEM_STATS
from tootanky.stats import Stats


@dataclass
class ItemPassive:
    """Class to define item (or more?) passive"""

    name: str = ""
    unique: bool = False
    stats: Stats = None


class AbstractItem(ABC):
    """Abstract BaseItem class"""

    @abstractmethod
    def apply_passive(self):
        pass


class BaseItem:
    """
    Additional effects passive/active are handled in the children Item specific classes.
    """

    damage_type = None
    base_damage = 0

    def __init__(self):
        item_stats = ALL_ITEM_STATS[self.name].copy()
        self.gold = item_stats.pop("gold")
        self.stats = Stats(item_stats)
        self.limitations = None
        if self.damage_type is not None:
            self.target_res_type = get_resistance_type(self.damage_type)

    def init_champion_type(self):
        pass

    def apply_passive(self):
        pass

    def damage(self, target, damage_modifier_flat=0, damage_modifier_coeff=1) -> float:
        """Calculates the damage dealt to a champion with a spell"""

        ratio_dmg = ratio_stat(champion=self.champion, target=target, ratios=self.ratios)

        pre_mtg_dmg = pre_mitigation_spell_damage(
            self.base_damage,
            ratio_dmg,
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


# Starter items
# TODO: Cull, Dark Seal, Gustwalker Hatchling, Mosstomper Seedling, Relic Shield, Scorchclaw Pup, Spectral Sickle,
#  Spellthief's Edge, Steel Shoulderguards, Tear of the Goddess
class DoransBlade(BaseItem):
    name = "Doran's Blade"
    type = "Starter"


class DoransRing(BaseItem):  # missing passive (mana_regen)
    name = "Doran's Ring"
    type = "Starter"


class DoransShield(BaseItem):  # missing passive (health_regen after taking damage)
    name = "Doran's Shield"
    type = "Starter"


# Basic items
# TODO: Catalyst of Aeons, Faerie Charm, Rejuvenation Bead
class AmplifyingTome(BaseItem):
    name = "Amplifying Tome"
    type = "Basic"


class BamisCinder(BaseItem):  # missing passive
    name = "Bami's Cinder"
    type = "Basic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Immolate"]


class BFSword(BaseItem):
    name = "B. F. Sword"
    type = "Basic"


class BlastingWand(BaseItem):
    name = "Blasting Wand"
    type = "Basic"


class CloakofAgility(BaseItem):
    name = "Cloak of Agility"
    type = "Basic"


class ClothArmor(BaseItem):
    name = "Cloth Armor"
    type = "Basic"


class Dagger(BaseItem):
    name = "Dagger"
    type = "Basic"


class LongSword(BaseItem):
    name = "Long Sword"
    type = "Basic"


class NeedlesslyLargeRod(BaseItem):
    name = "Needlessly Large Rod"
    type = "Basic"


class NullMagicMantle(BaseItem):
    name = "Null-Magic Mantle"
    type = "Basic"


class PickAxe(BaseItem):
    name = "Pickaxe"
    type = "Basic"


class RubyCrystal(BaseItem):
    name = "Ruby Crystal"
    type = "Basic"


class SapphireCrystal(BaseItem):
    name = "Sapphire Crystal"
    type = "Basic"


class Sheen(BaseItem):
    name = "Sheen"
    type = "Basic"
    ratios = [("base_attack_damage", 1)]
    base_damage = 0
    damage_type = "physical"

    def __init__(self):
        super().__init__()
        self.activate = False

    def on_hit_effect(self, target):
        """Calculates the bonus damage dealt with an autoattack : 100% of base AD"""
        damage = 0
        if self.activate:
            damage = self.damage(target)
            self.activate = False
        return damage


# Epic items
# TODO: Executioner's Calling, Forbidden Idol, Hexdrinker, Hextech Alternator, Ironspike Whip, Kircheis Shard,
#  Leeching Leer, Oblivion Orb, Phage, Quicksilver Sash, Seeker's Armguard, Spectre's Cowl, Vampiric Scepter,
#  Verdant Barrier, Warden's Mail, Winged Moonplate, Zeal
class AegisoftheLegion(BaseItem):
    name = "Aegis of the Legion"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.stats.ability_haste = 10


class AetherWisp(BaseItem):  # missing unique passive (bonus_move_speed)
    name = "Aether Wisp"
    type = "Epic"


class BandleglassMirror(BaseItem):  # missing base_mana_regen
    name = "Bandleglass Mirror"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.stats.ability_haste = 10


class BlightingJewel(BaseItem):
    name = "Blighting Jewel"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Void Pen"]
        self.stats.magic_resist_pen_percent = 0.13


class BrambleVest(BaseItem):  # missing passive
    name = "Bramble Vest"
    type = "Epic"


class CaulfieldsWarhammer(BaseItem):
    name = "Caulfield's Warhammer"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.stats.ability_haste = 10


class ChainVest(BaseItem):
    name = "Chain Vest"
    type = "Epic"


class CrystallineBracer(BaseItem):  # missing base_health_regen
    name = "Crystalline Bracer"
    type = "Epic"


class FiendishCodex(BaseItem):
    name = "Fiendish Codex"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.stats.ability_haste = 10


class Frostfang(BaseItem):  # missing base_mana_regen
    name = "Frostfang"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Support"]


class GiantsBelt(BaseItem):
    name = "Giant's Belt"
    type = "Epic"


class GlacialBuckler(BaseItem):  # missing ability haste
    name = "Glacial Buckler"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.stats.ability_haste = 10


class HarrowingCrescent(BaseItem):  # missing base_mana_regen
    name = "Harrowing Crescent"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Support"]


class HearthboundAxe(BaseItem):  # missing passive (bonus_move_speed when basic attacks)
    name = "Hearthbound Axe"
    type = "Epic"


class Kindlegem(BaseItem):
    name = "Kindlegem"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.stats.ability_haste = 10


class LastWhisper(BaseItem):
    name = "Last Whisper"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Last Whisper"]
        self.stats.armor_pen_percent = 0.18


class LostChapter(BaseItem):
    name = "Lost Chapter"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Mythic Component"]
        self.stats.ability_haste = 10


class NegatronCloak(BaseItem):
    name = "Negatron Cloak"
    type = "Epic"


class Noonquiver(BaseItem):
    name = "Noonquiver"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Mythic Component"]


class Rageknife(BaseItem):
    name = "Rageknife"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Crit Modifier"]
        self.ratios = [("crit_chance", 1.75 * 100)]


class RecurveBow(BaseItem):
    name = "Recurve Bow"
    type = "Epic"
    damage_type = "physical"

    def __init__(self):
        super().__init__()
        self.ratios = None

    def on_hit_effect(self, target):
        return self.damage(target, damage_modifier_flat=15)


class RunesteelSpaulders(BaseItem):  # missing base_health_regen
    name = "Runesteel Spaulders"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Support"]


class SerratedDirk(BaseItem):
    name = "Serrated Dirk"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.passive = ItemPassive(name="Gouge", unique=True, stats=Stats({"lethality": 10}))

    def apply_passive(self):
        self.stats = self.stats + self.passive.stats


class TargonsBuckler(BaseItem):  # missing base_health_regen
    name = "Targon's Buckler"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Support"]


class Tiamat(BaseItem):
    name = "Tiamat"
    type = "Epic"
    damage_type = "physical"

    def __init__(self):
        super().__init__()
        self.limitations = ["Hydra"]
        self.activate = False

    def init_champion_type(self):
        if self.champion.champion_type == "Melee":
            self.ratios = [("attack_damage", 0.4)]
        if self.champion.champion_type == "Ranged":
            self.ratios = [("attack_damage", 0.2)]

    def on_hit_effect(self, target):
        """
        Basic attacks on-hit deal (mel.40% AD/rang.20% AD) physical dmg to other enemies within 350 units of the target.
        """
        # TODO: This must depend on other targets' resistances
        damage = 0
        if self.activate:
            damage = self.damage(target)
        return damage


class WatchfulWardstone(BaseItem):
    name = "Watchful Wardstone"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.limitations = ["Sightstone"]
        self.stats.ability_haste = 10


# Legendary items
# TODO: Abyssal Mask, Anathema's Chains, Archangel's Staff, Ardent Censer, Axiom Arc, Banshee's Veil, Black Cleaver,
#  Black Mist Scythe, Blade of the Ruined King, Bloodthirster, Bulwark of the Mountain, Chempunk Chainsword,
#  Chemtech Putrifier, Dead Man's Plate, Death's Dance, Demonic Embrace, Essence Reaver, Fimbulwinter, Force of Nature,
#  Frozen Heart, Gargoyle Stoneplate, Guardian Angel, Guinsoo's Rageblade, Horizon Focus, Hullbreaker, Infinity Edge,
#  Knight's Vow, Lich Bane, Lord Dominik's Regards, Manamune, Maw of Malmortius, Mejai's Soulstealer,
#  Mercurial Scimitar, Mikael's Blessing, Morellonomicon, Mortal Reminder, Muramana, Pauldrons of Whiterock,
#  Phantom Dancer, Rabadon's Deathcap, Randuin's Omen, Rapid Firecannon, Ravenous Hydra, Redemption, Runaan's Hurricane,
#  Rylai's Crystal Scepter, Seraph's Embrace, Serpent's Fang, Shadowflame, Shard of True Ice, Silvermere Dawn,
#  Spear of Shojin, Spirit Visage, Staff of Flowing Water, Sterak's Gage, Stormrazor, Sunfire Aegis, The Collector,
#  Thornmail, Titanic Hydra, Turbo Chemtank, Umbral Glaive, Void Staff, Warmog's Armor, Winter's Approach, Wit's End,
#  Zeke's Convergence, Zhonya's Hourglass
class BlackCleaver(BaseItem):
    name = "Black Cleaver"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.stats.ability_haste = 30
        self.carve_stack_count = 0

    def get_carve_stack_stats(self, target, **kwargs):
        if self.carve_stack_count < 6:
            armor_reduction_percent = target.armor_reduction_percent
            self.carve_stack_count += 1
            return 1 - (1 - armor_reduction_percent - 0.05)/(1 - armor_reduction_percent)
        else:
            return 0

    def deapply_buffs(self, target, **kwargs):
        if self.carve_stack_count > 0:
            percent_debuff = 1 - (
                    1 - target.armor_reduction_percent + self.carve_stack_count * 0.05
            ) / (1 - target.armor_reduction_percent)
            target.update_armor_stats(percent_debuff=percent_debuff)
            self.carve_stack_count = 0


class CosmicDrive(BaseItem):  # missing passive
    name = "Cosmic Drive"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.stats.ability_haste = 30


class EdgeofNight(BaseItem):  # missing passive
    name = "Edge of Night"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.stats.lethality = 10


class GuardianAngel(BaseItem):  # missing passive
    name = "Guardian Angel"
    type = "Legendary"


class InfinityEdge(BaseItem):  # missing passive
    name = "Infinity Edge"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.limitations = ["Crit Modifier"]


class NashorsTooth(BaseItem):  # missing passive
    name = "Nashor's Tooth"
    type = "Legendary"


class NavoriQuickblades(BaseItem):  # missing passive
    name = "Navori Quickblades"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.limitations = ["Marksman Capstone", "Ability Haste Capstone"]
        self.stats.ability_haste = 20


class RabadonsDeathcap(BaseItem):
    name = "Rabadon's Deathcap"
    type = "Legendary"


class SeryldasGrudge(BaseItem):  # missing passive, ability haste
    name = "Serylda's Grudge"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.limitations = ["Last Whisper"]
        self.stats.armor_pen_percent = 0.3
        self.stats.ability_haste = 20


class VigilantWardstone(BaseItem):
    name = "Vigilant Wardstone"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.stats.ability_haste = 15


class YoumuusGhostblade(BaseItem):  # missing passive, active
    name = "Youmuu's Ghostblade"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.stats.lethality = 18
        self.stats.ability_haste = 15


# Mythic items
# TODO: Crown of the Shattered Queen, Divine Sunderer, Duskblade of Draktharr, Eclipse, Evenshroud,
#  Goredrinker, Heartsteel, Hextech Rocketbelt, Iceborn Gauntlet, Immortal Shieldbow, Imperial Mandate,
#  Jak'Sho, The Protean, Kraken Slayer, Liandry's Anguish, Locket of the Iron Solari, Luden's Tempest,
#  Moonstone Renewer, Night Harvester, Prowler's Claw, Radiant Virtue, Riftmaker, Rod of Ages, Shurelya's Battlesong,
#  Stridebreaker, Trinity Force
class Everfrost(BaseItem):  # missing active
    name = "Everfrost"
    type = "Mythic"

    def __init__(self):
        super().__init__()
        self.mythic_passive_stats = [("ability_power", 10, "flat")]
        self.stats.ability_haste = 20


class Galeforce(BaseItem):
    name = "Galeforce"
    type = "Mythic"

    def __init__(self):
        super().__init__()
        self.mythic_passive_stats = [("bonus_move_speed", 0.02, "percent")]

    def apply_active(self, target):
        max_health = target.orig_base_stats.health + target.orig_bonus_stats.health
        base_mr = target.base_magic_resist
        bonus_mr = target.bonus_magic_resist
        bonus_ad = self.champion.bonus_attack_damage
        magic_resist_pen_flat = self.champion.magic_resist_pen_flat
        magic_resist_pen_percent = self.champion.magic_resist_pen_percent
        if self.champion.level < 10:
            base_active_damage = 60
        elif self.champion.level >= 10:
            base_active_damage = 65 + (self.champion.level - 10) * 5
        total_damage = 0

        for _ in range(3):
            percent_missing_health = 1 - target.health / max_health
            if percent_missing_health <= 0.7:
                pre_mtg_dmg = (base_active_damage + 0.15 * bonus_ad) * (1 + percent_missing_health * 5 / 7)
            else:
                pre_mtg_dmg = (base_active_damage + 0.15 * bonus_ad) * 1.5
            damage = damage_after_resistance(
                pre_mitigation_damage=pre_mtg_dmg,
                base_resistance=base_mr,
                bonus_resistance=bonus_mr,
                flat_resistance_pen=magic_resist_pen_flat,
                resistance_pen=magic_resist_pen_percent,
                bonus_resistance_pen=0,
            )
            target.take_damage(damage)
            total_damage += damage

        return total_damage


ALL_ITEM_CLASSES = {cls.name: cls for cls in BaseItem.__subclasses__()}
SPELL_BLADE_ITEMS = ["Divine Sunderer", "Trinity Force", "Lich Bane", "Essence Reaver", "Sheen"]
CLASSIC_ON_HIT_ITEMS = ["Recurve Bow"]
WRATH_ITEMS = ["Rageknife", "Guinsoo's Rageblade"]
