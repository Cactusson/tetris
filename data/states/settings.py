import pygame as pg

from .. import tools, prepare
from ..components.animations import Animation
from ..components.settings_module import SettingsModule


class Settings(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.settings_module = SettingsModule(self.button_call)
        self.image = self.settings_module.image
        self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)
        self.last_image = None
        self.animations = pg.sprite.Group()
        self.play = False

    def start_from_menu(self, image, rect):
        self.play = False
        self.last_image = pg.sprite.Sprite()
        self.last_image.image = image
        self.last_image.rect = rect
        self.rect.left = self.last_image.rect.right + 300
        animation = Animation(
            x=self.last_image.rect.x - self.last_image.rect.width - 500,
            y=self.rect.y, duration=1000, round_values=True)
        animation.callback = self.set_play
        animation.start(self.last_image.rect)
        self.animations.add(animation)
        animation = Animation(
            x=100, y=self.last_image.rect.y,
            duration=1000, round_values=True)
        animation.start(self.rect)
        self.animations.add(animation)

    def set_play(self):
        self.play = True

    def update_image(self):
        self.settings_module.update_image()
        self.image = self.settings_module.image

    def button_call(self, name):
        if name == 'SOUND':
            self.settings_module.change_to_sound()
            self.update_image()
        elif name == 'CONTROLS':
            self.settings_module.change_to_controls()
            self.update_image()
        elif name == 'BACK':
            if self.settings_module.state == 'MAIN':
                if self.previous == 'MENU':
                    self.next = 'MENU'
                    self.persist['last_image'] = (self.image.copy(),
                                                  self.rect.copy())
                    self.done = True
                elif self.previous == 'PAUSE':
                    self.next = 'PAUSE'
                    self.done = True
            else:
                self.settings_module.start()
                self.update_image()
        else:
            if self.settings_module.button_system.active_button is None:
                return
            self.settings_module.button_system.toggle_lock()
            self.update_image()

    def startup(self, current_time, persistant):
        self.start_time = current_time
        self.persist = persistant
        self.settings_module.start()
        self.update_image()
        if self.previous == 'MENU':
            image, rect = self.persist['last_image']
            del self.persist['last_image']
            self.start_from_menu(image, rect)
        elif self.previous == 'PAUSE':
            self.play = True

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.play:
                if not self.settings_module.button_system.locked:
                    if event.key == pg.K_ESCAPE:
                        self.next = 'MENU'
                        self.persist['last_image'] = (self.image.copy(),
                                                      self.rect.copy())
                        self.done = True
                    elif event.key == pg.K_UP or event.key == pg.K_w:
                        self.settings_module.button_system.next_button('up')
                        self.update_image()
                    elif event.key == pg.K_DOWN or event.key == pg.K_s:
                        self.settings_module.button_system.next_button('down')
                        self.update_image()
                    elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        self.settings_module.button_system.press_button()
                    elif event.key == pg.K_a or event.key == pg.K_LEFT:
                        if self.settings_module.volume_bar:
                            self.settings_module.volume_bar.change_volume(-0.1)
                            self.update_image()
                    elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                        if self.settings_module.volume_bar:
                            self.settings_module.volume_bar.change_volume(0.1)
                            self.update_image()
                else:
                    if event.key == pg.K_ESCAPE:
                        self.settings_module.button_system.toggle_lock()
                    else:
                        self.settings_module.change_button(event.key)
                    self.update_image()

    def draw(self, surface):
        if self.previous == 'MENU':
            surface.fill(pg.Color('#CD9D77'))
        surface.blit(self.image, self.rect)
        if self.last_image:
            surface.blit(self.last_image.image, self.last_image.rect)

    def update(self, surface, current_time, dt):
        self.current_time = current_time
        self.animations.update(dt * 1000)
        self.draw(surface)
