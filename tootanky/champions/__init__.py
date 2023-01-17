from .ahri import Ahri
from .akshan import Akshan
from .amumu import Amumu
from .annie import Annie
from .ashe import Ashe
from .brand import Brand
from .caitlyn import Caitlyn
from .darius import Darius
from .ezreal import Ezreal
from .irelia import Irelia
from .jarvan import JarvanIV
from .jax import Jax
from .malphite import Malphite
from .missfortune import MissFortune
from .yasuo import Yasuo
from .yone import Yone
from .xerath import Xerath
from .zed import Zed
from tootanky.champion import BaseChampion

ALL_CHAMPIONS = {cls.name: cls for cls in BaseChampion.__subclasses__() if cls.__name__ != "Dummy"}
