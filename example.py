from champion import Annie, Ahri, Jax, Irelia
from data_parser import SCALING_STAT_NAMES

annie = Annie()
ahri = Ahri()
jax = Jax()
irelia = Irelia()

damage1 = ahri.auto_attack(annie)
damage2 = annie.auto_attack(ahri)
damage3 = jax.auto_attack(irelia)
damage4 = irelia.auto_attack(jax)

print(f"Ahri lvl 1 auto Annie level 1, damage dealt: {round(damage1, 2)}")
print(f"Annie lvl 1 auto Ahri level 1, damage dealt: {round(damage2, 2)}")
print(f"Jax lvl 1 auto Irelia level 1, damage dealt: {round(damage3, 2)}")
print(f"Irelia lvl 1 auto Jax level 1, damage dealt: {round(damage4, 2)}")

annie=Annie(level = 18)
print(annie.get_stats())
