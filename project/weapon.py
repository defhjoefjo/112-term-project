from SETTINGS import *



class weapon(object):
    def __init__(self, damageMultiplier,bulSpedMulti):
        self.damageMultiplier = damageMultiplier
        self.bulSpedMulti = bulSpedMulti

class glock(weapon):
    def __init__(self,damageMultiplier,bulSpedMulti):
        super().__init__(damageMultiplier,bulSpedMulti)
        self.name = 'glock'
        self.id = 100

class awp(weapon):
    def __init__(self,damageMultiplier,bulSpedMulti):
        super().__init__(damageMultiplier,bulSpedMulti)
        self.name = 'awp'
        self.id = 101