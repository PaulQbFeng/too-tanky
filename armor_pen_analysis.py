import matplotlib.pyplot as plt
import numpy as np

Armor = np.linspace(50,200,40)

normalized_damage = 1/(1+Armor/100)

damage_with_30percent_arpen = 1/(1+Armor*0.7/100)

damage_with_10flat_arpen = 1/(1+(Armor-10)/100)

damage_with_20flat_arpen = 1/(1+(Armor-20)/100)

damage_with_30flat_arpen = 1/(1+(Armor-30)/100)

damage_with_50flat_arpen = 1/(1+(Armor-50)/100)

plt.plot(Armor, normalized_damage, label = "0 arpen")
plt.plot(Armor, damage_with_30percent_arpen, label = "30% arpen")
plt.plot(Armor, damage_with_10flat_arpen, label = "10 flat arpen")
plt.plot(Armor, damage_with_20flat_arpen, label = "20 flat arpen")
plt.plot(Armor, damage_with_30flat_arpen, label = "30 flat arpen")
plt.plot(Armor, damage_with_50flat_arpen, label = "50 flat arpen")

plt.ylabel("normalized damage")
plt.xlabel("armor")
plt.legend(loc="upper right")

print("30% armor pen is better than 10 flat armor pen if the target has more than 34 armor")
print("30% armor pen is better than 20 flat armor pen if the target has more than 67 armor")
print("30% armor pen is better than 50 flat armor pen if the target has more than 167 armor")

plt.show()

