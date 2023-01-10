def test_dummy_res(dummy_0, dummy_100, dummy_110):
    assert dummy_0.armor == 0
    assert dummy_0.magic_resist == 0
    assert dummy_0.health == 1000

    assert dummy_100.armor == 100
    assert dummy_100.magic_resist == 100
    assert dummy_100.health == 1000

    assert dummy_110.armor == 110
    assert dummy_110.magic_resist == 110
    assert dummy_110.health == 1000
