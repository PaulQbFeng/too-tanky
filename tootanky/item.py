from abc import ABC, abstractmethod
from dataclasses import dataclass

from tootanky.damage import damage_after_resistance, damage_after_positive_resistance
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

    item_name = None

    def __init__(self):
        item_stats = ALL_ITEM_STATS[self.item_name].copy()
        self.gold = item_stats.pop("gold")
        self.stats = Stats(item_stats)
        self.passive = ItemPassive()
        self.champion = None

    def apply_passive(self):
        pass


# Starter items
# TODO: Cull, Dark Seal, Gustwalker Hatchling, Mosstomper Seedling, Relic Shield,
#  Scorchclaw Pup, Spectral Sickle, Spellthief's Edge, Steel Shoulderguards, Tear of the Goddess
class DoranBlade(BaseItem):
    item_name = "Doran's Blade"
    type = "Starter"


class DoranRing(BaseItem):  # missing passive (mana_regen)
    item_name = "Doran's Ring"
    type = "Starter"


class DoranShield(BaseItem):  # missing passive (health_regen after taking damage)
    item_name = "Doran's Shield"
    type = "Starter"


# Basic items
# TODO: Catalyst of Aeons, Faerie Charm, Rejuvenation Bead
class AmplifyingTome(BaseItem):
    item_name = "Amplifying Tome"
    type = "Basic"


class BamiCinder(BaseItem):  # missing passive
    item_name = "Bami's Cinder"
    type = "Basic"


class BFSword(BaseItem):
    item_name = "B. F. Sword"
    type = "Basic"


class BlastingWand(BaseItem):
    item_name = "Blasting Wand"
    type = "Basic"


class CloakofAgility(BaseItem):
    item_name = "Cloak of Agility"
    type = "Basic"


class ClothArmor(BaseItem):
    item_name = "Cloth Armor"
    type = "Basic"


class Dagger(BaseItem):
    item_name = "Dagger"
    type = "Basic"


class LongSword(BaseItem):
    item_name = "Long Sword"
    type = "Basic"


class NeedlesslyLargeRod(BaseItem):
    item_name = "Needlessly Large Rod"
    type = "Basic"


class NullMagicMantle(BaseItem):
    item_name = "Null-Magic Mantle"
    type = "Basic"


class PickAxe(BaseItem):
    item_name = "Pickaxe"
    type = "Basic"


class RubyCrystal(BaseItem):
    item_name = "Ruby Crystal"
    type = "Basic"


class SapphireCrystal(BaseItem):
    item_name = "Sapphire Crystal"
    type = "Basic"


class Sheen(BaseItem):
    item_name = "Sheen"
    type = "Basic"

    def spellblade(self, owner_champion, enemy_champion):
        """Calculates the bonus damage dealt with an autoattack : 100% of base AD"""
        return damage_after_positive_resistance(owner_champion.base_attack_damage, enemy_champion.bonus_armor)


# Epic items
# TODO: Executioner's Calling, Forbidden Idol, Hexdrinker, Hextech Alternator, Ironspike Whip, Kircheis Shard,
#  Leeching Leer, Oblivion Orb, Phage, Quicksilver Sash, Rageknife, Recurve Bow, Seeker's Armguard, Spectre's Cowl,
#  Tiamat, Vampiric Scepter, Verdant Barrier, Warden's Mail, Winged Moonplate, Zeal
class AegisLegion(BaseItem):  # missing ability haste
    item_name = "Aegis of the Legion"
    type = "Epic"


class AetherWisp(BaseItem):  # missing unique passive (bonus_move_speed)
    item_name = "Aether Wisp"
    type = "Epic"


class BandleglassMirror(BaseItem):  # missing ability haste and base_mana_regen
    item_name = "Bandleglass Mirror"
    type = "Epic"


class BlightingJewel(BaseItem):
    item_name = "Blighting Jewel"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.stats.add("magic_resist_pen_percent", 13)


class BrambleVest(BaseItem):  # missing passive
    item_name = "Bramble Vest"
    type = "Epic"


class CaulfieldWarhammer(BaseItem):  # missing ability haste
    item_name = "Caulfield's Warhammer"
    type = "Epic"


class ChainVest(BaseItem):
    item_name = "Chain Vest"
    type = "Epic"


class CrystallineBracer(BaseItem):  # missing base_health_regen
    item_name = "Crystalline Bracer"
    type = "Epic"


class FiendishCodex(BaseItem):  # missing ability haste
    item_name = "Fiendish Codex"
    type = "Epic"


class Frostfang(BaseItem):  # missing base_mana_regen
    item_name = "Frostfang"
    type = "Epic"


class GiantBelt(BaseItem):
    item_name = "Giant's Belt"
    type = "Epic"


class GlacialBuckler(BaseItem):  # missing ability haste
    item_name = "Glacial Buckler"
    type = "Epic"


class HarrowingCrescent(BaseItem):  # missing base_mana_regen
    item_name = "Harrowing Crescent"
    type = "Epic"


class HearthboundAxe(BaseItem):  # missing passive (bonus_move_speed when basic attacks)
    item_name = "Hearthbound Axe"
    type = "Epic"


class Kindlegem(BaseItem):  # missing ability haste
    item_name = "Kindlegem"
    type = "Epic"


class LastWhisper(BaseItem):
    item_name = "Last Whisper"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.stats.armor_pen_percent = 18


class LostChapter(BaseItem):  # missing ability haste
    item_name = "Lost Chapter"
    type = "Epic"


class NegatronCloak(BaseItem):
    item_name = "Negatron Cloak"
    type = "Epic"


class Noonquiver(BaseItem):
    item_name = "Noonquiver"
    type = "Epic"


class RunesteelSpaulders(BaseItem):  # missing base_health_regen
    item_name = "Runesteel Spaulders"
    type = "Epic"


class SerratedDirk(BaseItem):
    item_name = "Serrated Dirk"
    type = "Epic"

    def __init__(self):
        super().__init__()
        self.passive = ItemPassive(name="Gouge", unique=True, stats=Stats({"lethality": 10}))

    def apply_passive(self):
        self.stats = self.stats + self.passive.stats


class TargonBuckler(BaseItem):  # missing base_health_regen
    item_name = "Targon's Buckler"
    type = "Epic"


class WatchfulWardstone(BaseItem):  # missing ability haste
    item_name = "Watchful Wardstone"
    type = "Epic"


# Legendary items
# TODO: Abyssal Mask, Anathema's Chains, Archangel's Staff, Ardent Censer, Axiom Arc, Banshee's Veil, Black Cleaver,
#  Black Mist Scythe, Blade of the Ruined King, Bloodthirster, Bulwark of the Mountain, Chempunk Chainsword,
#  Chemtech Putrifier, Cosmic Drive, Dead Man's Plate, Death's Dance, Demonic Embrace, Edge of Night, Essence Reaver,
#  Fimbulwinter, Force of Nature, Frozen Heart, Gargoyle Stoneplate, Guardian Angel, Guinsoo's Rageblade, Horizon Focus,
#  Hullbreaker, Infinity Edge, Knight's Vow, Lich Bane, Lord Dominik's Regards, Manamune, Maw of Malmortius,
#  Mejai's Soulstealer, Mercurial Scimitar, Mikael's Blessing, Morellonomicon, Mortal Reminder, Muramana,
#  Nashor's Tooth, Navori Quickblades, Pauldrons of Whiterock, Phantom Dancer, Rabadon's Deathcap, Randuin's Omen,
#  Rapid Firecannon, Ravenous Hydra, Redemption, Runaan's Hurricane, Rylai's Crystal Scepter, Seraph's Embrace,
#  Serpent's Fang, Shadowflame, Shard of True Ice, Silvermere Dawn, Spear of Shojin, Spirit Visage,
#  Staff of Flowing Water, Sterak's Gage, Stormrazor, Sunfire Aegis, The Collector, Thornmail, Titanic Hydra,
#  Turbo Chemtank, Umbral Glaive, Vigilant Wardstone, Void Staff, Warmog's Armor, Winter's Approach, Wit's End,
#  Zeke's Convergence, Zhonya's Hourglass
class SeryldaGrudge(BaseItem):  # missing passive, ability haste
    item_name = "Serylda's Grudge"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.stats.armor_pen_percent = 30


class YoumuuGhostblade(BaseItem):  # missing passive, active, ability haste
    item_name = "Youmuu's Ghostblade"
    type = "Legendary"

    def __init__(self):
        super().__init__()
        self.stats.lethality = 18


# Mythic items
# TODO: Crown of the Shattered Queen, Divine Sunderer, Duskblade of Draktharr, Eclipse, Evenshroud, Everfrost,
#  Goredrinker, Heartsteel, Hextech Rocketbelt, Iceborn Gauntlet, Immortal Shieldbow, Imperial Mandate,
#  Jak'Sho, The Protean, Kraken Slayer, Liandry's Anguish, Locket of the Iron Solari, Luden's Tempest,
#  Moonstone Renewer, Night Harvester, Prowler's Claw, Radiant Virtue, Riftmaker, Rod of Ages, Shurelya's Battlesong,
#  Stridebreaker, Trinity Force
class Galeforce(BaseItem):
    item_name = "Galeforce"
    type = "Mythic"

    def __init__(self):
        super().__init__()
        self.mythic_passive_ratio = [0.2]
        self.mythic_passive_type = ["bonus_move_speed"]

    def apply_active(self, enemy_champion):
        max_health = enemy_champion.orig_base_stats.health + enemy_champion.orig_bonus_stats.health
        base_mr = enemy_champion.base_magic_resist
        bonus_mr = enemy_champion.bonus_magic_resist
        bonus_ad = self.champion.bonus_attack_damage
        magic_resist_pen_flat = self.champion.magic_resist_pen_flat
        magic_resist_pen_percent = self.champion.magic_resist_pen_percent
        if self.champion.level < 10:
            base_active_damage = 60
        elif self.champion.level >= 10:
            base_active_damage = 65 + (self.champion.level - 10) * 5
        total_damage = 0

        for _ in range(3):
            percent_missing_health = 1 - enemy_champion.health / max_health
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
            enemy_champion.take_damage(damage)
            total_damage += damage

        return total_damage


ALL_ITEM_CLASSES = {cls.item_name: cls for cls in BaseItem.__subclasses__()}
