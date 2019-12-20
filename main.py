import model as m
import view as v
from os import system


def game():
    deck = m.Deck()
    deck.generate_deck()
    deck.shuffle()
    board = m.PyramidBoard(deck)
    board.pyramid_generator()
    pyramid = board.pyramid
    stock = board.stock
    view = v.BoardView(board)
    current_from_stock = board.current()
    # main game loop.
    while True:
        for i in stock:
            i.flip()
        print(view.instruction())

        print(view.render_extra_card(current_from_stock))
        print(view.render_pyramid())
        if pyramid[0][0].state == 'Unused':
            print('Game over!\n'
                  'Thank\'s God, finally! :D ')
            break
        cards = []
        command = input('Enter command:\n'
                        '>>> ')
        if command == 't':
            try:
                c1 = input('Your card:\n'
                           '>>> ')
                if c1 == 'e':
                    card1 = current_from_stock
                    cards.append(card1)
                else:
                    c1 = c1.split(', ')
                    row1 = int(c1[0]) * -1
                    column1 = int(c1[1]) * -1
                    card1 = pyramid[row1][column1]
                    cards.append(card1)
                more = input('One more card?[y/n]\n'
                             '>>>')
                if more == 'y':
                    c2 = input('You\'re card:\n'
                               '>>> ')
                    if c2 == 'e':
                        card2 = current_from_stock
                        cards.append(card2)
                    else:
                        c2 = c2.split(', ')
                        row2 = int(c2[0]) * -1
                        column2 = int(c2[1]) * -1
                        card2 = pyramid[row2][column2]
                        cards.append(card2)
                    board.compare(cards)
                elif more == 'y':
                    board.compare(cards)
            except IndexError:
                print('Card in incorrect format(see help)...!')
            except ValueError:
                print('')
            current_from_stock = board.current()
            board.uncover()
            system('cls')
        elif command == 's' or command == 'start':
            game()
        elif command == 'h' or command == 'help':
            print(view.instruction())
            continue
        elif command == 'c' or command == 'change':
            current_from_stock = board.current()
            system('cls')
            continue
        elif command == 'win':
            board.cheat()
            system('cls')
            continue
        elif command == 'q' or command == 'quit':
            exit()
        else:
            print('Unknown command')
            system('cls')
            continue

game()
