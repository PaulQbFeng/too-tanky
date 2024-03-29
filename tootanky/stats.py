import copy
from typing import Any, Optional


def add_stat(name, old_value, new_value):
    if name.endswith("_pen_percent"):
        return 1 - (1 - old_value) * (1 - new_value)
    else:
        return old_value + new_value


def sub_stat(name, old_value, new_value):
    if name.endswith("_pen_percent"):
        return 1 - (1 - old_value) / (1 - new_value)
    else:
        return old_value - new_value


class Stats:
    """
    Champions, items, and rune shards can all be considered to have stats.
    Stats in league all have a fixed way of being stacked, hence why it makes sense to define a class.
    """

    def __init__(self, stat_dict: Optional[dict] = None):
        if stat_dict is None:
            self._dict = {}
        else:
            self._dict = copy.deepcopy(stat_dict)

    def __getattr__(self, attribute):
        """Get attribute from underlying dict, default at 0"""
        return self._dict.get(attribute, 0)

    def __setattr__(self, __name: str, __value: Any) -> None:
        """Set attribute to the underlying dict"""
        if __name == "_dict":
            super().__setattr__("_dict", __value)
        else:
            self._dict[__name] = __value

    def __add__(self, stats: "Stats"):
        """
        Magic method to add to Stats object s1 + s2
        There are 3 cases to separate:
            - s2.attribute not in s1, set the value in s1
            - s2.attribute stacks multiplicatively (armor_pen_percent etc..), computes the result in percent
            - s2.attribute in s1, sum the 2 flat attributes
        """
        addition = self._dict.copy()
        for name, value in stats._dict.items():
            if name not in self._dict:
                addition[name] = value
            else:
                addition[name] = add_stat(name, self._dict.get(name), value)

        return Stats(addition)

    def __sub__(self, stats):
        """
        Magic method to add to Stats object s1 - s2
        There are 3 cases to separate:
            - s2.attribute not in s1, set -value in s1
            - s2.attribute stacks multiplicatively (armor_pen_percent etc..), computes the result in percent
            - s2.attribute in s1, subtract the 2 flat attributes
        """
        subtraction = self._dict.copy()
        for name, value in stats._dict.items():
            if name not in self._dict:
                subtraction[name] = -value
            else:
                subtraction[name] = sub_stat(name, self._dict.get(name), value)

        return Stats(subtraction)

    def get_stat_names(self) -> list:
        """
        Returns all stat names from the underlying dict.
        """
        return list(self._dict.keys())

    def print_stats(self):
        """pretty print the stats"""
        return print("\n".join([f"{k}: {v}" for k, v in self._dict.items()]))
