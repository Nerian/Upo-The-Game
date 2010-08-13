
import Ship
import random
from gameobjects import vector2


class Factoria():
        
    def build_player(self):
        return Ship.Wing()
    def build_clone(self, pos):

        return Ship.Clone(pos)

    def build_clone(self):
        return Ship.Clone(vector2.Vector2(random.randint(20,780),-50))

    def build_hunter(self):
        return Ship.Hunter(vector2.Vector2(random.randint(20,780),-50))

    def build_kamicaze(self):
        return Ship.Kamikaze(vector2.Vector2(random.randint(20,780),-50))

    def build_bombardero(self):
        return Ship.Bombardero(vector2.Vector2(random.randint(20,780),-50))

    def build_vidas(self):
        return Ship.Vidas(vector2.Vector2(random.randint(20,780),-50))

    def build_missil(self):
        print "not implemented"

    def build_kami(self):
        return Ship.Kami(vector2.Vector2(random.randint(20,780),40))

    def build_US(self):
        return Ship.US(vector2.Vector2(random.randint(20,780),40))

    def build_nucleo(self):
        return Ship.Nucleo(vector2.Vector2(random.randint(20,780),40))







