
from . import setup
from . import constants as c
from .control import Control
from .states import main_menu, play_state, score_state

def main():
    the_app = Control()
    state_dict = {
        c.MENU_SCROLL: main_menu.MenuScroll,
        c.MENU_STILL: main_menu.Menu,
        c.PLAY_NORMAL: play_state.Play,
        c.HIGH_SCORE: score_state.Scored
    }
    the_app.setup_states(state_dict, c.INITIAL_STATE)
    the_app.main()
