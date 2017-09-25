"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""

import pygame as pg
from . import prepare, tools
from .states import game, highscore, pause, menu, restartmenu, controls, sound, settings


def main():
    """
    Add states to control here.
    """
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {'GAME': game.Game(),
                  'HIGHSCORE': highscore.HighScore(),
                  'MENU': menu.Menu(),
                  'PAUSE': pause.Pause(),
                  'RESTARTMENU': restartmenu.RestartMenu(),
                  'CONTROLS': controls.Controls(),
                  'SOUND': sound.Sound(),
                  'SETTINGS': settings.Settings(),
                  }
    run_it.setup_states(state_dict, 'MENU')
    pg.mixer.music.play(-1)
    run_it.main()
