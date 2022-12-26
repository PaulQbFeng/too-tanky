class SpellFactory:
    _SPELLS = {}

    @classmethod
    def register_spell(cls, spell_cls):
        champion_name = spell_cls.champion_name
        spell_key = spell_cls.__name__[0].lower()
        if champion_name not in cls._SPELLS:
            cls._SPELLS[champion_name] = dict()
        cls._SPELLS[champion_name][spell_key] = spell_cls
        return spell_cls

    @classmethod
    def get_spells_for_champion(cls, champion_name):
        if champion_name in cls._SPELLS:
            return cls._SPELLS[champion_name]
        raise KeyError(f"Could not find spells for champion {champion_name}")
