from tootanky.champion import BaseChampion


class Jax(BaseChampion):
    name = "Jax"
    range_type = "Melee"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
