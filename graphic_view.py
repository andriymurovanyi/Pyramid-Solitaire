# View

from model import Deck
from model import PyramidBoard
import sys
import background_rc
from PyQt5 import uic
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow,  QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QCursor


class PyramidView(QMainWindow):
    def __init__(self, parent=None):
        """
        Initialized all variables.
        """
        super(PyramidView, self).__init__(parent)

        self.card = None  # Card object form for active card.
        self.card2 = None  # Card object form for second card .
        self.last_pos = None  # Last position of current active card.
        self.flag = False  # "lever arm" for moving cards.
        self.current_card = None  # Label form for current active card
        self.ui = uic.loadUi('pyramid.ui')
        # Card size
        self.width = self.ui.label_00.width()  # 71
        self.height = self.ui.label_00.height()  # 101
        # ---------
        self.cards = dict()
        self.coordinates = []  # Labels coordinates on field.
        self.labels = []  # All labels.


        self.initUI()

    def initUI(self):
        """
        Interface.

        Include all interactions with interface.
        :return: None
        """
        # ------------------------------------------------------------------------
        deck = Deck()
        deck.generate_deck()
        deck.shuffle()
        board = PyramidBoard(deck)
        self.__board = board
        board.pyramid_generator()
        self.__pyramid = board.pyramid
        stock = board.stock
        self.__stock = stock
        self.__pyramid_cards = []  # Cards from pyramid in linear form.
        print(self.__stock)
        print(self.__board.stock)

        self.backgroundLeftAddCard = self.ui.stock_previous
        self.foregroundLeftAddCard = self.ui.stock_current  # Card from stock.
        self.rightAddCard = self.ui.stock  # Graphic implementation of stock.
        # -------------------------------------------------------------------------
        for i in self.__pyramid[-1]:
            i.state = 'Active'
        # -----------------------------------------
        new_game = self.ui.actionNew_Game
        new_game.triggered.connect(self.new_game)
        exit_game = self.ui.actionExit
        exit_game.setStatusTip('Quit game!')
        exit_game.triggered.connect(self.quit_game)
        cheat_button = self.ui.smileButton

        cheat_button.clicked.connect(self.cheat)

        # --------------------------------------------------------------------
        self.ui.setWindowTitle('Solitaire')
        self.ui.setWindowIcon(QIcon(':/img/images/app_icon.png'))
        # Adding back side to cards from additional deck
        self.rightAddCard.setPixmap(QPixmap(':/img/images/back.png'))
        self.foregroundLeftAddCard.setVisible(False)
        self.backgroundLeftAddCard.setPixmap(QPixmap(':/img/images/back_start.png'))
        self.rightAddCard.mousePressEvent = self.next_from_stock
        self.foregroundLeftAddCard.mouseMoveEvent = self.mouseMoveEvent
        self.foregroundLeftAddCard.mouseReleaseEvent = self.mouseReleaseEvent

        # --------------------------------------------------------------------
        for i in range(len(self.__pyramid)):
            for j in range(len(self.__pyramid[i])):
                self.cards['label_' + str(i) + str(j)] = self.__pyramid[i][j]
                self.__pyramid_cards.append(self.__pyramid[i][j])

        for i in self.cards.keys():
            label_card = eval('self.ui.' + i)
            label_card.setPixmap(self.cards[i].check_pixmap)
            self.labels.append(label_card)
        for lab_card in self.labels:
            position = lab_card.pos()
            lab_card.mouseMoveEvent = self.mouseMoveEvent
            lab_card.mouseReleaseEvent = self.mouseReleaseEvent
            self.coordinates.append(position)
        self.ui.mousePressEvent = self.mousePressEvent
        print(len(self.coordinates))
        self.ui.show()

    # --- Mouse events. ------------------------------------------------------
    def mousePressEvent(self, event):
        if event.x() in range(self.foregroundLeftAddCard.x(),
                              self.foregroundLeftAddCard.x() + self.width) \
                and event.y() in range(self.foregroundLeftAddCard.y(),
                                       self.foregroundLeftAddCard.y() +
                                       self.height):
            print('Hello!')
            self.card = self.__board.stack[-1]

            self.current_card = self.foregroundLeftAddCard
            self.last_pos = self.current_card.pos()
            if event.button() == Qt.LeftButton:
                self.flag = True
                print('True')
            return

        for i in self.coordinates:
            self.card = self.__pyramid_cards[self.coordinates.index(i)]
            if event.x() in range(i.x(), i.x() + self.width) and \
                    event.y() in range(i.y(), i.y() + self.height):
                if self.card.state == 'Active':

                    self.current_card = \
                        self.labels[self.coordinates.index(i)]
                    self.ui.statusbar.\
                        showMessage('Current card: ' + str(i.x()) + str(i.y()))
                    self.last_pos = self.current_card.pos()  # Coordinates of card.
                    if event.button() == Qt.LeftButton:
                        self.flag = True
                    break

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton) and \
                self.flag and self.card.state == 'Active':
            QApplication.setOverrideCursor(Qt.ClosedHandCursor)
            center_point = QPoint(self.current_card.width() // 2,
                                  self.current_card.height() // 2)
            self.current_card.move(self.current_card.mapToParent(event.pos()
                                                                 - center_point))
            self.current_card.raise_()

    def mouseReleaseEvent(self, event):
        QApplication.setOverrideCursor(Qt.OpenHandCursor)
        current_coords = self.current_card.pos()
        current_x = current_coords.x()
        current_y = current_coords.y()
        if self.card.state == 'Active':
            if self.card.value == 13:
                print('hi')
                self.__board.compare(self.card)
                self.uncover()

            for i in self.coordinates:
                if self.__pyramid_cards[self.coordinates.index(i)].state\
                        == 'Active':
                    if current_x in range(i.x() - self.width // 2,
                                          i.x() + self.width // 2) and \
                            current_y in range(i.y() - self.height // 2,
                                               i.y() + self.height):
                        print('hi')
                        self.card2 = \
                            self.__pyramid_cards[self.coordinates.index(i)]
                        self.__board.compare(self.card, self.card2)
            self.uncover()

        self.current_card.move(self.last_pos)

    def no_event(self):
        pass

    # --- Slots.-----------------------------------------------------------------------
    def next_from_stock(self, *args):
        """
        Flipping stock.

        Take a next card from stock
        :return: None
        """
        self.foregroundLeftAddCard.setVisible(True)
        add_card = self.__board.current

        self.foregroundLeftAddCard.setPixmap(add_card.check_pixmap)
        self.backgroundLeftAddCard.setPixmap(QPixmap(':/img/images/back_start.png'))
        # if len(self.__board.stack) > 1:
        #     self.backgroundLeftAddCard.\
        #         setPixmap(self.__board.stack[-2].check_pixmap)
        # else:
        #     self.no_event()
        if not self.__board.stack:
            self.rightAddCard.setPixmap(QPixmap(':/img/images/back_start.png'))
            self.foregroundLeftAddCard.setPixmap(QPixmap(':/img/images/back.png'))
        else:
            self.rightAddCard.setPixmap(QPixmap(':/img/images/back.png'))
        # self.foregroundLeftAddCard = self.__board.current
        # if self.foregroundLeftAddCard:
        #     self.foregroundLeftAddCard.setVisible(True)
        #     self.foregroundLeftAddCard.setPixmap(QPixmap(self.foregroundLeftAddCard.check_pixmap))
        # else:
        #     self.foregroundLeftAddCard.setVisible(False)
        #
        # self.backgroundLeftAddCard = self.__board.stock[-2]
        # if self.backgroundLeftAddCard:
        #     self.backgroundLeftAddCard.setVisible(True)
        #     self.backgroundLeftAddCard.setPixmap(QPixmap(self.backgroundLeftAddCard.check_pixmap))
        # else:
        #     self.backgroundLeftAddCard.setVisible(False)

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
        for i in self.cards.keys():
            label_card = eval('self.ui.' + i)
            label_card.setPixmap(self.cards[i].check_pixmap)

        for card in self.__pyramid_cards:
            if card.state == 'Unused':
                self.labels[self.__pyramid_cards.index(card)].setVisible(False)

        if self.card.state == 'Unused':
            self.current_card.setVisible(False)


        if self.__pyramid[0][0].state == 'Unused':
            self.win_message()

    def new_game(self):
        """
        New game.

        Used to start new game with new cards.
        :return: None
        """
        for c in self.labels:
            c.setVisible(True)
        self.initUI()

    def quit_game(self):
        """
        Exit.

        Used to quit the game
        :return: None
        """
        reply = QMessageBox.question(self, 'Quit message', 'Are you sure you '
                                                           'want to exit?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ui.close()

    def win_message(self):
        reply = QMessageBox.information(self, 'Game over', 'Oh God, FINALLY!',
                                        QMessageBox.Ok, QMessageBox.Ok)

    def cheat(self):
        for i in self.__pyramid:
            for card in i:
                card.state = 'Unused'
        self.uncover()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    PyramidView()
    sys.exit(app.exec_())
