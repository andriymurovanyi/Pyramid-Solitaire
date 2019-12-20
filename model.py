import json
import random
import os
import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import background_rc


def decks():
    """
    Load decks from data.json.
    :return: pass
    """
    with open('data.json', 'r') as data:
        f = json.load(data)
    return f['Decks']


class Card(QLabel):
    """
    Represent a playing card.
    """
    def __init__(self, rank, suit, state='Blocked', cards_type='Standart deck'):
        """
        Used to initialize rank and suit vars.

        :param rank: card rank
        :param suit: card suit
        """
        super(Card, self).__init__()
        assert cards_type in decks(), 'Wrong type!'
        assert rank in decks()[cards_type]['ranks'].keys(), 'Wrong rank!'
        assert suit in decks()[cards_type]['suits'], 'Wrong suit!'
        self.__rank = rank
        self.__suit = suit
        self.__state = state
        self.__cards_type = cards_type
        self.__back = None
        self.__face = None
        self.setScaledContents(True)
        self.load_image()

        self.setFixedSize(71, 101)
    #     self.initUI()
    #
    # def initUI(self):
    #     image = self.load_face()
    #     back = self.load_back()
    #     self.setPixmap(image)
    #     self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.b_move = True
            print(event.pos())

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton) and self.b_move:
            self.move(self.mapToParent(event.pos()))

    @property
    def rank(self):
        """
        :return: card rank
        """
        return self.__rank

    @property
    def suit(self):
        """
        :return: card suit
        """
        return self.__suit

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        assert value in ['Active', 'Blocked', 'Unused']
        self.__state = value

    @property
    def value(self):
        return decks()[self.__cards_type]['ranks'][self.__rank]

    def flip(self):
        """
        Flip.

        Change state of card on Active if it's Blocked and conversely.
        """
        if self.__state == 'Blocked':
            self.state = 'Active'
        else:
            self.state = 'Blocked'

    @property
    def check_pixmap(self):
        if self.state == 'Blocked':
            return self.__back
        else:
            return self.__face

    def load_image(self):
        self.__face = QPixmap(':/cards/cards/%s%s.png' % (self.rank, self.suit))
        self.__back = QPixmap(':/img/images/back.png')


    # def __str__(self):
    #     return str(self.__rank) + ':' + str(self.__suit)


class Deck:
    """
    Represent a deck of cards.
    """

    def __init__(self, deck_type='Standart deck'):
        self.__deck_type = deck_type
        self.__deck = []

    def generate_deck(self, n=1):
        """
        Using to generate deck of cards.

        :param n: number of decks
        :return: generated deck
        """
        ranks = decks()[self.__deck_type]['ranks']
        suits = decks()[self.__deck_type]['suits']
        for i in range(n):
            for r in ranks:  # r - ranks.
                for s in suits:  # s - suits.
                    self.__deck.append(Card(r, s))


    def shuffle(self):
        """
        Shuffle cards in Deck.
        """
        random.shuffle(self.__deck)

    @property
    def deck(self):
        """Getter """
        return self.__deck

    def __str__(self):
        return str(self.__deck)


class PyramidBoard:
    """
    State and behavior.
    """
    def __init__(self, deckObj):
        self.__stock = []
        self.__deck = deckObj.deck
        self.__values = 0
        self.__pyramid = []
        self.__stack_of_propped_cards = []
        self.__stack = []

    def pyramid_generator(self):
        """
        Generator.

        Generate a pyramid stack.
        :return:
        """
        size = 7
        self.__pyramid = [[] for i in range(size)]
        for i in range(size):
            for j in range(size - i - 1, size):
                self.__pyramid[i].append(self.__deck.pop())

    @property
    def pyramid(self):
        """
        getter for pyramid.
        :return: pyramid
        """
        return self.__pyramid

    @property
    def stock(self):
        """
        Render picking stack.
        """
        self.__stock = self.__deck
        return self.__stock

    @property
    def stock_of_dropped_cards(self):
        return self.__stack_of_propped_cards

    @property
    def stack(self):
        return self.__stack

    def compare(self, *args):
        """
        Comparing.

        If card or cards values is equal to 13 - drop card from pyramid.
        :param args: list of cards(can exist only one card)
        """
        sum_ = 0
        assert len(args) <= 2, 'Too much cards'
        for card in args:
            if card.state == 'Active':
                sum_ += card.value

        if sum_ == 13:
            for card in args:
                card.state = 'Unused'
                self.drop(card)


    def drop(self, card):
        """
        Dropping.

        Drop cards from pyramid.
        :param card: card to be dropped.
        """
        for i in range(len(self.__pyramid)):
            if card in self.__pyramid[i] and card.state == 'Unused':
                self.__stack_of_propped_cards.append(card)
        if card in self.__stock and card.state == 'Unused':
            self.stock_of_dropped_cards.append(card)
            self.__stock.remove(card)


    def uncover(self):
        """
        Uncovering high-level.

        If two card are dropped, - high level will be open.
        """
        for row in range(len(self.__pyramid) - 1, 0, -1):
            for card in range(1, row + 1):
                if self.__pyramid[row][card].state == 'Unused' \
                        and self.__pyramid[row][card - 1].state == 'Unused'\
                        and self.__pyramid[row - 1][card - 1].state == 'Blocked':
                    self.__pyramid[row - 1][card - 1].state = 'Active'

    @property
    def current(self):
        """
        Flipping through a stock of cards.
        """
        stock_ = self.__stock
        if stock_:
            current = stock_.pop()
            current.state = 'Active'
            self.__stack.append(current)
            if len(stock_) == 0:
                stock_.extend(self.__stack)
                self.__stack.clear()
                current.state = 'Active'
            return current

    def cheat(self):
        """
        Welcome to the Dark Side :D
        """
        for i in self.__pyramid:
            for j in i:
                j.state = 'Unused'




