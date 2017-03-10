'''
A Test for simulation of UNO play

Date: 2017-3-8 22:24(CST)
Author: Morris Dong
'''
# pylint: disable=R0903
# pylint: disable=R0912
# pylint: disable=R0915
from enum import Enum
import random
import sqlite3
import uuid

db_conn = sqlite3.connect('uno.db')
db_conn.close()
game_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org'))


class CardType(Enum):
    '''
    Enum for card type. Include Deafault, Normal, Skip, Reverse, Draw Two, Wild and Wild Draw Four
    '''
    DEFAULT = -1
    NORMAL = 1
    SKIP = 2
    REVERSE = 3
    DRAW_TWO = 4
    WILD = 5
    WILD_DRAW_FOUR = 6


class CardColor(Enum):
    '''
    Enum for card color. Include Deafault, Green, Blue, Yellow and Red
    '''
    DEFAULT = -1
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    RED = 4


class Card:
    '''
    Card class. Include type, color and value info..
    '''
    def __init__(self, t=CardType.DEFAULT, c=CardColor.DEFAULT, v=-1):
        self.type = t
        self.color = c
        self.value = v

    def __str__(self):
        if self.type == CardType.WILD or self.type == CardType.WILD_DRAW_FOUR:
            return self.type.name
        else:
            return self.color.name + ' ' +\
                (str(self.value) if self.type ==
                 CardType.NORMAL else self.type.name)


class Player:
    '''
    Player class. Include name and cards
    '''
    def __init__(self, i=-1):
        self.name = i
        self.hold_list = []
    def get_grade(self):
        '''
        Func. to get the grade of the cards of this player holds
        '''
        result = 0
        for card in self.hold_list:
            result += card.value
        return result

    def __str__(self):
        return 'player' + str(self.name)


class CardManager:
    '''
    Card managemention class.
    With features of Draw Card and automaticly re-shuffle the wasted card.
    '''
    def __init__(self):
        self.card_list = []
        self.wasted_card_list = []
        self.card_list.append(Card(CardType.NORMAL, CardColor.GREEN, 0))
        self.card_list.append(Card(CardType.NORMAL, CardColor.RED, 0))
        self.card_list.append(Card(CardType.NORMAL, CardColor.BLUE, 0))
        self.card_list.append(Card(CardType.NORMAL, CardColor.YELLOW, 0))
        for i in range(9):
            self.card_list.append(Card(CardType.NORMAL, CardColor.GREEN, i))
            self.card_list.append(Card(CardType.NORMAL, CardColor.GREEN, i))
            self.card_list.append(Card(CardType.NORMAL, CardColor.RED, i))
            self.card_list.append(Card(CardType.NORMAL, CardColor.RED, i))
            self.card_list.append(Card(CardType.NORMAL, CardColor.BLUE, i))
            self.card_list.append(Card(CardType.NORMAL, CardColor.BLUE, i))
            self.card_list.append(Card(CardType.NORMAL, CardColor.YELLOW, i))
            self.card_list.append(Card(CardType.NORMAL, CardColor.YELLOW, i))
        self.card_list.append(Card(CardType.SKIP, CardColor.GREEN, 20))
        self.card_list.append(Card(CardType.SKIP, CardColor.GREEN, 20))
        self.card_list.append(Card(CardType.SKIP, CardColor.RED, 20))
        self.card_list.append(Card(CardType.SKIP, CardColor.RED, 20))
        self.card_list.append(Card(CardType.SKIP, CardColor.BLUE, 20))
        self.card_list.append(Card(CardType.SKIP, CardColor.BLUE, 20))
        self.card_list.append(Card(CardType.SKIP, CardColor.YELLOW, 20))
        self.card_list.append(Card(CardType.SKIP, CardColor.YELLOW, 20))
        self.card_list.append(Card(CardType.REVERSE, CardColor.GREEN, 20))
        self.card_list.append(Card(CardType.REVERSE, CardColor.GREEN, 20))
        self.card_list.append(Card(CardType.REVERSE, CardColor.RED, 20))
        self.card_list.append(Card(CardType.REVERSE, CardColor.RED, 20))
        self.card_list.append(Card(CardType.REVERSE, CardColor.BLUE, 20))
        self.card_list.append(Card(CardType.REVERSE, CardColor.BLUE, 20))
        self.card_list.append(Card(CardType.REVERSE, CardColor.YELLOW, 20))
        self.card_list.append(Card(CardType.REVERSE, CardColor.YELLOW, 20))
        self.card_list.append(Card(CardType.DRAW_TWO, CardColor.GREEN, 20))
        self.card_list.append(Card(CardType.DRAW_TWO, CardColor.GREEN, 20))
        self.card_list.append(Card(CardType.DRAW_TWO, CardColor.RED, 20))
        self.card_list.append(Card(CardType.DRAW_TWO, CardColor.RED, 20))
        self.card_list.append(Card(CardType.DRAW_TWO, CardColor.BLUE, 20))
        self.card_list.append(Card(CardType.DRAW_TWO, CardColor.BLUE, 20))
        self.card_list.append(Card(CardType.DRAW_TWO, CardColor.YELLOW, 20))
        self.card_list.append(Card(CardType.DRAW_TWO, CardColor.YELLOW, 20))
        self.card_list.append(Card(CardType.WILD, CardColor.DEFAULT, 50))
        self.card_list.append(Card(CardType.WILD, CardColor.DEFAULT, 50))
        self.card_list.append(Card(CardType.WILD, CardColor.DEFAULT, 50))
        self.card_list.append(Card(CardType.WILD, CardColor.DEFAULT, 50))
        self.card_list.append(
            Card(CardType.WILD_DRAW_FOUR, CardColor.DEFAULT, 50))
        self.card_list.append(
            Card(CardType.WILD_DRAW_FOUR, CardColor.DEFAULT, 50))
        self.card_list.append(
            Card(CardType.WILD_DRAW_FOUR, CardColor.DEFAULT, 50))
        self.card_list.append(
            Card(CardType.WILD_DRAW_FOUR, CardColor.DEFAULT, 50))
        random.shuffle(self.card_list)

    def pop_card(self):
        '''
        Func. to pop out a new card.
        '''
        if len(self.card_list) == 0:
            self.card_list = self.wasted_card_list
            random.shuffle(self.card_list)
            self.wasted_card_list = []
            self.__record_shuffle()
        return self.card_list.pop()

    def waste_card(self, card):
        '''
        Func. to collect the wasted card.
        '''
        self.wasted_card_list.append(card)

    def __record_shuffle(self):
        '''
        record the card bank status after shuffle
        '''
        cardlist_str = ''
        for card in self.card_list:
            cardlist_str += str(card) + ' '
        db_conn.execute(
            '''
            INSERT INTO CARDRECORD(GAMENAME, CARDLIST)
            VALUES(?,?)
            ''', (game_id, cardlist_str)
        )
        db_conn.commit()


def report_action(player, action):
    '''
    report an anction and record into db
    '''
    actor_name = ''
    card_str = ''
    if player is None:
        actor_name = 'GOD'
        card_str = 'N/A'
    else:
        actor_name = str(player)
        for card in player.hold_list:
            card_str += str(card) + ' '
    print(actor_name + ': ' + action)
    db_conn.execute(
        '''
        INSERT INTO GAMERECORD(GameName, PlayerName, Action, HoldCards)
        VALUES (?, ?, ?, ?)
        ''', (game_id, actor_name, action, card_str)
    )
    db_conn.commit()

class GameManager:
    '''
    Game managemention class.
    With the features of player mgmt., banker setting and game ctrling.
    '''
    clockwish = 1
    player_list = []
    banker_id = 0
    named_color = CardColor.DEFAULT
    card_mana = CardManager()

    def __init__(self, count):
        for i in range(count):
            self.player_list.append(Player(i,))

    def __set_banker(self):
        '''
        Func to set banker
        '''
        self.banker_id = -1
        for i in range(len(self.player_list)):
            tmp = self.card_mana.pop_card()
            if tmp.value > self.banker_id:
                self.banker_id = i
            self.card_mana.waste_card(tmp)

    def play(self):
        '''
        The main func. to play a game.
        '''
        self.__set_banker()
        player_index = self.banker_id
        updated = False
        print('GOD: Banker is player' + str(player_index))
        for tmp in range(7):  # pylint: disable=W0612
            for i in range(self.banker_id, len(self.player_list)):
                self.player_list[i].hold_list.append(self.card_mana.pop_card())
            for i in range(self.banker_id):
                self.player_list[i].hold_list.append(self.card_mana.pop_card())
        tmp_card = self.card_mana.pop_card()
        while tmp_card.type == CardType.WILD_DRAW_FOUR:
            report_action(None, 'WILD_DRAW_FOUR')
            self.card_mana.waste_card(tmp_card)
            tmp_card = self.card_mana.pop_card()
        if tmp_card.type == CardType.WILD:
            report_action(None, 'WILD')
            self.named_color = CardColor(random.randrange(1, 5))
            report_action(self.player_list[player_index], 'WILD_DRAW_FOUR')
            player_index += 1
        else:
            if tmp_card.type == CardType.REVERSE:
                self.clockwish *= -1
            elif tmp_card.type == CardType.SKIP:
                player_index += self.clockwish
            report_action(None, str(tmp_card))
        while True:
            player_index %= len(self.player_list)
            now_player = self.player_list[player_index]
            valid_id = []

            if tmp_card.type == CardType.WILD or tmp_card.type == CardType.WILD_DRAW_FOUR:
                for i in range(len(now_player.hold_list)):
                    if now_player.hold_list[i].color == self.named_color \
                            or now_player.hold_list[i].type == CardType.WILD:
                        valid_id.append(i)
            else:
                for i in range(len(now_player.hold_list)):
                    hlc = now_player.hold_list[i]
                    if hlc.type == CardType.WILD or hlc.color == tmp_card.color \
                            or (hlc.value < 20 and hlc.value == tmp_card.value):
                        valid_id.append(i)
            if len(valid_id) == 0:
                for i in range(len(now_player.hold_list)):
                    if now_player.hold_list[i].type == CardType.WILD_DRAW_FOUR:
                        valid_id.append(i)

            if len(valid_id) > 0:
                i = random.choice(valid_id)
                self.card_mana.waste_card(tmp_card)
                tmp_card = now_player.hold_list.pop(i)
                updated = True
            else:
                report_action(now_player, 'Draw')
                new_card = self.card_mana.pop_card()
                if tmp_card.type == CardType.WILD or tmp_card.type == CardType.WILD_DRAW_FOUR:
                    if new_card.color == self.named_color \
                            or new_card.type == CardType.WILD:
                        self.card_mana.waste_card(tmp_card)
                        tmp_card = new_card
                        updated = True
                    else:
                        now_player.hold_list.append(new_card)
                        report_action(now_player, 'Pass')
                else:
                    if new_card.type == CardType.WILD \
                    or new_card.color == tmp_card.color \
                    or (new_card.value < 20 and new_card.value == tmp_card.value):
                        self.card_mana.waste_card(tmp_card)
                        tmp_card = new_card
                        updated = True
                    else:
                        now_player.hold_list.append(new_card)
                        report_action(now_player, 'Pass')

            if updated is True:
                if len(now_player.hold_list) == 1:
                    report_action(now_player, 'UNO!')
                if len(now_player.hold_list) == 0:
                    break
                report_action(now_player, str(tmp_card))
                if tmp_card.type == CardType.WILD or tmp_card.type == CardType.WILD_DRAW_FOUR:
                    self.named_color = CardColor(random.randrange(1, 5))
                    report_action(now_player, 'Set Color into ' +
                                  self.named_color.name)
                    if tmp_card.type == CardType.WILD_DRAW_FOUR:
                        player_index = (
                            player_index + self.clockwish) % len(self.player_list)
                        now_player = self.player_list[player_index]
                        now_player.hold_list.append(self.card_mana.pop_card())
                        now_player.hold_list.append(self.card_mana.pop_card())
                        now_player.hold_list.append(self.card_mana.pop_card())
                        now_player.hold_list.append(self.card_mana.pop_card())

                else:
                    if tmp_card.type == CardType.DRAW_TWO:
                        player_index = (
                            player_index + self.clockwish) % len(self.player_list)
                        now_player = self.player_list[player_index]
                        now_player.hold_list.append(self.card_mana.pop_card())
                        now_player.hold_list.append(self.card_mana.pop_card())
                        report_action(now_player, 'Have drew two')
                    else:
                        if tmp_card.type == CardType.REVERSE:
                            self.clockwish *= -1
                        elif tmp_card.type == CardType.SKIP:
                            player_index += self.clockwish
                updated = False
            player_index += self.clockwish
        self.__sum_up()

    def __sum_up(self):
        self.player_list.sort(key=lambda p: p.get_grade())

        report_action(None, "Winner: palyer" + str(self.player_list[0].name))
        for i in range(1, len(self.player_list)):
            report_action(None, 'Next: player' +
                          str(self.player_list[i].name) + '\t' + \
                          str(self.player_list[i].get_grade()))


if __name__ == '__main__':
    db_conn = sqlite3.connect('uno.db')
    db_conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS "CardRecord" (
                "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                "GameName"  TEXT NOT NULL,
            "CardList"  TEXT NOT NULL
        )
        '''
    )
    db_conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS "GameRecord" (
                "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                "GameId"  TEXT NOT NULL,
                "PlayerName"  TEXT NOT NULL,
                "Action"  TEXT NOT NULL,
                "HoldCards"  TEXT NOT NULL
        )
        '''
    )
    GAME = GameManager(4)
    GAME.play()
    db_conn.commit()
    db_conn.close()
