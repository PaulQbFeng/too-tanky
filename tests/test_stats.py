from stats import Stats


def test_stat_add():
    s1 = Stats({"armor": 30, "attack_damage": 15, "armor_pen_percent": 18})
    s2 = Stats({"armor": 10, "attack_damage": 7, "armor_pen_percent": 12})

    sum = s1 + s2
    assert sum.armor == 40
    assert sum.attack_damage == 22
    assert round(sum.armor_pen_percent, 2) == 27.84

    sub = s1 - s2
    assert sub.armor == 20
    assert sub.attack_damage == 8
    assert round(sub.armor_pen_percent, 2) == 8.16
