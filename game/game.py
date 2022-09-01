import pygame
import pytmx
import pyscroll

from players.player import Player
class Game:
    def __init__(self):
        #creer la fenetre du jeu
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Pygamon - Aventure")

        #charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("assets/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        self.map = "world"

        #generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x,player_position.y)

        # Définir une liste qui stocke les rectangles de collision

        self.walls = []
        for obj in tmx_data.objects:
                if obj.name == "collision": # TODO : à améliorer
                    self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        #Definir le rectangle pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enterHouse1')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def switch_house(self):
        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("assets/redHouse.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Définir une liste qui stocke les rectangles de collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":  # TODO : à améliorer
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # récupérer le point de spawn
        spawn_house_point = tmx_data.get_object_by_name("spawnHouse")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

        # Definir le rectangle pour sortir de la maison
        enter_house = tmx_data.get_object_by_name('exitHouse')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)



    def switch_world(self):
        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame("assets/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Définir une liste qui stocke les rectangles de collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":  # TODO : à améliorer
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # Definir le rectangle pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enterHouse1')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        #récupérer le point de spawn
        spawn_house_point = tmx_data.get_object_by_name("exitHouse1")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y

    def update(self):
        self.group.update()

        #vérifier si on rentre dans une maison
        if self.map == "world" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = "house"

        # vérifier si on rentre dans une maison
        if self.map == "house" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = "world"

        #check env
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()


    def run(self):
        clock = pygame.time.Clock()

        #boucle du jeu
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()