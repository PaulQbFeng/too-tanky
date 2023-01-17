from tootanky.glossary import convert_to_snake_case


def test_snake_case():
    assert convert_to_snake_case("Miss Fortune") == "miss_fortune"
    assert convert_to_snake_case("K'Sante") == "ksante"
    assert convert_to_snake_case("Future's Market") == "futures_market"
    assert convert_to_snake_case("Legende: Tenacity") == "legende_tenacity"
