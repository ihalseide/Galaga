
from . import setup
from . import constants as c
from .control import Control
from .states import main_menu, play_state, score_state

def main():
    the_app = Control()
    state_dict = {
        c.MENU_STATE: main_menu.Menu(),
        c.PLAY_STATE: play_state.Play(),
        c.SCORED_STATE: score_state.Scored()
    }
    the_app.setup_states(state_dict, c.INITIAL_STATE)
    the_app.main()
