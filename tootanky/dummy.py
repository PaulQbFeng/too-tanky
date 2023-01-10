from tootanky.champion import BaseChampion

# Dummy class for tests in practice tool.
class Dummy(BaseChampion):
    name = "Dummy"

    def __init__(self, health: float = 1000, bonus_resistance: int = 0):
        super().__init__(level=1)
        """Dummy (here defined as a champion) has the same armor and magic resist. His health is capped at 10 000"""
        assert bonus_resistance % 10 == 0
        assert health % 100 == 0
        assert health <= 10000
        self.orig_bonus_stats.armor = bonus_resistance
        self.orig_bonus_stats.magic_resist = bonus_resistance
        self.orig_bonus_stats.health = health - 1000
        self.restore_champion_stats()
