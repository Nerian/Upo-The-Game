import Ship

import pygame
from pygame.locals import *
from gameobjects import vector2
from utilidades import load_png


class Ship(pygame.sprite.Sprite):

    """La clase Ship contiene los atributos y metodos
        comunes a todos las naves del juego"""

    def __init__(self, imagen, heading, speed, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(imagen)
        self.rect.topleft = pos
        self.heading = heading
        self.speed = speed
        self.time_passed = 0
        self.lastshot = 0

        self.hit = False
        self.hit_time = 1 #how much time is going to last de animation
        self.was_hit = 0 #how much time the animation has been active

        self.life = 0
        self.impact_damage = 0
        self.type = 'ship'

    def update_pos(self):
        #Actualiza la posicion del sprite de acuerdo
        self.heading = self.heading.normalize()
        self.rect.topleft += self.speed * self.heading * self.time_passed

    def update(self, time_passed, screen, clock):
        #Actualiza el estado del objetivo y lo pinta en pantalla
        self.time_passed = time_passed
        self.update_pos()
        screen.blit(self.image, self.rect)
        self.clock = clock
        self.lastshot += self.time_passed
        self.was_hit += self.time_passed

    def check_out_map(self):
        #Devuelve True si el objeto esta fuera del mapa, False en caso contrario
        x,y = self.rect.topleft
        if (x<-100 or y<-100 or x>900 or y>700):
            return True
        else:
            return False

    def impact(self, damage):
        #Actualiza la vida tras recibir un impacto
        self.life = self.life - damage

    def check_death(self):
        #Devuelve True si el objeto esta muerto
        if (self.life < 0):
            return True
        else:
            return False

    def shot_code(self, header, damage):
        #Crea un misil
        posicion_misil = self.rect.midbottom
        misil = Missile(damage, 300, header, posicion_misil)
        return misil

    def is_hit(self, imagen):
        #Actualiza el sprite del objeto al estado de 'tocado'
        self.hit = True
        self.was_hit = 0
        self.image, rect = load_png(imagen)

    def check_hit(self):
        #Cuenta atras para volver al estado natural del objeto
        if(self.hit):
            self.was_hit += self.time_passed
            if(self.was_hit>self.hit_time):
                self.not_hit()
    def not_hit(self, imagen):
        self.hit = False
        self.was_hit = 0
        self.image, rect = load_png(imagen)

    def set_heading(self,tupla):
        self.heading = vector2.Vector2(tupla)



class Wing(Ship):

    """La clase Wing contiene todos los metodos y atributos del jugador"""

    def __init__(self):
        Ship.__init__(self, "Player.png", vector2.Vector2(0,0), 300, [300,300])
        self.life = 700
        self.impact_damage = 100
        self.type = 'Player'

     #Metodos de movimiento
    def move_up(self):
        self.heading[1]=-1

    def move_down(self):
        self.heading[1]=1

    def move_right(self):
        self.heading[0]=1

    def move_left(self):
        self.heading[0]=-1

    def not_move_up(self):
        self.heading[1]=0

    def not_move_down(self):
        self.heading[1]=0

    def not_move_right(self):
        self.heading[0]=0

    def not_move_left(self):
        self.heading[0]=0

    def update_pos(self):
        #Actualiza la posicion del sprite, comprobando si es correcta.
        oldPos = self.rect.topleft
        self.heading = self.heading.normalize()
        self.rect.topleft += self.speed * self.heading * self.time_passed
        if(self.check_out_map()):
            self.rect.topleft = oldPos

    def check_out_map(self):
        #Devuelve True si la posicion del sprite esta dentro del mapa, false en el caso contrario
        x,y = self.rect.topleft
        if (x<0 or y<0 or x>800-self.rect.width or y>600-self.rect.height):
            return True
        else:
            return False

    def shot(self):
        #Crea un objeto misil.
        misil = None
        if(self.lastshot > 0.05):
            x = self.rect.size[0]
            a,b = self.rect.topleft
            posicion_misil = (a+x/2,b-50)
            misil = Missile(40, 350, vector2.Vector2(0,-1), posicion_misil, "misil_player.png")
            self.lastshot = 0
        return misil

    def is_hit(self):
        #Redefinimos la funcion is_hit del padre.
        super(Wing, self).is_hit('Player_hit.png')

    def not_hit(self):
        #Redefinimos la funcion is_hit del padre.
        super(Wing, self).not_hit('Player.png')




class Clone(Ship):

    """La clase Clone contiene todos los atributos y metodos para los clones"""

    def __init__(self, pos = vector2.Vector2(100,50), heading = vector2.Vector2(0,1), speed=140):
        Ship.__init__(self,"Clon.png", heading, speed, pos)
        self.life = 50
        self.impact_damage = 20
        self.score = 20
        self.type = 'Clon'

    def shot(self):

        missil = None
        if(self.lastshot > 2):
            missil = self.shot_code(vector2.Vector2(0,1), 20)
            self.lastshot = 0
        return missil

    def is_hit(self):
        self.hit = True
        self.was_hit = 0
        self.image, rect = load_png('Clon_hit.png')

    def not_hit(self):
        self.hit = False
        self.was_hit = 0
        self.image, rect = load_png("Clon.png")


class Hunter(Ship):

    """La clase Hunter contiene todos los atributos y metodos para los hunters"""

    def __init__(self, pos = vector2.Vector2(100,50), heading = vector2.Vector2(0,1), speed=180):
        Ship.__init__(self,"Hunter.png", heading, speed, pos)
        self.life = 100
        self.impact_damage = 30
        self.score = 100
        self.type = 'Hunter'

    def shot(self):

        missil = None
        if(self.lastshot > 2):
            missil = self.shot_code(vector2.Vector2(0,1), 30)
            self.lastshot = 0
        return missil

    def is_hit(self):
        self.hit = True
        self.was_hit = 0
        self.image, rect = load_png('Hunter_hit.png')

    def not_hit(self):
        self.hit = False
        self.was_hit = 0
        self.image, rect = load_png("Hunter.png")

    def check_attack_zone(self, player):
        #Varia la direccion del hunter hacia donde el player este
        a,b = self.rect.topleft
        x,y = player.rect.topleft

        if(a<x):
            self.set_heading((1,1))
        if(a>x):
            self.set_heading((-1,1))




class Kamikaze (Ship):
    """La clase Kamikaze contiene todos los atributos y metodos para los kamikazes"""
    def __init__(self, pos = vector2.Vector2(100,50), heading = vector2.Vector2(0,1), speed=300):
        Ship.__init__(self,"Kamikaze.png", heading, speed, pos)
        self.life = 40
        self.impact_damage = 60
        self.score = 60
        self.type = 'Kamikaze'


    def shot(self):
        #El Kamikaze no dispara
        return None

    def is_hit(self):
        self.hit = True
        self.was_hit = 0
        self.image, rect = load_png('Kamikaze_hit.png')

    def not_hit(self):
        self.hit = False
        self.was_hit = 0
        self.image, rect = load_png("Kamikaze.png")

    def check_attack_zone(self, player):
        #Varia la direccion del kamikaze hacia donde el player este
        a,b = self.rect.topleft
        x,y = player.rect.topleft

        if(a<x):
            self.set_heading((1,1))
        if(a>x):
            self.set_heading((-1,1))



class Bombardero(Ship):
    def __init__(self, pos = vector2.Vector2(100,50), heading = vector2.Vector2(0,1), speed=110):
        Ship.__init__(self,"Bombardero.png", heading, speed, pos)
        self.life = 40
        self.impact_damage = 80
        self.score = 200
        self.type = 'Bombardero'

    def shot(self):
        #El bombardero no dispara
        return None

    def is_hit(self):
        self.hit = True
        self.was_hit = 0
        self.image, rect = load_png('Bombardero_hit.png')

    def not_hit(self):
        self.hit = False
        self.was_hit = 0
        self.image, rect = load_png("Bombardero.png")


class Vidas(Ship):
    def __init__(self, pos = vector2.Vector2(100,50), heading = vector2.Vector2(0,1), speed=100):
        Ship.__init__(self,"apple.png", heading, speed, pos)
        self.type = 'vida'

class Kami(Ship):
    def __init__(self, pos = vector2.Vector2(100,50), heading = vector2.Vector2(0,0), speed=140):
        Ship.__init__(self,"Kami.png", heading, speed, pos)
        self.life = 5000
        self.impact_damage = 1000
        self.score = 6000
        self.type = 'Boss'

    def check_attack_zone(self, player):
        #Varia la direccion del hunter hacia donde el player este
        a,b = self.rect.topleft
        x,y = player.rect.topleft

        if(a<x):
            self.set_heading((1,0))
        if(a>x):
            self.set_heading((-1,0))

    def shot(self):

        missil = None
        if(self.lastshot > 0.5):
            missil = self.shot_code(vector2.Vector2(0,1), 40)
            self.lastshot = 0
        return missil

    def is_hit(self):
        self.hit = True
        self.was_hit = 0
        self.image, rect = load_png('Kami_hit.png')

    def not_hit(self):
        self.hit = False
        self.was_hit = 0
        self.image, rect = load_png("Kami.png")
        
    def update_pos(self):
        #Actualiza la posicion del sprite, comprobando si es correcta.
        oldPos = self.rect.topleft
        self.heading = self.heading.normalize()
        self.rect.topleft += self.speed * self.heading * self.time_passed
        if(self.check_out_map()):
            self.rect.topleft = oldPos

class US(Ship):
    def __init__(self, pos = vector2.Vector2(100,50), heading = vector2.Vector2(0,0), speed=190):
        Ship.__init__(self,"US.png", heading, speed, pos)
        self.life = 7000
        self.impact_damage = 1000
        self.score = 10000
        self.type = 'Boss'

    def check_attack_zone(self, player):
        #Varia la direccion del hunter hacia donde el player este
        a,b = self.rect.topleft
        x,y = player.rect.topleft

        if(a<x):
            self.set_heading((1,0))
        if(a>x):
            self.set_heading((-1,0))

    def shot(self):

        missil = None
        if(self.lastshot > 0.5):
            missil = self.shot_code(vector2.Vector2(0,1), 40)
            self.lastshot = 0
        return missil

    def is_hit(self):
        self.hit = True
        self.was_hit = 0
        self.image, rect = load_png('US_hit.png')

    def not_hit(self):
        self.hit = False
        self.was_hit = 0
        self.image, rect = load_png("US.png")

    def update_pos(self):
        #Actualiza la posicion del sprite, comprobando si es correcta.
        oldPos = self.rect.topleft
        self.heading = self.heading.normalize()
        self.rect.topleft += self.speed * self.heading * self.time_passed
        if(self.check_out_map()):
            self.rect.topleft = oldPos

class Nucleo(Ship):
    def __init__(self, pos = vector2.Vector2(100,50), heading = vector2.Vector2(0,0), speed=50):
        Ship.__init__(self,"Nucleo.png", heading, speed, pos)
        self.life = 1000
        self.impact_damage = 1000
        self.score = 100000
        self.type = 'Boss'

    def check_attack_zone(self, player):
        #Varia la direccion del hunter hacia donde el player este
        a,b = self.rect.topleft
        x,y = player.rect.topleft

        if(a<x):
            self.set_heading((1,0))
        if(a>x):
            self.set_heading((-1,0))

    def shot(self):

        missil = None
        if(self.lastshot > 0.5):
            missil = self.shot_code(vector2.Vector2(0,1), 40)
            self.lastshot = 0
        return missil

    def is_hit(self):
        self.hit = True
        self.was_hit = 0
        self.image, rect = load_png('Nucleo_hit.png')

    def not_hit(self):
        self.hit = False
        self.was_hit = 0
        self.image, rect = load_png("Nucleo.png")

    def update_pos(self):
        #Actualiza la posicion del sprite, comprobando si es correcta.
        oldPos = self.rect.topleft
        self.heading = self.heading.normalize()
        self.rect.topleft += self.speed * self.heading * self.time_passed
        if(self.check_out_map()):
            self.rect.topleft = oldPos


class Missile(Ship):
    def __init__(self, damage, speed, heading, pos, imagen = "misil_player2.png"):
        Ship.__init__(self, imagen, heading, speed, pos)
        self.impact_damage = damage
        self.type = 'Missil'

    def check_out_map(self):
        #Devuelve True si la posicion del sprite esta fuera del mapa, false en el caso contrario
        x,y = self.rect.topleft

        if (x<0 or y<-self.rect.height or x>800 or y>600):
            return True
        else:
            return False

    def update_pos(self):
        self.heading = self.heading.normalize()
        self.rect.topleft += self.speed * self.heading * self.time_passed