import pytest
from tootanky.dummy import Dummy


@pytest.fixture
def dummy_0():
    return Dummy(health=1000, bonus_resistance=0)


@pytest.fixture
def dummy_100():
    return Dummy(health=1000, bonus_resistance=100)


@pytest.fixture
def dummy_110():
    return Dummy(health=1000, bonus_resistance=110)
