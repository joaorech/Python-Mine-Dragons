import math


#=------------- Monster -------------=#
class Monster:
    
    def __init__(self, level: int):
        self._level = level
        self._attack = math.ceil(level/2)
        self._hp = level + 1

    #---- Properties ----#
    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, value: int):
        self._level = value
        self._attack = math.ceil(value/2)
        self._hp = value + 1
    
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value: int):
        self._hp = value
    
    @property
    def attack(self):
        return self._attack
    @attack.setter
    def attack(self, value: int):
        self._attack = value
    #--------------------#

    #------ Methods -----#
    def Attack(self, damage: int) -> int:
        self.hp -= damage
        if self.hp > 0:
            return self.attack
        else:
            return 0
    #--------------------#
#=-----------------------------------=#