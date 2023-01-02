import pytest
from tootanky.champion import Dummy


@pytest.fixture()
def dummy_100():
    return Dummy(health=1000, bonus_resistance=100)
