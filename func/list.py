# List contents of current context.
# Different functions are defined for different levels.

from . import request
from colored import attr
from trello.board import Board
from trello.list import List
from trello.card import Card
from clint.textui import indent


def list_boards():
    boards_response = request.get('1/members/me/boards', {'filter': 'open'})
    boards = []

    for board_data in boards_response:
        boards.append(Board(board_data))

    print('Open boards for {}{}{}:'.format(attr(1),
                                           request.get('1/members/me', {'fields': 'username'})['username'], attr(0)))
    for board in boards:
        with indent():
            board.short_print()


def list_lists(board_id):
    lists_response = request.get('1/boards/{}/lists'.format(board_id), {'filter': 'open'})
    lists = []

    for list_data in lists_response:
        lists.append(List(list_data))

    print('Lists in {}{}{}:'.format(attr(1),
                                    request.get('1/boards/{}'.format(board_id), {'fields': 'name'})['name'], attr(0)))
    for tlist in lists:
        with indent():
            tlist.short_print()


def list_cards(list_id):
    cards_response = request.get('1/lists/{}/cards'.format(list_id), {'filter': 'open'})
    cards = []

    for card_data in cards_response:
        cards.append(Card(card_data))

    print('Cards in {}{}{}:'.format(attr(1),
                                    request.get('1/lists/{}'.format(list_id), {'fields': 'name'})['name'], attr(0)))
    for card in cards:
        with indent():
            card.short_print()
