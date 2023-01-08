import pytest
from tootanky.champion import Dummy


@pytest.fixture
def dummy_100():
    return Dummy(health=1000, bonus_resistance=100)


@pytest.fixture
def dummy_110():
    return Dummy(health=1000, bonus_resistance=110)
