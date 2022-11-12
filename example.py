from champion import Annie, Ahri
annie = Annie()
ahri = Ahri()

damage1 = ahri.auto_attack(annie)
damage2 = annie.auto_attack(ahri)

print(f"Ahri lvl 1 auto Annie level 1, damage dealt: {round(damage1, 2)}")
print(f"Annie lvl 1 auto Ahri level 1, damage dealt: {round(damage2, 2)}")