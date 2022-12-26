from tootanky.champion import BaseChampion


class Jax(BaseChampion):
    champion_name = "Jax"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
