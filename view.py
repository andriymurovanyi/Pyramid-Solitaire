# View

instruction = """\
============================================================+  
Welcome to Pyramid Solitaire!                              ||  
Rules:                                                     || 
You should remove pairs of                                 || 
cards that equal to 13.                                    ||  
Values:                                                    ||
K - 13                                                     ||
Q - 12                                                     ||
J - 11                                                     ||
A - 1                                                      ||
Other cards: name = value (2 - 2, ..., etc)                ||
List of commands:                                          ||
1) New Game - start or s                                   ||
2) Help menu - help or h                                   ||
3) Take card - enter 't' key and                           ||
input it's row and column or 'e' to take form stock        || 
!!!Indexing goes from right to left!!!                     ||
3) Change extra card - change or c                         ||
4) Quit - quit or q                                        ||
Good luck, have fun :D                                     ||
============================================================+
"""


class BoardView:
    def __init__(self, board):
        self.__board = board
        self.__pyramid = self.__board.pyramid
        self.__stock = self.__board.stock

    def render_pyramid(self):
        """
        Render pyramid.

        Printing pyramid in human-readable form
        """
        result = ''
        for i in self.__pyramid:
            for j in i:
                if j.state == 'Blocked':
                    result += ' ' + '[#]'
                elif j.state == 'Unused':
                    result += ' ' + ' - '
                else:
                    result += ' ' + str(j)
            result += '\n'
        result = result.split('\n')
        for i in result:
            print(i.center(50))
        return '<>'

    @staticmethod
    def render_extra_card(card=None):
        """
        Render extra_card.

        Printing extra_card in human-readable form
        """
        return '===========\n' +\
               'Stock-card: \n' + str(card) + '\n' \
               '==========='

    @staticmethod
    def instruction():
        return instruction















