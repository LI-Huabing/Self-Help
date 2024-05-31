import Self_Help as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        yield Welcome, dict(
            Sex=0,
            Age=130,
            Nation="xyz",
            Education=0,
            Law_Related=0,
            Marriage=0,
            Income=0,
        )