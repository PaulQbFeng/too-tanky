from typing import Optional


class Stats:
    """
    Champions, items, and rune shards can all be considered to have stats.
    Stats in league all have a fixed way of being stacked, hence why it makes sense to define a class.
    """

    def __init__(self, stat_dict: Optional[dict] = None):
        if stat_dict is None:
            stat_dict = {}

        self._dict = stat_dict

    def __getattr__(self, attribute):
        return self._dict.get(attribute)

    def __add__(self, stats):
        addition = dict()
        for name, value in stats._dict.items():
            if name not in self._dict:
                addition[name] = value
            elif name.endswith("_pen_percent"):
                addition[name] = 100 * (1 - (1 - self._dict.get(name) / 100) * (1 - value / 100))
            else:
                addition[name] = self._dict.get(name) + value

        return Stats(addition)

    def __sub__(self, stats):
        subtraction = dict()
        for name, value in stats._dict.items():
            if name not in self._dict:
                subtraction[name] = -value
            elif name.endswith("_pen_percent"):
                subtraction[name] = 100 * (1 - (1 - self._dict.get(name) / 100) * (1 + value / 100))
            else:
                subtraction[name] = self._dict.get(name) - value

        return Stats(subtraction)

    def print_stats(self):
        return print("\n".join([f"{k}: {v}" for k, v in self.__dict__.items()]))

    def get(self, attribute: str, default: float):
        """Similar to a dict get with default value"""
        return self._dict.get(attribute, default)
