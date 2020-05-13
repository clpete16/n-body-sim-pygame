import pygame
from pygame.locals import *


class GameWindow:

    def __init__(self, settings):

        pygame.init()
        pygame.key.set_repeat(16)

        self.screen = self.make_screen(settings.width, settings.height)
        self.background = self.make_background(settings.width, settings.height)

        self.clock = pygame.time.Clock()
        self.screenScale = 50
        self.camera = [0, 0, 0]

        self.font = pygame.font.get_default_font()
        self.fontsize = 18

        self.staticLabels = []

    def make_screen(self, w, h):
        return pygame.display.set_mode((w, h))

    def make_background(self, w, h):
        bg = pygame.Surface((w, h))
        bg = bg.convert()
        bg.fill([10, 10, 10])
        return bg

    def make_static_label(self, text, color=[200, 200, 200]):
        self.staticLabels.append(pygame.font.Font(
            self.font, self.fontsize).render((text), True, color))

    def draw_static_labels(self):
        # Draw static labels descending from the top left
        labelHeight = 10
        for label in self.staticLabels:
            self.screen.blit(label, (10, labelHeight))
            labelHeight += 35

    def draw_dynamic_labels(self, settings, timeSinceEpoch, objects):
        # Draw dynamic labels descending from the top center
        dateLabel = pygame.font.Font(self.font, self.fontsize).render(
            ("Date: " + f"{(timeSinceEpoch/settings.timescale):.2f}" + settings.timescaleWord), True, [200, 200, 200])
        self.screen.blit(
            dateLabel, (int((settings.width - dateLabel.get_width())/2), 10))

        timescaleLabel = pygame.font.Font(self.font, self.fontsize).render(
            ("Timestep: " + str(round(settings.FPS*settings.timestep/settings.timescale, 1)) + settings.timescaleWord), True, [200, 200, 200])
        self.screen.blit(timescaleLabel,
                         (int((settings.width - timescaleLabel.get_width())/2), 35))

        if settings.centerOnObject:
            centeredAboutLabel = pygame.font.Font(self.font, self.fontsize).render(
                ("Centered about: " + objects[settings.centerObjectNumber].name), True, [200, 200, 200])
            self.screen.blit(centeredAboutLabel,
                            (int((settings.width - centeredAboutLabel.get_width())/2), 60))

    def draw_objects(self, objects, settings):
        if settings.centerObjectNumber >= len(objects):
            settings.centerObjectNumber = 0
        center = objects[settings.centerObjectNumber]
        for obj in objects:
            x = int(self.screenScale*(obj.position[0] - center.position[0] *
                                      settings.centerOnObject) / settings.distScale + settings.width/2 + self.camera[0])
            y = int(self.screenScale*(obj.position[1] - center.position[1] *
                                      settings.centerOnObject) / settings.distScale + settings.height/2 + self.camera[1])
            pygame.draw.circle(self.screen, obj.color, [x, y], int(
                self.screenScale/50*obj.radius), 0)

    def reset_frame(self):
        self.screen.blit(self.background, (0, 0))

    def update_frame(self):
        pygame.display.flip()

    def process_inputs(self, settings):
        for event in pygame.event.get():

            if event.type == QUIT:
                settings.active = False

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    settings.active = False

                if event.key == K_UP:
                    if self.screenScale < 1000:
                        self.screenScale += 5
                elif event.key == K_DOWN:
                    if self.screenScale > 10:
                        self.screenScale -= 5

                if event.key == K_RIGHT:
                    if settings.timestep < settings.maxTimestep / settings.FPS:
                        settings.timestep *= 1.1
                    else:
                        settings.timestep = settings.maxTimestep / settings.FPS

                elif event.key == K_LEFT:
                    if settings.timestep > settings.minTimestep / settings.FPS:
                        settings.timestep /= 1.1
                    else:
                        settings.timestep = settings.minTimestep / settings.FPS

                if event.key == K_a:
                    self.camera[0] += 10
                elif event.key == K_d:
                    self.camera[0] -= 10

                if event.key == K_w:
                    self.camera[1] += 10
                elif event.key == K_s:
                    self.camera[1] -= 10

                if event.key == K_c:
                    self.camera = [0, 0, 0]
                    self.screenScale = 50

                if event.key == K_x:
                    settings.centerOnObject = not settings.centerOnObject
                    self.camera = [0, 0, 0]
                    self.screenScale = 50

                if event.key == K_r:
                    settings.active = False
                    settings.restart = True

                if event.key == K_0:
                    settings.centerObjectNumber = 0

                elif event.key == K_1:
                    settings.centerObjectNumber = 1

                elif event.key == K_2:
                    settings.centerObjectNumber = 2

                elif event.key == K_3:
                    settings.centerObjectNumber = 3

                elif event.key == K_4:
                    settings.centerObjectNumber = 4

                elif event.key == K_5:
                    settings.centerObjectNumber = 5

                elif event.key == K_6:
                    settings.centerObjectNumber = 6

                elif event.key == K_7:
                    settings.centerObjectNumber = 7

                elif event.key == K_8:
                    settings.centerObjectNumber = 8

                elif event.key == K_9:
                    settings.centerObjectNumber = 9

        return settings

    def delay_until_next_frame(self, fps):
        self.clock.tick(fps)

    def make_game_screen_labels(self):
        self.make_static_label("CONTROLS:")
        self.make_static_label("W, A, S, D to move camera")
        self.make_static_label("C to reset camera")
        self.make_static_label("X to center on object")
        self.make_static_label("0-9 to choose center object")
        self.make_static_label("R to reset simulation")
        self.make_static_label("Arrow U/D to zoom")
        self.make_static_label("Arrow L/R to change timestep")
        self.make_static_label("Press escape to quit")

    def make_choice_screen(self):
        rssButton = Button((200, 200, 200), 100, 100, 600, 100, "Real Solar System")
        emButtom = Button((200, 200, 200), 100, 300, 600, 100, "Earth-moon System")
        eightButton = Button((200, 200, 200), 100, 500, 600, 100, "Figure-8 System")
        roidButton = Button((200, 200, 200), 100, 700, 600, 100, "Asteroid Belt System")
        self.buttons = [rssButton, emButtom, eightButton, roidButton]

    def draw_buttons(self):
        for button in self.buttons:
            text = pygame.font.Font(self.font, 60).render((button.text), True, (0, 0, 0))
            pygame.draw.rect(self.screen, button.color, (button.x, button.y, button.width, button.height), 0)
            self.screen.blit(text, (button.x + (button.width/2 - text.get_width()/2), button.y + (button.height/2 - text.get_height()/2)))

class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def isOver(self):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True 
        return False