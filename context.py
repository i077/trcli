# Class to keep track of and change contexts.
from enum import Enum
from func import request


class Context:
    path = '~'
    data = {}
    cd = {}  # For TAB-completion
    parent = ''

    def __init__(self):
        self.enter_user()

    def enter_user(self):
        """Enter a user-level context."""
        self.path = '~'
        self.data = request.get('1/members/me')
        self.cd = self.cd_json_to_dict(request.get('1/members/me/boards', {'filter': 'open',
                                                                           'fields': 'id,name'}))
        self.parent = ''

    def enter_board(self, board_id):
        """Enter a board-level context."""
        board_data = request.get('1/boards/{}'.format(board_id))
        self.path = '~/{}'.format(board_data['name'])
        self.data = board_data
        self.cd = self.cd_json_to_dict(request.get('1/boards/{}/lists/open'.format(board_id)))

    def enter_list(self, list_id):
        """Enter a list-level context."""
        list_data = request.get('1/lists/{}'.format(list_id))
        parent_data = request.get('1/lists/{}/board'.format(list_id), {'fields': 'id,name'})
        self.parent = parent_data['id']
        self.path = '~/{}/{}'.format(parent_data['name'], list_data['name'])
        self.data = list_data
        self.cd = self.cd_json_to_dict(request.get('1/lists/{}/cards/open'.format(list_id)))

    def enter_card(self, card_id):
        """Enter a card-level context."""
        card_data = request.get('1/cards/{}'.format(card_id))
        parent_data = request.get('1/cards/{}/list'.format(card_id), {'fields': 'id,name'})
        self.parent = parent_data['id']
        self.path = '~/{}/{}'.format(parent_data['name'], card_data['name'])
        self.data = card_data
        # self.cd = self.cd_json_to_dict(request.get('1/lists/{}/cards/open'.format(card_id)))

    @staticmethod
    def cd_json_to_dict(json_data):
        """Converts a JSON-formatted dict with 'id' and 'name' fields to a dict mapping name to id."""
        endpoints = {}
        for pair in json_data:
            endpoints[pair['name']] = pair['id']
        return endpoints


class ContextLevel(Enum):
    USER = 1
    BOARD = 2
    LIST = 3
    CARD = 4
