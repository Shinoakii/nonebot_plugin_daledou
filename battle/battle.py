from .player import Player
from round import Round
from util import TIMEOUTMSG


class Battle:

    def __init__(self, player1, player2) -> None:
        self.p1 = Player(player1)
        self.p2 = Player(player2)
        self.battle_msg = []

    def battle_pvp(self):
        # battle-start
        self.battle_msg.append('战斗开始')
        Turn = 1
        time_out = False
        while self.p1.is_alive() and self.p2.is_alive():
            round = Round(Turn, self.p1, self.p2, self.battle_msg)
            self.p1, self.p2, self.battle_msg = round.get_next_round()
            if Turn >= 25:
                time_out = True
                break
            Turn += 1
        if time_out:
            winner = self.p1 if self.p1.hp > self.p2.hp else self.p2  # 血一样多p2胜利，因为p1先手
            self.battle_msg.append(TIMEOUTMSG.format(Turn, winner.nick_name))
            return winner
        if self.p1.is_alive():
            winner = self.p1
        else:
            winner = self.p2
        return winner
