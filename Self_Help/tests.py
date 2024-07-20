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
            Email="xyz",
        )
        yield Description
        if self.player.id_in_group == 1:
            yield Plaintiff, dict(Plaintiff_Choice_1=0)
        if self.player.id_in_group == 2 and self.group.Plaintiff_Choice_1 == 0:
            yield Defendant_1, dict(Defendant_Choice_1=0)
        if self.player.id_in_group == 1 and self.group.Plaintiff_Choice_1 == 0:
            yield Plaintiff_1, dict(Plaintiff_Choice_2=0)
        if self.player.id_in_group == 2 and self.group.Plaintiff_Choice_1 == 1:
            yield Defendant_2, dict(Defendant_Choice_2=0)
        if self.player.id_in_group == 2 and self.group.Plaintiff_Choice_1 == 2:
            yield Defendant_3, dict(Defendant_Choice_3=0)
        yield Result