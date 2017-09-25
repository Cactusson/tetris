import pygame as pg

from .. import tools, prepare
from ..components.animations import Animation
from ..components.label import Label
from ..components.buttonsystem import ButtonSystem
# from ..components.task import Task


class Menu(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.basic_image = self.make_image()
        self.rect = self.basic_image.get_rect(
            center=prepare.SCREEN_RECT.center)
        self.button_system = ButtonSystem(
            self.button_call, ['PLAY', 'HIGH SCORE', 'SETTINGS', 'QUIT'])
        self.update_image()
        self.last_image = None
        self.animations = pg.sprite.Group()
        self.tasks = pg.sprite.Group()
        self.play = True

    def start(self):
        self.play = True
        self.left_gates, self.right_gates = self.make_gates()
        self.gates = pg.sprite.Group(self.left_gates, self.right_gates)

    def start_from_highscore(self, image, rect):
        # self.gates.empty()
        self.play = False
        self.last_image = pg.sprite.Sprite()
        self.last_image.image = image
        self.last_image.rect = rect
        self.rect.right = self.last_image.rect.left - 500
        animation = Animation(
            x=self.last_image.rect.x + self.last_image.rect.width + 500,
            y=self.rect.y, duration=1000, round_values=True)
        animation.callback = self.set_play
        animation.start(self.last_image.rect)
        self.animations.add(animation)
        animation = Animation(
            x=200, y=self.last_image.rect.y,
            duration=1000, round_values=True)
        animation.start(self.rect)
        self.animations.add(animation)

    def make_image(self):
        width, height = 400, 500
        image = pg.Surface((width, height)).convert()
        image.fill(pg.Color('#B2704E'))
        title = Label('Quicksand-Regular', 100, 'TETRIS', pg.Color('black'),
                      center=(width // 2, height // 2 - 200))
        image.blit(title.image, title.rect)
        return image

    def make_gates(self):
        left_gates = pg.sprite.Sprite()
        left_gates.image = prepare.GFX['other']['gates_left2']
        left_gates.rect = left_gates.image.get_rect(topleft=(-400, 0))

        right_gates = pg.sprite.Sprite()
        right_gates.image = prepare.GFX['other']['gates_right2']
        right_gates.rect = right_gates.image.get_rect(topleft=(800, 0))

        return left_gates, right_gates

    def make_animations(self, opening=True):
        if self.animations:
            self.animations.empty()
        self.play = False
        if opening:
            x_left = -400
            x_right = 800
            callback = self.set_play
        else:
            x_left = 0
            x_right = 300
            callback = self.finish
        left_animation = Animation(
            x=x_left, y=0, duration=750, round_values=True,
            transition='in_sine')
        left_animation.callback = callback
        left_animation.start(self.left_gates.rect)
        right_animation = Animation(
            x=x_right, y=0, duration=750, round_values=True,
            transition='in_sine')
        right_animation.start(self.right_gates.rect)
        self.animations.add(left_animation, right_animation)

    def button_call(self, name):
        if name == 'PLAY':
            self.make_animations(False)
        elif name == 'HIGH SCORE':
            self.next = 'HIGHSCORE'
            self.persist['last_image'] = self.image.copy(), self.rect.copy()
            self.done = True
        elif name == 'SETTINGS':
            self.next = 'SETTINGS'
            self.persist['last_image'] = self.image.copy(), self.rect.copy()
            self.done = True
        elif name == 'QUIT':
            self.quit = True

    def set_play(self):
        self.play = True

    def finish(self):
        self.next = 'GAME'
        self.done = True

    def update_image(self):
        self.image = self.basic_image.copy()
        self.button_system.rect.center = (self.rect.width // 2,
                                          self.rect.height // 2 + 50)
        self.image.blit(self.button_system.image, self.button_system.rect)

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        if self.previous == 'GAME':
            self.make_animations(True)
        elif self.previous == 'HIGHSCORE' or self.previous == 'CONTROLS':
            image, rect = self.persist['last_image']
            del self.persist['last_image']
            self.start_from_highscore(image, rect)
        else:
            self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            elif self.play:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.button_system.next_button('up')
                    self.update_image()
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.button_system.next_button('down')
                    self.update_image()
                elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.button_system.press_button()
                elif event.key == pg.K_m:
                    if prepare.music_volume > 0:
                        prepare.music_volume -= 0.1
                        if prepare.music_volume < 0:
                            prepare.music_volume = 0
                        pg.mixer.music.set_volume(prepare.music_volume)
                elif event.key == pg.K_k:
                    if prepare.music_volume < 1.0:
                        prepare.music_volume += 0.1
                        if prepare.music_volume > 1.0:
                            prepare.music_volume = 1.0
                        pg.mixer.music.set_volume(prepare.music_volume)

    def draw(self, surface):
        surface.fill(pg.Color('#CD9D77'))
        surface.blit(self.image, self.rect)
        if self.last_image:
            surface.blit(self.last_image.image, self.last_image.rect)
        self.gates.draw(surface)

    def update(self, surface, current_time, dt):
        self.current_time = current_time
        self.animations.update(dt * 1000)
        self.tasks.update(dt * 1000)
        self.draw(surface)
