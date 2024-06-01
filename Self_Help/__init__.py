
from otree.api import *
c = cu

doc = '这是中文版本的私力救济行为实验。'
class C(BaseConstants):
    NAME_IN_URL = 'Self_Help'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    Plaintiff_Choice_1 = models.IntegerField(choices=[[0, '起诉'], [1, '自行维权'], [2, '和解']], initial=99, label='在这一阶段，您作为被侵权者的决策为：')
    Defendant_Choice_2 = models.IntegerField(choices=[[0, '对抗'], [1, '妥协']], initial=99, label='在这一阶段，您作为侵权者的决策为：')
    Defendant_Choice_3 = models.IntegerField(choices=[[0, '不和解'], [1, '和解']], initial=99, label='在这一阶段，您作为侵权者的决策为：')
    Defendant_Choice_1 = models.IntegerField(choices=[[0, '投入大量成本'], [1, '投入少量成本']], initial=99, label='在这一阶段，您作为侵权者的决策为：')
    Plaintiff_Choice_2 = models.IntegerField(choices=[[0, '投入大量成本'], [1, '投入少量成本']], initial=99, label='在这一阶段，您作为被侵权者的决策为：')
def set_payoff(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.Plaintiff_Choice_1 == 0:
        if group.Plaintiff_Choice_2 == 0 and group.Defendant_Choice_1 == 0:
            p1.payoff = 200
            p2.payoff = 200
        elif group.Plaintiff_Choice_2 == 1 and group.Defendant_Choice_1 == 1:
            p1.payoff = 400
            p2.payoff = 400
        elif group.Plaintiff_Choice_2 == 0 and group.Defendant_Choice_1 == 1:
            p1.payoff = 1000
            p2.payoff = -400
        else:
            p1.payoff = -400
            p2.payoff = 1000
    elif group.Plaintiff_Choice_1 == 1:
        if group.Defendant_Choice_2 == 0:
            p1.payoff = -450
            p2.payoff = 200
        else:
            p1.payoff = 550
            p2.payoff = 400
    else:
        if group.Defendant_Choice_3 == 0:
            p1.payoff = 0
            p2.payoff = 1000
        else:
            p1.payoff = 800
            p2.payoff = 200
class Player(BasePlayer):
    Sex = models.IntegerField(choices=[[0, '女'], [1, '男'], [99, '其他']], label='您的性别为：')
    Age = models.IntegerField(label='您的年龄为：', max=130, min=0)
    Education = models.IntegerField(choices=[[0, '初中及以下'], [1, '高中'], [2, '本科及同等学历'], [3, '硕士及同等学历'], [4, '博士及同等学历'], [99, '其他']], label='您的受教育程度为：')
    Law_Related = models.IntegerField(choices=[[0, '无关'], [1, '有关']], label='您的教育或工作经历是否同法学或法律事务有关？')
    Marriage = models.IntegerField(choices=[[0, '未婚'], [1, '已婚'], [2, '离异'], [3, '丧偶'], [99, '其他']], label='您的婚姻状况为：')
    Income = models.IntegerField(choices=[[0, '2000元以下'], [1, '2000元到4000元'], [2, '4000元到6000元'], [3, '6000元到8000元'], [4, '8000元到10000元'], [5, '10000元到12000元'], [6, '12000元到14000元'], [7, '14000元到16000元'], [8, '16000元到18000元'], [9, '18000元到20000元'], [10, '20000元以上']], label='您的月平均收入为（以人民币计）：')
    Email = models.StringField(blank=True, initial='None', label='您的电子邮箱为（非必填项）：')
    Nation = models.IntegerField(choices=[[0, '亚洲'], [1, '欧洲'], [2, '北美洲'], [3, '南美洲'], [4, '非洲'], [5, '大洋洲'], [99, '其他']], label='您的经常居住地位于：')
class Welcome(Page):
    form_model = 'player'
    form_fields = ['Sex', 'Age', 'Nation', 'Education', 'Law_Related', 'Marriage', 'Income', 'Email']
    timeout_seconds = 180
class Description(Page):
    form_model = 'player'
    timeout_seconds = 300
class Plaintiff(Page):
    form_model = 'group'
    form_fields = ['Plaintiff_Choice_1']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1
class WaitForPlaintiff(WaitPage):
    title_text = '您被分配到的角色是：侵权者！'
    body_text = '您被分配到的角色是：<b>侵权者</b>！目前被侵权者正在决策，请您稍作等待。如您在本页面等待时间超过5分钟，您可先行退出，实验团队将尝试通过邮件（如预留）向您汇报实验结果（如成功完成）。'
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2
class Defendant_1(Page):
    form_model = 'group'
    form_fields = ['Defendant_Choice_1']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2 and group.Plaintiff_Choice_1 == 0
class Plaintiff_1(Page):
    form_model = 'group'
    form_fields = ['Plaintiff_Choice_2']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1 and group.Plaintiff_Choice_1 == 0
class Defendant_2(Page):
    form_model = 'group'
    form_fields = ['Defendant_Choice_2']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2 and group.Plaintiff_Choice_1 == 1
class Defendant_3(Page):
    form_model = 'group'
    form_fields = ['Defendant_Choice_3']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2 and group.Plaintiff_Choice_1 == 2
class WaitForAll(WaitPage):
    after_all_players_arrive = set_payoff
    title_text = '等待所有参与者完成实验'
    body_text = '实验已经接近尾声，请您稍作等待。如您在本页面等待时间超过5分钟，您可先行退出，实验团队将尝试通过邮件（如预留）向您汇报实验结果（如成功完成）。'
class Result(Page):
    form_model = 'player'
page_sequence = [Welcome, Description, Plaintiff, WaitForPlaintiff, Defendant_1, Plaintiff_1, Defendant_2, Defendant_3, WaitForAll, Result]