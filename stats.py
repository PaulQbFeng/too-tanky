from typing import Optional, Dict, Union

StatsAnnot = Dict[str, Union[int, float]]

class Stats:
    """
    Champions, items, and rune shards can all be considered to have stats.
    Stats in league all have a fixed way of being stacked, hence why it makes sense to define a class.
    """

    def __init__(self, stat_dict: Optional[StatsAnnot] = None):
        if stat_dict is None:
            stat_dict = {}
            
        for name, value  in stat_dict.items():
            setattr(self, name, value)

    def print_stats(self):
        return print("\n".join([f"{k}: {v}" for k, v in self.__dict__.items()]))


    def __add__(self, stats: StatsAnnot):
        addition = dict()
        for name, value in stats.__dict__.items():
            if not hasattr(self, name):
                addition[name] = value
            else:
                addition[name] = getattr(self, name) + value

        return Stats(addition)

    def __sub__(self, stats: StatsAnnot):
        subtraction = dict()
        for name, value in stats.__dict__.items():
            if not hasattr(self, name):
                subtraction[name] = -value
            else:
                subtraction[name] = getattr(self, name) - value

        return Stats(subtraction)


    def get(self, attribute: str, default: float):
        """Similar to a dict get with default value"""
        return getattr(self, attribute, default)
