import pygame


class Pawn(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pass


class Camera(Pawn):
    def __init__(self, x, y, size):
        super().__init__(x, y)
        self.size = size

    def move(self, x, y):

        if self.x + x <= -1000:
            self.x = 0
        elif self.x + x >= self.size:
            self.x = self.size
        else:
            self.x += x

        if self.y + y <= -2000:
            self.y = 0
        elif self.y + y >= 200:
            self.y = 200
        else:
            self.y += y


class Button(Pawn):
    def __init__(self, x, y, enabled, button_text, pic_disabled, pic_enabled, pic_clicked):
        super().__init__(x, y)
        self.enabled = enabled
        self.pic_disabled = pygame.image.load(pic_disabled)
        self.pic_enabled = pygame.image.load(pic_enabled)
        self.pic_clicked = pygame.image.load(pic_clicked)
        self.hovered = False
        self.button_text = button_text
        btn_font = pygame.font.SysFont('Arial', 30)
        self.btn_text = btn_font.render(self.button_text, True, (255, 255, 255))

    def draw(self, screen):

        if not self.enabled:
            screen.blit(self.pic_disabled, (self.x, self.y))
        else:
            if self.hovered:
                screen.blit(self.pic_enabled, (self.x, self.y))
            else:
                screen.blit(self.pic_disabled, (self.x, self.y))

        screen.blit(self.btn_text, (self.x+16, self.y+1))

    def ogl_draw(self, screen):
        if not self.enabled:
            screen.OPENGLBLIT(self.pic_disabled, (self.x, self.y))
        else:
            if self.hovered:
                screen.OPENGLBLIT(self.pic_enabled, (self.x, self.y))
            else:
                screen.OPENGLBLIT(self.pic_disabled, (self.x, self.y))

        screen.OPENGLBLIT(self.btn_text, (self.x+16, self.y+1))

    def hover(self, mouse_x, mouse_y, sys_debug=False):
        self.hovered = self.x < mouse_x < self.x + 256 and self.y < mouse_y < self.y + 32
        if self.hovered and sys_debug:
            print("hovered")

    def clicked(self, click):
        if self.hovered and click:
            return True
        else:
            return False


class TexEnum:
    def __init__(self, base_val):
        self.base_val = base_val

        self.ALL = 0 + base_val
        self.UP = 1 + base_val
        self.LEFT = 2 + base_val
        self.DOWN = 3 + base_val
        self.RIGHT = 4 + base_val
        self.ULEFT = 11 + base_val
        self.DLEFT = 12 + base_val
        self.DRIGHT = 13 + base_val
        self.URIGHT = 14 + base_val
        self.LUR = 21 + base_val
        self.ULD = 22 + base_val
        self.LDR = 23 + base_val
        self.DRU = 24 + base_val
        self.CORE = 30 + base_val

# End of File
