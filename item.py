from abc import ABC, abstractmethod
from dataclasses import dataclass

from damage import damage_after_resistance, damage_after_positive_resistance
from data_parser import ALL_ITEM_STATS
from stats import Stats


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
    Base class to represent an item. It is initialized with the base stats of the item.
    Additional effects passive/active are handled in the children Champion specific classes.
    """

    def __init__(self, item_name: str, item_type: str):
        item_stats = ALL_ITEM_STATS[item_name].copy()
        self.gold = item_stats.pop("gold")
        self.stats = Stats(item_stats)
        self.type = item_type
        self.passive = ItemPassive()

    def apply_passive(self):
        pass


# Starter items
# TODO: Cull, Dark Seal, Doran's Ring, Doran's Shield, Gustwalker Hatchling, Mosstomper Seedling, Relic Shield,
#  Scorchclaw Pup, Spectral Sickle, Spellthief's Edge, Steel Shoulderguards, Tear of the Goddess
class DoranBlade(BaseItem):
    item_name = "Doran's Blade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Starter", **kwargs)


# Basic items
# TODO: Bami's Cinder, Catalyst of Aeons, Dagger, Faerie Charm, Null-Magic Mantle, Rejuvenation Bead, Sapphire Crystal
class AmplifyingTome(BaseItem):
    item_name = "Amplifying Tome"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class BFSword(BaseItem):
    item_name = "B. F. Sword"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class BlastingWand(BaseItem):
    item_name = "Blasting Wand"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class CloakofAgility(BaseItem):
    item_name = "Cloak of Agility"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class ClothArmor(BaseItem):
    item_name = "Cloth Armor"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class LongSword(BaseItem):
    item_name = "Long Sword"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class NeedlesslyLargeRod(BaseItem):
    item_name = "Needlessly Large Rod"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class PickAxe(BaseItem):
    item_name = "Pickaxe"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class RubyCrystal(BaseItem):
    item_name = "Ruby Crystal"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)


class Sheen(BaseItem):
    item_name = "Sheen"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Basic", **kwargs)

    def spellblade(self, owner_champion, enemy_champion):
        """Calculates the bonus damage dealt with an autoattack : 100% of base AD"""
        return damage_after_positive_resistance(
            owner_champion.base_attack_damage, enemy_champion.bonus_armor
        )


# Epic items
# TODO: Aegis of the Legion, Aether Wisp, Bandleglass Mirror, Blighting Jewel, Bramble Vest, Caulfield's Warhammer,
#  Chain Vest, Crystalline Bracer, Executioner's Calling, Fiendish Codex, Forbidden Idol, Frostfang, Giant's Belt,
#  Glacial Buckler, Harrowing Crescent, Hearthbound Axe, Hexdrinker, Hextech Alternator, Ironspike Whip, Kindlegem,
#  Kircheis Shard, Leeching Leer, Lost Chapter, Negatron Cloak, Noonquiver, Oblivion Orb, Phage, Quicksilver Sash,
#  Rageknife, Recurve Bow, Runesteel Spaulders, Seeker's Armguard, Spectre's Cowl, Targon's Buckler, Tiamat,
#  Vampiric Scepter, Verdant Barrier, Warden's Mail, Watchful Wardstone, Winged Moonplate, Zeal
class LastWhisper(BaseItem):
    item_name = "Last Whisper"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Epic", **kwargs)
        self.stats.add("armor_pen_percent", 18)


class SerratedDirk(BaseItem):
    item_name = "Serrated Dirk"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Epic", **kwargs)
        self.passive = ItemPassive(name="Gouge", unique=True, stats=Stats({"lethality": 10}))

    def apply_passive(self):
        self.stats = self.stats + self.passive.stats


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

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Legendary", **kwargs)
        self.stats.add("armor_pen_percent", 30)


class YoumuuGhostblade(BaseItem):  # missing passive, active, ability haste
    item_name = "Youmuu's Ghostblade"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Legendary", **kwargs)
        self.stats.add("lethality", 18)


# Mythic items
# TODO: Crown of the Shattered Queen, Divine Sunderer, Duskblade of Draktharr, Eclipse, Evenshroud, Everfrost,
#  Goredrinker, Heartsteel, Hextech Rocketbelt, Iceborn Gauntlet, Immortal Shieldbow, Imperial Mandate,
#  Jak'Sho, The Protean, Kraken Slayer, Liandry's Anguish, Locket of the Iron Solari, Luden's Tempest,
#  Moonstone Renewer, Night Harvester, Prowler's Claw, Radiant Virtue, Riftmaker, Rod of Ages, Shurelya's Battlesong,
#  Stridebreaker, Trinity Force
class Galeforce(BaseItem):
    item_name = "Galeforce"

    def __init__(self, **kwargs):
        super().__init__(item_name=__class__.item_name, item_type="Mythic", **kwargs)

    def apply_active(self, holder, enemy_champion):
        max_health = enemy_champion.orig_base_stats.health + enemy_champion.orig_bonus_stats.health
        base_mr = enemy_champion.base_magic_resist
        bonus_mr = enemy_champion.bonus_magic_resist
        bonus_ad = holder.bonus_attack_damage
        magic_resist_pen_flat = holder.magic_resist_pen_flat
        magic_resist_pen_percent = holder.magic_resist_pen_percent
        if holder.level < 10:
            base_active_damage = 60
        elif holder.level >= 10:
            base_active_damage = 65 + (holder.level - 10) * 5
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
                bonus_resistance_pen=0
            )
            enemy_champion.take_damage(damage)
            total_damage += damage

        return total_damage


ALL_ITEM_CLASSES = {cls.item_name: cls for cls in BaseItem.__subclasses__()}
