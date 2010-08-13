


#   UPO: The Game
#   Un proyecto de Gonzalo Rodriguez-Baltanas Diaz (siotopo@gmail.com)
#   Tutorizado por Domingo Savio Rodriguez Baena (dsrodbae@upo.es)
#   Curso 2008-2009  2 ITIG   Universidad Pablo de Olavide
#


#Trucos      Pulsa la tecla   A    ^_^








import random
import pygame.sprite
import pygame
from pygame.locals import *
from factoria import Factoria
from utilidades import load_png
import random

class Escena ():

    """ Contiene los metodos y atributos necesarios para renderizar la escena logica"""

    def __init__(self):
        self.group_players = pygame.sprite.Group()     #Lista con los jugadores
        self.group_missil = pygame.sprite.Group()      #Lista con todos los misiles
        self.group_enemy = pygame.sprite.Group()        #Lista con todos los enemigos
        self.group_vidas = pygame.sprite.Group()         #Lista con todas las vidas

        self.background, self.rect = load_png("nightSky.png")
        self.textos = Texts()

        self.lastAreaCheck = 0

    def update(self, time_passed, screen, clock):

        self.lastAreaCheck += time_passed

        #Setup background
        screen.fill((0,0,0))
        screen.blit(self.background, self.rect)

        #Update all renderable objects
        self.update_missil(time_passed, screen, clock)
        self.update_players(time_passed, screen, clock)
        self.update_enemy(time_passed, screen, clock)
        self.update_vidas(time_passed, screen, clock)

        #Colissions
        self.check_colission_playerToEnemy()
        self.check_colission_playerToMissil()
        self.check_colission_enemyToMissil()
        self.check_colission_playerToVidas()
        self.check_attack_zone()

        #Garbage collector
        self.check_hit()
        self.check_life_enemy()
        self.check_enemy_out_map()
        #Enemy shot
        self.check_shoting()

        #Texts
        self.update_textos()
        
        pygame.display.update()

    def update_textos(self):
        player = player = self.group_players.sprites()[0]

        self.textos.update(player.life, game.score, game.vidas)
        self.textos.renderAll()

    def update_players(self, time_passed, screen, clock):
        self.group_players.update(time_passed, screen, clock)

    def update_missil(self, time_passed, screen, clock):
        self.group_missil.update(time_passed, screen, clock)
        for item in self.group_missil:
            if item.check_out_map():
                self.group_missil.remove(item)

    def update_enemy(self, time_passed, screen, clock):
        self.group_enemy.update(time_passed, screen, clock)

    def update_vidas(self, time_passed, screen, clock):
        self.group_vidas.update(time_passed, screen, clock)

    def add(self, obj, tipo):
        if(tipo == "player"):
            self.group_players.add(obj)
        if(tipo == "enemy"):
            self.group_enemy.add(obj)
        if(tipo == "missil"):
            self.group_missil.add(obj)
        if(tipo == "vidas"):
            self.group_vidas.add(obj)

    def check_colission_playerToEnemy(self):
        colisions = pygame.sprite.groupcollide(self.group_players, self.group_enemy, False, False)
        iterator = colisions.itervalues()
        player = self.group_players.sprites()[0]

        while True:
            try:
                enemy_list = iterator.next()
                for enemy in enemy_list:
                    player.impact(enemy.impact_damage)
                    enemy.impact(player.impact_damage)
                    player.is_hit()
                    enemy.is_hit()
            except StopIteration:                
                break
        
    def check_colission_playerToMissil(self):
        colisions = pygame.sprite.groupcollide(self.group_players, self.group_missil, False, False)
        iterator = colisions.itervalues()
        player = self.group_players.sprites()[0]
        lista_basura = pygame.sprite.Group()

        while True:
            try:
                missile_list = iterator.next()
                for missil in missile_list:
                    player.impact(missil.impact_damage)
                    player.is_hit()
                    soundExplosion.play()   ########### Sound ################
                    lista_basura.add(missil)
            except StopIteration:                
                break

        self.group_missil.remove(lista_basura)



    def check_colission_enemyToMissil(self):
        colisions = pygame.sprite.groupcollide(self.group_enemy, self.group_missil, False, False)
        iterator = colisions.iterkeys()
        missil_dead = pygame.sprite.Group()

        while True:
            try:
                enemy = iterator.next()
                for missil in colisions[enemy]:
                    enemy.impact(missil.impact_damage)
                    missil_dead.add(missil)
                    enemy.is_hit()
                    soundExplosionEnemy.play()  ################# Sound ###########
                    #self.group_missil.remove(missil)
            except StopIteration:
                break
        self.group_missil.remove(missil_dead)

    def check_colission_playerToVidas(self):
        colisions = pygame.sprite.groupcollide(self.group_players, self.group_vidas, False, False)
        iterator = colisions.itervalues()
        player = self.group_players.sprites()[0]
        lista_basura = pygame.sprite.Group()

        while True:
            try:
                lista_vidas = iterator.next()
                for vidas in lista_vidas:
                    player.life = 700
                    lista_basura.add(vidas)
            except StopIteration:
                break

        self.group_vidas.remove(lista_basura)

    def check_life_enemy(self):
        listaMuertos = pygame.sprite.Group()
        player = self.group_players.sprites()[0]

        for ship in self.group_enemy.sprites():
            if(ship.check_death()):
                listaMuertos.add(ship)
                game.addScore(ship.score)

                soundExplosionDeath.play() ############# Sound ##################
                #ship.is_hit('Player_hit.png')
                #ship.die()
        self.group_enemy.remove(listaMuertos)

    def check_enemy_out_map(self):
        listaEnemigosFuera = pygame.sprite.Group()

        for ship in self.group_enemy.sprites():
            if(ship.check_out_map()):
                listaEnemigosFuera.add(ship)

        self.group_enemy.remove(listaEnemigosFuera)


    def check_shoting(self):
        for ship in self.group_enemy.sprites():
            missil = ship.shot()
            if(missil != None):
                self.add(missil, "missil")

    def check_hit(self):
        for ship in self.group_enemy.sprites():
            ship.check_hit()
        for ship in self.group_players.sprites():
            ship.check_hit()

    def check_attack_zone(self):
        #Cambia el vector de direccion para aqueias naves que sigan al player
        player = player = self.group_players.sprites()[0]

        if(self.lastAreaCheck >1):
            for ship in self.group_enemy.sprites():
                
                if(ship.type == 'Hunter'):
                    if(self.getProbability(40)):
                        ship.check_attack_zone(player)
                elif (ship.type == 'Kamikaze'):
                    if(self.getProbability(40)):
                        ship.check_attack_zone(player)
                elif(ship.type == 'Boss'):
                    if(self.getProbability(99)):
                        ship.check_attack_zone(player)

            self.lastAreaCheck = 0

    def getProbability(self,probability):
        number = random.randint(0,100)

        if number < probability:
            return True
        else:
            return False







class Game():

    def __init__(self):
        
        #Inicializamos el relog
        self.clock = pygame.time.Clock()

        #Creamos el objeto de escena y factoria
        self.escena = Escena()
        self.factoria = Factoria()

        #Players
        self.player = self.factoria.build_player()
        self.vidas = 7
        self.score = 0

        #Tiempo en el nivel
        self.level_time = 0
        self.time_passed = 0

    def update(self):
        self.time_passed = self.clock.tick(30)/1000.0
        self.getEvent()
        self.escena.update(self.time_passed, screen, self.clock)


    def getEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.player.life +=1000
                if event.key == K_LEFT:
                    self.player.move_left()
                if event.key == K_RIGHT:
                    self.player.move_right()
                if event.key == K_DOWN:
                    self.player.move_down()
                if event.key == K_UP:
                    self.player.move_up()
                if event.key == K_SPACE:
                    missil = self.player.shot()
                    if(missil != None):
                        self.escena.add(missil, 'missil')

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    self.player.not_move_left()
                if event.key == K_RIGHT:
                    self.player.not_move_right()
                if event.key == K_DOWN:
                    self.player.not_move_down()
                if event.key == K_UP:
                    self.player.not_move_up()

    def pruebaClon(self):
        self.escena.add(self.player, "player")
        clon = self.factoria.build_clone()
        self.escena.add(clon, "enemy")

        while not clon.check_death():
            self.update()

        if not self.player.check_death():
            return True
        else:
            return False

    def initGame(self):
        self.escena = Escena()
        self.level_time = 0
        self.player = self.factoria.build_player()
        self.score = 0
        self.vidas = 7
        self.time_passed = 0

    def clearLevel(self):
        self.escena = Escena()
        self.level_time = 0
        self.player = self.factoria.build_player()

    def game(self):

        self.initGame()
        while(self.vidas >0):
            if(self.nivel1()):
                break

        while( self.vidas>0):
            if(self.nivel2()):
                break

        while( self.vidas>0):
            if(self.nivel3()):
                break

        while( self.vidas>0):
            if(self.nivel4()):
                break

        while( self.vidas>0):
            if(self.nivel5()):
                break

        while( self.vidas>0):
            if(self.nivel6()):
                break

        while( self.vidas>0):
            if(self.nivel7()):
                break

        self.clearLevel()
        self.creditos()

    def nivel1(self):
        self.clearLevel()
        self.escena.add(self.player, "player")

        while not self.levelTime(60) and not self.player.check_death():
            self.update()
            self.addKamikaze(40)
            self.addVidas(1)

        if(not self.player.check_death()):
            self.finNivelTexto(1)

        return self.finNivel()



        
    def nivel2(self):
        self.clearLevel()
        self.escena.add(self.player, "player")
        boss = self.factoria.build_kami()

        while not self.levelTime(60) and not self.player.check_death():
            self.update()
            self.addClone(30)
            self.addKamikaze(30)
            self.addVidas(1)

        if(not self.player.check_death()):
            self.escena.add(boss, "enemy")
            while not self.player.check_death() and not boss.check_death():
                self.update()
                self.addVidas(1)
                self.addKamikaze(50)

        if(not self.player.check_death()):
            self.level_time = 0
            while not self.levelTime(5):
                self.update()
            self.finNivelTexto(2)

        return self.finNivel()

    def nivel3(self):
        self.clearLevel()
        self.escena.add(self.player, "player")
        while not self.levelTime(60) and not self.player.check_death():
            self.update()
            self.addClone(20)
            self.addHunter(25)
            self.addKamikaze(25)
            self.addVidas(1)

        if(not self.player.check_death()):
            self.finNivelTexto(3)

        return self.finNivel()
        
    def nivel4(self):
        self.clearLevel()
        self.escena.add(self.player, "player")
        while not self.levelTime(60) and not self.player.check_death():
            self.update()
            self.addClone(30)
            self.addHunter(30)
            self.addBombardero(30)
            self.addVidas(1)
            self.addKamikaze(10)

        if(not self.player.check_death()):
            self.finNivelTexto(4)

        return self.finNivel()
        
    def nivel5(self):
        self.clearLevel()
        self.escena.add(self.player, "player")
        boss = self.factoria.build_US()

        
        while not self.levelTime(60) and not self.player.check_death():
            self.update()
            self.addClone(30)
            self.addHunter(30)
            self.addVidas(1)
            self.addKamikaze(20)

        if(not self.player.check_death()):
            self.escena.add(boss, "enemy")
            while not self.player.check_death() and not boss.check_death():
                self.update()
                self.addVidas(1)
                self.addHunter(70)

        if(not self.player.check_death()):
            self.level_time = 0

            while not self.levelTime(5):
                self.update()

            self.finNivelTexto(5)


        return self.finNivel()

    def nivel6(self):
        self.clearLevel()
        self.escena.add(self.player, "player")
        while not self.levelTime(60) and not self.player.check_death():
            self.update()
            self.addClone(40)
            self.addHunter(40)
            self.addKamikaze(40)
            self.addVidas(1)

        if(not self.player.check_death()):
            self.finNivelTexto(6)

        return self.finNivel()

    def nivel7(self):
        self.clearLevel()
        self.escena.add(self.player, "player")
        boss = self.factoria.build_nucleo()

        while not self.levelTime(60) and not self.player.check_death():
            self.update()
            self.addKamikaze(60)
            self.addHunter(60)
            self.addVidas(1)

        if(not self.player.check_death()):
            self.escena.add(boss, "enemy")
            while not self.player.check_death() and not boss.check_death():
                self.update()
                self.addVidas(1)
                self.addKamikaze(70)

        if(not self.player.check_death()):
            self.finJuegoTexto()
        return self.finNivel()


    def levelTime(self, time):
        #Devuelve True si es hora de terminar el nivel
        self.level_time += self.time_passed
        if(self.level_time > time):
            return True
        else:
            return False


    def getProbability(self,probability):
        number = random.randint(0,1000)

        if number < probability:
            return True
        else:
            return False

    def addClone(self, probability):
        if self.getProbability(probability):
            self.escena.add(self.factoria.build_clone(), "enemy")

    def addHunter(self, probability):
        if self.getProbability(probability):
            self.escena.add(self.factoria.build_hunter(), "enemy")

    def addKamikaze(self, probability):
        if self.getProbability(probability):
            self.escena.add(self.factoria.build_kamicaze(), "enemy")

    def addBombardero(self, probability):
        if self.getProbability(probability):
            self.escena.add(self.factoria.build_bombardero(), "enemy")

    def addVidas(self, probability):
        if self.getProbability(probability):
            self.escena.add(self.factoria.build_vidas(), "vidas")

    def addScore(self, score):
        self.score +=score

    def loseLevel(self):
        #Te resta una vida
        if(self.vidas>0):
            self.vidas -=1

    def finNivel(self):
        if(not self.player.check_death()):
            return True
        else:
            self.loseLevel()
            return False
        
    def finNivelTexto(self, nivel):
        #Genera y escribe en pantalla el texto de 'Has pasado al nivel X'
        font_nivel = pygame.font.SysFont("arial",40)
        surfaceNivel = font_nivel.render("Has superado el nivel "+str(nivel), True, (255,100,255))
        screen.blit(surfaceNivel, (250,300))
        pygame.display.update()
        
        self.level_time = 0
        self.time_passed = 0

        while not self.levelTime(4):
            self.time_passed = self.clock.tick(30)/1000.0
            self.getEvent()

    def finJuegoTexto(self):
        #Genera y escribe en pantalla el texto 'Has ganado!!!!'
        font_nivel = pygame.font.SysFont("arial",40)
        surfaceNivel = font_nivel.render("has ganado!!!!", True, (255,100,255))
        screen.blit(surfaceNivel, (250,300))
        pygame.display.update()

        self.level_time = 0
        self.time_passed = 0

        while not self.levelTime(4):
            self.time_passed = self.clock.tick(30)/1000.0
            self.getEvent()

    def creditos(self):
        #Genera y escribe en pantalla los creditos
        font_nivel = pygame.font.SysFont("arial",40)
        surfaceNivel = font_nivel.render("Programming, design, concept: Gonzalo Rodriguez-Baltanas Diaz", True, (255,100,255))
        screen.blit(surfaceNivel, (250,300))
        pygame.display.update()

        self.level_time = 0
        self.time_passed = 0

        while not self.levelTime(8):
            self.time_passed = self.clock.tick(30)/1000.0
            self.getEvent()








class Texts():

    def __init__(self):
        #Creamos los textos.
        self.font_vida = pygame.font.SysFont("arial",20)
        self.font_puntos = pygame.font.SysFont("arial",20)
        self.vidas = pygame.font.SysFont("arial",20)
        self.surfaceVida = self.font_vida.render("Vida: "+str(0), True, (255,255,255))
        self.surfacePuntos = self.font_puntos.render("Puntos:  "+str(0), True,(255,255,255))
        self.surfaceVidas = self.font_puntos.render("Vidas:  "+str(0), True,(255,255,255))

    def update(self, vida=200, puntos=100, vidas = 7):
        #Renderizamos las texturas los textos
        self.surfaceVida = self.font_vida.render("Vida: "+str(vida), True,(255,255,255))
        self.surfacePuntos = self.font_puntos.render("Puntos:  "+str(puntos), True,(255,255,255))
        self.surfaceVidas = self.font_puntos.render("Vidas:  "+str(vidas), True,(255,255,255))
        
    def renderAll(self):
        screen.blit(self.surfaceVida, (10,20))
        screen.blit(self.surfacePuntos, (10,40))
        screen.blit(self.surfaceVidas, (10,60))

##########################  Main Def ##################################


######################### The Main ######################################################

#Inicializamos Pygame
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

soundExplosion = pygame.mixer.Sound("Data/explosion.ogg")
soundExplosion.set_volume(0.2)
soundExplosionDeath = pygame.mixer.Sound("Data/explosionDeath.ogg")
soundExplosionDeath.set_volume(0.2)
soundExplosionEnemy = pygame.mixer.Sound("Data/explosionEnemy.ogg")
soundExplosionEnemy.set_volume(0.2)

pygame.mixer.music.load("Data/StarWar.ogg")
pygame.mixer.music.play(-1)


#Inicializamos la superficie principal
screen = pygame.display.set_mode((800, 600), 0, 32)
game = Game()

#Definimos el titulo de la ventana
pygame.display.set_caption("Upo: The Game")


"""Main game loop"""

game.game()


