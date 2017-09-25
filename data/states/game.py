import pygame as pg

from .. import tools, prepare
from ..components.animations import Animation
from ..components.well import Well
from ..components.gui import GUI
from ..components.task import Task


class Game(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.pre_dump_time = 2000
        self.post_dump_time = 5000
        self.tasks = pg.sprite.Group()
        self.animations = pg.sprite.Group()
        self.level = 1
        self.lines = 0
        self.well_location = (112, 35)
        # states = TRANSITION, PLAY, LOST

    def start(self):
        self.state = 'TRANSITION'
        self.change_lines(0)
        self.gui = GUI()
        self.well = Well(self.gui.preview,
                         self.change_lines, self.lose, self.well_location)

        self.left_gates, self.right_gates = self.make_gates()
        self.gates = pg.sprite.Group(self.left_gates, self.right_gates)
        self.left_animation, self.right_animation = self.make_animations()
        self.animations = pg.sprite.Group(self.left_animation,
                                          self.right_animation)
        self.start_animations()

    def make_gates(self):
        left_gates = pg.sprite.Sprite()
        left_gates.image = prepare.GFX['other']['gates_left2']
        left_gates.rect = left_gates.image.get_rect(topleft=(0, 0))

        right_gates = pg.sprite.Sprite()
        right_gates.image = prepare.GFX['other']['gates_right2']
        right_gates.rect = right_gates.image.get_rect(topleft=(300, 0))

        return left_gates, right_gates

    def make_animations(self):
        self.start_time = None
        left_animation = Animation(
            x=-400, y=0, duration=750, round_values=True,
            transition='in_sine')
        left_animation.callback = self.start_play
        right_animation = Animation(
            x=800, y=0, duration=750, round_values=True, transition='in_sine')
        return left_animation, right_animation

    def start_animations(self):
        self.left_animation.start(self.left_gates.rect)
        self.right_animation.start(self.right_gates.rect)

    def restart(self):
        self.gui = GUI()
        self.descend_well()

    def prepare_start(self):
        self.tasks.add(Task(self.start_play, 200))

    def start_play(self):
        self.state = 'PLAY'
        self.well.start(self.current_time)

    def descend_well(self):
        self.well = Well(self.gui.preview,
                         self.change_lines, self.lose,
                         (self.well_location[0], -self.well.rect.height))
        animation = Animation(
            x=self.well_location[0], y=self.well_location[1], duration=2000,
            round_values=True, transition='out_back')
        animation.callback = self.prepare_start
        animation.start(self.well.rect)
        self.animations.add(animation)

    def dump_well(self):
        animation = Animation(
            x=self.well.rect.x, y=600, duration=2000, round_values=True,
            transition='in_sine')
        animation.callback = self.restart_menu
        animation.start(self.well.rect)
        self.animations.add(animation)

    def lose(self):
        self.state = 'LOST'
        self.tasks.add(Task(self.dump_well, 1000))

    def restart_menu(self):
        self.well.state = 'PRE_PLAY'
        self.persist['result'] = self.lines, self.gui.get_time_string()
        self.next = 'RESTARTMENU'
        self.done = True

    def change_level(self):
        self.level += 1
        self.well.usual_move_time -= 50
        self.well.move_time = self.well.usual_move_time
        self.gui.change_level(self.level)

    def change_lines(self, amount):
        if amount == 0:
            self.lines = 0
        else:
            if ((self.lines % 10) + amount) // 10 > 0:
                if self.lines + amount < 50:
                    self.change_level()
            self.lines += amount
            self.gui.change_lines(self.lines)

    def finish_animations(self):
        if self.animations:
            self.animations.empty()
        self.state = 'TRANSITION'
        left_animation = Animation(
            x=0, y=0, duration=750, round_values=True,
            transition='in_sine')
        left_animation.callback = self.finish
        left_animation.start(self.left_gates.rect)
        right_animation = Animation(
            x=300, y=0, duration=750, round_values=True,
            transition='in_sine')
        right_animation.start(self.right_gates.rect)
        self.animations.add(left_animation, right_animation)

    def finish(self):
        self.next = 'MENU'
        self.done = True

    def startup(self, current_time, persistant):
        self.persist = persistant
        if self.previous == 'MENU':
            self.start()
        elif self.previous == 'PAUSE':
            if 'quit' in self.persist:
                del self.persist['quit']
                self.finish_animations()
        elif self.previous == 'RESTARTMENU':
            if 'quit' in self.persist:
                del self.persist['quit']
                self.finish_animations()
            else:
                self.restart()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if self.state == 'PLAY':
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.persist['screen'] = pg.display.get_surface().copy()
                    self.next = 'PAUSE'
                    self.done = True
                # make it easier + toggle soft_drop
                elif event.key == prepare.controls['move_left']:
                    self.well.player_action('left')
                elif event.key == prepare.controls['move_right']:
                    self.well.player_action('right')
                elif event.key == prepare.controls['rotate_counterclockwise']:
                    self.well.player_action('rotate_counterclockwise')
                elif event.key == prepare.controls['rotate_clockwise']:
                    self.well.player_action('rotate_clockwise')
                elif event.key == prepare.controls['soft_drop']:
                    self.well.player_action('start_soft_drop')
                elif event.key == prepare.controls['hard_drop']:
                    self.well.player_action('hard_drop')
            elif event.type == pg.KEYUP:
                if event.key == prepare.controls['soft_drop']:
                    self.well.player_action('stop_soft_drop')

    def draw(self, surface):
        surface.fill(pg.Color('#CD9D77'))
        self.well.draw(surface)
        self.gui.draw(surface)
        self.gates.draw(surface)

    def update(self, surface, current_time, dt):
        self.current_time = current_time
        self.tasks.update(dt * 1000)
        self.animations.update(dt * 1000)
        if self.state == 'PLAY':
            self.well.update(current_time, dt)
            self.gui.update_time(dt * 1000)
        elif self.state == 'LOST':
            self.well.update(current_time, dt)
        self.draw(surface)
