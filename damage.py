# TODO: it seems that hp are ceiled while damage floored. (however it seems that the ad is rounded in the stat section ingame)

def damage_ad_armor(attack_ad: float, defense_armor: float):
    """
    Calculates the output damage of an auto attack from a champion with X amount of 
    attack damage on a champion with Y amount of armor.
    """
    return attack_ad * 100 / (100 + defense_armor)

