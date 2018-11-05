# --------------- Imports ---------------

import pygame
from pygame.locals import *
from PIL import Image

from OpenGL.GL import *
from OpenGL.GLU import *
from random import randrange
from random import randint

import MapGen

import classes

# --------------- Constants ---------------

tex_deep  = classes.TexEnum(0)
tex_shall = classes.TexEnum(100)
tex_sand  = classes.TexEnum(200)
tex_grass = classes.TexEnum(300)
tex_mount = classes.TexEnum(400)

# --------------- Predefines ---------------

if not pygame.font:
    print("Error occurred")
if not pygame.mixer:
    print("Error occurred")

window_width = 1600
window_height = 900

debug = True

# --------------- Functions ---------------

def list_to_txt(name, tlist):
    to_file = open(name, "w")
    i = 0
    for elem in tlist:
        to_file.write(str(elem) + " ")
        if i % 16 == 15: to_file.write("\n")
        i += 1
    to_file.close()



class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.mouse_pos = [0, 0]
        self.background = pygame.image.load("Map_Old.bmp").convert()
        headline_font = pygame.font.SysFont('Arial', 100)
        self.headline = headline_font.render("Conquest Of The New World", False, (0, 0, 0))
        self.menu_box = pygame.Surface((1000, 500))
        self.menu_box.set_alpha(128)
        self.menu_box.fill((255, 255, 255))

        self.btn_solitaire_game = classes.Button(300, 600, True, "New Solitair Game", "Button_Disabled.bmp",
                                                 "Button_Enabled.bmp",
                                                 "Button_Clicked.bmp")
        self.btn_load_game = classes.Button(300, 640, True, "Load Solitair Game", "Button_Disabled.bmp",
                                            "Button_Enabled.bmp",
                                            "Button_Clicked.bmp")
        self.btn_quit = classes.Button(300, 680, True, "Quit Game", "Button_Disabled.bmp", "Button_Enabled.bmp",
                                       "Button_Clicked.bmp")
        self.btn_options = classes.Button(300, 720, True, "Options", "Button_Disabled.bmp", "Button_Enabled.bmp",
                                          "Button_Clicked.bmp")

    def setup(self):
        return 11

    def update(self):

        mouse_counter = 0
        mouse_counter_old = 0
        self.mouse_pos = pygame.mouse.get_pos()

        #self.screen.\
        OPENGLBLIT(self.background, [0, 0])
        self.screen.OPENGLBLIT(self.headline, [200, 200])
        self.screen.OPENGLBLIT(self.menu_box, (200, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_counter += 1

        if mouse_counter != mouse_counter_old:
            mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
        else:
            mouse_left, mouse_middle, mouse_right = False, False, False
            mouse_counter = 0

        mouse_counter_old = mouse_counter

        self.btn_solitaire_game.hover(self.mouse_pos[0], self.mouse_pos[1])
        self.btn_solitaire_game.ogl_draw(self.screen)
        self.btn_load_game.hover(self.mouse_pos[0], self.mouse_pos[1])
        self.btn_load_game.ogl_draw(self.screen)
        self.btn_options.hover(self.mouse_pos[0], self.mouse_pos[1])
        self.btn_options.ogl_draw(self.screen)
        self.btn_quit.hover(self.mouse_pos[0], self.mouse_pos[1])
        self.btn_quit.ogl_draw(self.screen)

        pygame.display.flip()

        if self.btn_solitaire_game.clicked(mouse_left):
            return 20
        elif self.btn_quit.clicked(mouse_left):
            return 0
            print("quit")
        else:
            return 11

    def end(self):
        pass


class Game:
    def __init__(self,screen):                                                                                          # zum initialisieren des Levels werden einige Elemente initialisiert
        self.screen = screen                                                                                            # der Screen enthält die Bildelemente
        self.top_menu = pygame.Surface((1200, 35))
        #self.top_menu.set_alpha()
        self.top_menu.fill((120, 120, 120))

        self.zoom = 1

        self.mouse_pos = [0, 0]                                                                                         # initialisiere die Maus

        self.btn_end_round = classes.Button(10, 5, True, "End Round", "Button_Disabled.bmp",
                                            "Button_Enabled.bmp", "Button_Clicked.bmp")
        self.btn_quit = classes.Button(270, 5, True, "Quit Game", "Button_Disabled.bmp",
                                       "Button_Enabled.bmp", "Button_Clicked.bmp")
        self.btn_zoom_in = classes.Button(540, 5, True, "Zoom In", "Button_Disabled.bmp", "Button_Enabled.bmp",
                                          "Button_Clicked.bmp")
        self.btn_zoom_out = classes.Button(810, 5, True, "Zoom Out", "Button_Disabled.bmp", "Button_Enabled.bmp",
                                           "Button_Clicked.bmp")

        self.cam = classes.Camera(100, 100, 10000)

        self.t_wdeep = pygame.image.load("waterdeep_iso.png").convert_alpha()
        self.t_wdeep_shall = pygame.image.load("water_deep_shallow_iso.png").convert_alpha()
        self.t_wshallow  = pygame.image.load("watershallow_iso.png").convert_alpha()

    def setup(self):                                                                                      # setup sollte nur einmal aufgerufen werden, hier werden Gamerelevante teile initialisiert

        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        return 21

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        mouse_counter = 0
        mouse_counter_old = 0
        mouse_left, mouse_middle, mouse_right = 0, 0, 0
        quit = False

        event_flag = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.cam.move(0, -50)
                if event.key == pygame.K_UP:
                    self.cam.move(0, 50)
                if event.key == pygame.K_LEFT:
                    self.cam.move(50, 0)
                if event.key == pygame.K_RIGHT:
                    self.cam.move(-50, 0)
                if event.key == pygame.K_ESCAPE:
                        quit = True
                event_flag = True
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_counter += 1

        if mouse_counter != mouse_counter_old:
            mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
        else:
            mouse_left, mouse_middle, mouse_right = False, False, False
            mouse_counter = 0
        mouse_counter_old = mouse_counter

        scale_x = int(self.zoom * 64)
        scale_y = int(self.zoom * 32)

        # draw map on screen
        if event_flag:
            self.screen.fill((0, 0, 0))
            for y in range(0, 512):
                for x in range(0, 512):
                    cart_x = x * scale_y
                    cart_y = y * scale_y

                    iso_x = cart_x - cart_y
                    iso_y = (cart_x + cart_y)/2

                    draw_x = iso_x+self.cam.x
                    draw_y = iso_y+self.cam.y

                    if draw_x > -scale_x and draw_y > -scale_x and draw_x < window_width + scale_x and draw_y < window_height + scale_x:



                        if y < 100 :
                            tile = pygame.transform.scale(self.t_wdeep,(scale_x, scale_y))
                        elif y == 100:
                            tile = pygame.transform.scale(self.t_wdeep_shall, (scale_x, scale_y))
                        else:
                            tile = pygame.transform.scale(self.t_wshallow, (scale_x, scale_y))
                        self.screen.blit(tile, (draw_x, draw_y))


        # get together main screen
        self.screen.blit(self.top_menu, (0, 0))
        self.btn_end_round.hover(self.mouse_pos[0], self.mouse_pos[1])
        self.btn_end_round.draw(self.screen)
        self.btn_quit.hover(self.mouse_pos[0], self.mouse_pos[1])
        self.btn_quit.draw(self.screen)
        self.btn_zoom_in.hover(self.mouse_pos[0], self.mouse_pos[1])
        self.btn_zoom_in.draw(self.screen)
        self.btn_zoom_out.hover(self.mouse_pos[0], self.mouse_pos[1])
        self.btn_zoom_out.draw(self.screen)

        pygame.display.flip()

        quit = self.btn_quit.clicked(mouse_left)

        if self.btn_zoom_in.clicked(mouse_left):
            self.zoom *=2
            print(self.zoom)
        if self.btn_zoom_out.clicked(mouse_left):
            self.zoom /= 2
            print(self.zoom)

        if quit:
            return 10
            print("quit")
        else:
            return 21

class Texture:
    def __init__(self, texture):
        self.coords = [[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]]
        print(self.coords)
        self.image = pygame.image.load(texture).convert()
        self.data  = pygame.image.tostring(self.image,"RGBA",1)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def bind(self):
        glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)
        tex_name = [0]
        glBindTexture(GL_TEXTURE_2D,tex_name[0])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        return texid


class Terrain_World:
    def __init__(self, screen, size):
        self.size = size
        self.verticies = []
        self.edges = []
        self.surfaces = []

        # generate map
        # zuerst die Distribution ermitteln
        dist = MapGen.Dist_Function(size, 0.8)
        dist.calcdist()
        dist.clean(4, 1)
        # seed generieren
        seedmap = MapGen.Seedmap(size)
        seedmap.drawfromdist(dist)
        # nun die heightmap zeichnen
        self.heightmap = MapGen.Heightmap(size, 2)
        self.heightmap.gen2_prep(seedmap)
        self.heightmap.slopedown()
        self.heightmap.cleanup()



        # setting up verticies
        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.heightmap.map[x][y] < 0:
                    z = 0
                else:
                    z = self.heightmap.map[x][y] * 0.5
                self.verticies.append((x, y, z))


        #setting up edges
        for j in range(0, self.size):
            for i in range(0, self.size):
                if i - 1 >= 0:
                    self.edges.append((j * self.size + i, j * self.size + i - 1))
                if j - 1 >= 0:
                    self.edges.append((j * self.size + i, (j - 1) * self.size + i))
                if i-1 >= 0 and j - 1 >= 0:
                    self.edges.append(((j - 1) * self.size + i - 1, j * self.size + i))

        #setting up surfaces
        for j in range(0, self.size):
            for i in range(0, self.size):
                if i-1 >= 0 and j-1 >= 0:
                    self.surfaces.append(((j - 1) * self.size + i - 1, j * self.size + i-1, j * self.size + i, (j - 1) * self.size + i))


        self.deepwater = Texture('Images/WasserTief.png')
        self.shallwater = Texture('Images/WasserSeicht.png')
        self.sand = Texture('Images/Sand.png')
        self.grass = Texture('Images/Grasmitte.png')
        self.mountain = Texture("Images/DunklerSand.png")

        self.screen = screen

    def export_surface(self,name):
        to_file = open(name, "w")
        for surface in self.surfaces:
            to_file.write(str(surface))
            to_file.write("\n")
        to_file.close()

    def export_verticies(self,name):
        to_file = open(name, "w")
        for vertex in self.verticies:
            to_file.write(str(vertex))
            to_file.write("\n")
        to_file.close()

    def terrain(self, lines=False):
        if not lines:
            #self.landtex.bind()
            hlist = self.heightmap.to_list()
            y = 0
            for surface in self.surfaces:
                x = 0

                if hlist[y] == -2:
                    self.deepwater.bind()
                elif hlist[y] == -1:
                    self.shallwater.bind()
                elif hlist[y] == 0:
                    self.sand.bind()
                elif hlist[y] == 1:
                    self.grass.bind()
                elif 2 <= hlist[y] <= 4:
                    self.grass.bind()
                elif hlist[y] >= 5:
                    self.mountain.bind()
                else:
                    self.deepwater.bind()

                glBegin(GL_QUADS)
                for vertex in surface:

                    glColor3fv((0.7, 0.7, 0.7))
                    glTexCoord2f(self.grass.coords[x % 4][0], self.grass.coords[x % 4][1])
                    glVertex3fv(self.verticies[vertex])
                    x += 1
                y += 1
                glEnd()

        else:
            glBegin(GL_LINES)
            for edge in self.edges:
                for vertex in edge:
                    glVertex3fv(self.verticies[vertex])
            glEnd()


    def setup(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.terrain()
        pygame.display.flip()
        return 31

    def update(self):

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.terrain()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    glTranslatef(1.0, 1.0, 0.0)
                    print("down")
                if event.key == pygame.K_UP:
                    glTranslatef(-1.0, -1.0, 0.0)
                    print("up")
                if event.key == pygame.K_LEFT:
                    glTranslatef(1.0, -1.0, 0.0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(-1.0, 1.0, 0.0)
                if event.key == pygame.K_MINUS:
                    glTranslatef(1.0, 1.0, -5.0)
                if event.key == pygame.K_PLUS:
                    glTranslatef(1.0, 1.0, 5.0)
            if event.type == pygame.QUIT:
                quit()

        pygame.display.flip()



# Here begins the main loop for game activities

def main():

    # game engine initialization
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height), DOUBLEBUF|OPENGL)
    gluPerspective(45, (window_width/window_height), 0.1, 50.0)

    glTranslatef(0.0, -12.0, -8.0)

    pygame.display.set_caption("Conquest Of New World")
    pygame.mouse.set_visible(True)
    pygame.key.set_repeat(1, 30)

    clock = pygame.time.Clock()

    mode = 30
    size = 128
    frametime = 0
    frametime_old = 0



    # classes

    menu = Menu(screen)
    game = Game(screen)
    terrain_world = Terrain_World(screen, size)
    #terrain_world.export_surface("testsurface.txt")
    #terrain_world.export_verticies("testvertex.txt")
    #list_to_txt("testliste.txt",terrain_world.heightmap.to_list())

    glRotatef(-45.0, 1, 0, 0)
    glRotatef(45.0, 0, 0, 1)
    running = True
    while running:
        if mode == 30:
            terrain_world.update()
        else:
            if mode == 10:
                mode =menu.setup()
            elif mode == 11:
                mode = menu.update()
            elif mode == 20:
                mode = game.setup()
            elif mode == 21:
                mode = game.update()
            elif mode == 30:
                terrain_world.setup()
            elif mode == 31:
                terrain_world.update()
            elif mode == 0:
                running = False

        clock.tick(50)
        frametime = pygame.time.get_ticks()
        framerate = frametime - frametime_old
        framerate = 1000/framerate
        # print("framerate:", framerate)
        frametime_old = frametime




main()
