
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
    Yuangao_Weiquan = models.IntegerField(choices=[[0, '尝试和解'], [1, '放弃维权']], initial=99, label='在这一阶段，您的决策为：')
    Beigao_Hejie = models.IntegerField(choices=[[0, '同意和解'], [1, '不同意和解']], initial=99, label='在这一阶段，您的决策为：')
    Yuangao_Erxuanyi = models.IntegerField(choices=[[0, '自行维权'], [1, '诉讼']], initial=99, label='在这一阶段，您的决策为：')
    Beigao_Zixingweiquan = models.IntegerField(choices=[[0, '妥协'], [1, '对抗']], initial=99, label='在这一阶段，您的决策为：')
    Yuangao_Susong = models.IntegerField(choices=[[0, '投入少量成本'], [1, '投入大量成本']], initial=99, label='在这一阶段，您的决策为：')
    Beigao_Susong = models.IntegerField(choices=[[0, '投入少量成本'], [1, '投入大量成本']], initial=99, label='在这一阶段，您的决策为：')
def set_payoff(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.Yuangao_Weiquan == 1:
        p1.payoff = 0
        p2.payoff = 1000
    if group.Yuangao_Weiquan == 0:
        if group.Beigao_Hejie == 0:
            p1.payoff = 800
            p2.payoff = 200
        if group.Beigao_Hejie == 1:
            if group.Yuangao_Erxuanyi == 0:
                if group.Beigao_Zixingweiquan == 0:
                    p1.payoff = 550
                    p2.payoff = 400
                if group.Beigao_Zixingweiquan == 1:
                    p1.payoff = -450
                    p2.payoff = 200
            if group.Yuangao_Erxuanyi == 1:
                if group.Yuangao_Susong == 0 and group.Beigao_Susong == 0:
                    p1.payoff = 400
                    p2.payoff = 400
                if group.Yuangao_Susong == 1 and group.Beigao_Susong == 0:
                    p1.payoff = 1000
                    p2.payoff = -400
                if group.Yuangao_Susong == 0 and group.Beigao_Susong == 1:
                    p1.payoff = -400
                    p2.payoff = 1000
                if group.Yuangao_Susong == 1 and group.Beigao_Susong == 1:
                    p1.payoff = 200
                    p2.payoff = 200
class Player(BasePlayer):
    Sex = models.IntegerField(choices=[[0, '女'], [1, '男'], [99, '其他']], label='您的性别为：')
    Age = models.IntegerField(label='您的年龄为：', max=130, min=0)
    Education = models.IntegerField(choices=[[0, '初中及以下'], [1, '高中'], [2, '本科'], [3, '硕士研究生'], [4, '博士研究生及以上'], [99, '其他']], label='您的受教育程度为：')
    Law_Related = models.IntegerField(choices=[[0, '无关'], [1, '有关']], label='您的教育或工作经历是否同法学或法律事务有关？')
    Marriage = models.IntegerField(choices=[[0, '未婚'], [1, '已婚'], [2, '离异'], [3, '丧偶'], [99, '其他']], label='您的婚姻状况为：')
    Income = models.IntegerField(choices=[[0, '2000元以下'], [1, '2000元到4000元'], [2, '4000元到6000元'], [3, '6000元到8000元'], [4, '8000元到10000元'], [5, '10000元到12000元'], [6, '12000元到14000元'], [7, '14000元到16000元'], [8, '16000元到18000元'], [9, '18000元到20000元'], [10, '20000元以上']], label='您的月平均收入为：')
    Comment = models.StringField(blank=True, initial='非必填项，但期待您的反馈！', label='您对目前的结果满意吗？您有什么感受或心得吗？欢迎畅所欲言！')
class Huanying(Page):
    form_model = 'player'
    form_fields = ['Sex', 'Age', 'Education', 'Law_Related', 'Marriage', 'Income']
    timeout_seconds = 180
class Dengdai_1(WaitPage):
    title_text = '等待其他参与者进入房间'
    body_text = '本实验由包括您在内的两名参与者共同实时完成。一旦有其他参与者进入房间，实验将自动开始，请您稍作等待。'
class Shiyan_Miaoshu(Page):
    form_model = 'player'
    timeout_seconds = 300
class Yuangao_Weiquan(Page):
    form_model = 'group'
    form_fields = ['Yuangao_Weiquan']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1
class Dengdai_2(WaitPage):
    title_text = '您被分配到的角色是：侵权者'
    body_text = '您被分配到的角色是：侵权者。<br>目前被侵权者正在决策，请您稍作等待。'
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2
class Beigao_Hejie(Page):
    form_model = 'group'
    form_fields = ['Beigao_Hejie']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2 and group.Yuangao_Weiquan == 0
class Dengdai_3(WaitPage):
    title_text = '侵权者正在决策'
    body_text = '目前侵权者正在决策，请您稍作等待。'
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1
class Yuangao_Erxuanyi(Page):
    form_model = 'group'
    form_fields = ['Yuangao_Erxuanyi']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1 and group.Beigao_Hejie == 1
class Dengdai_4(WaitPage):
    title_text = '被侵权者正在决策'
    body_text = '目前被侵权者正在决策，请您稍作等待。'
    @staticmethod
    def is_displayed(player: Player):
        return True
class Beigao_Zixingweiquan(Page):
    form_model = 'group'
    form_fields = ['Beigao_Zixingweiquan']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2 and group.Yuangao_Erxuanyi == 0
class Beigao_Susong(Page):
    form_model = 'group'
    form_fields = ['Beigao_Susong']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 2 and group.Yuangao_Erxuanyi == 1
class Yuangao_Susong(Page):
    form_model = 'group'
    form_fields = ['Yuangao_Susong']
    timeout_seconds = 180
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return player.id_in_group == 1 and group.Yuangao_Erxuanyi == 1
class WaitForAll(WaitPage):
    after_all_players_arrive = set_payoff
    title_text = '等待所有参与者完成实验'
    body_text = '实验已经接近尾声，请您稍作等待。待所有参与者完成决策后，系统将自动计算博弈结果。'
class Jeiguo(Page):
    form_model = 'player'
    form_fields = ['Comment']
class Zaijian(Page):
    form_model = 'player'
page_sequence = [Huanying, Dengdai_1, Shiyan_Miaoshu, Yuangao_Weiquan, Dengdai_2, Beigao_Hejie, Dengdai_3, Yuangao_Erxuanyi, Dengdai_4, Beigao_Zixingweiquan, Beigao_Susong, Yuangao_Susong, WaitForAll, Jeiguo, Zaijian]