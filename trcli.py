# Command line interface for trcli, a subclass of cmd

import cmd
import json
# import os
import shlex

from clint.textui import colored

from context import Context, ContextLevel
from func import request, list

CLI_NAME = 'trcli'


class Trcli(cmd.Cmd):

    def __init__(self):
        super().__init__()

        # Check for an API Token
        try:
            open('config.txt')
        except FileNotFoundError:
            print("No auth token found. Go to the following URL and paste your token in here.")
            self.do_auth('')
            return

        # Get user's info
        print('Authenticating...')
        user_data = {}
        try:
            user_data = request.get('/1/members/me', {'fields': 'fullName,username'})
        except json.JSONDecodeError:
            print('There was a problem communicating with Trello. Rerun to re-authenticate.')
            # os.remove('config.txt')
        self.username = user_data['username']

        self.context = Context()

        self.intro = 'Signed in as {} ({}).'.format(user_data['fullName'], user_data['username'])
        self.update_prompt()

    def update_prompt(self):
        self.prompt = '{}@trello:{}$ '.format(self.username, self.context.path)

    @staticmethod
    def do_auth(arg):
        """auth: auth [token]\n\tGet a new authentication token. If given one, save it instead of prompting for one."""
        arg = shlex.split(arg)

        # Prompt for new token with URL if not given one
        if len(arg) == 0:
            print('Follow this URL, grant {} access, and enter the generated token here.'.format(CLI_NAME))
            print('https://trello.com/1/connect?key={}&name={}&response_type=token&expires=never&scope=read,write'
                  .format(request.API_KEY, CLI_NAME))
            new_token = input('token: ')
        # If give one, save it to config.txt
        else:
            new_token = arg[0]
        f = open('config.txt', 'w')
        f.write(new_token)

    def do_ls(self, arg):
        """list: list [context]\n\tLists contents of current or specified context."""
        arg = shlex.split(arg)

        if len(arg) == 0:
            context_level = self.get_context_level()
            if context_level == ContextLevel.USER:
                list.list_boards()
            elif context_level == ContextLevel.BOARD:
                list.list_lists(self.context.data['id'])
            elif context_level == ContextLevel.LIST:
                list.list_cards(self.context.data['id'])

        else:
            context = self.rel_to_abs_context(arg[0])
            if context[0] == '~':
                list.list_boards()
            else:
                print(colored.yellow('Listing specific contexts not implemented yet'))

    def do_cd(self, arg):
        """cd: cd [context]\n\tChange to a different context."""
        # Check if context is valid
        arg = shlex.split(arg)
        if len(arg) == 0:
            self.context.enter_user()
        # Look up id of board and call enter_board on context
        elif self.get_context_level() == ContextLevel.USER:
            board_name = arg[0]
            if board_name in self.context.cd:
                board_id = self.context.cd[board_name]
                self.context.enter_board(board_id)
            else:
                print(colored.red('Invalid board name.'))
        elif self.get_context_level() == ContextLevel.BOARD:
            if arg[0] == '..':
                self.context.enter_user()
            else:
                list_name = arg[0]
                self.context.enter_list(self.context.cd[list_name])
        elif self.get_context_level() == ContextLevel.LIST:
            if arg[0] == '..':
                self.context.enter_board(self.context.parent)
            else:
                card_name = arg[0]
        self.update_prompt()

    # noinspection PyUnusedLocal
    @staticmethod
    def do_exit(arg):
        """exit: exit | ^D\n\tExit the CLI."""
        print()
        return True

    # Sending an EOF will exit the CLI.
    do_EOF = do_exit

    def rel_to_abs_context(self, context):
        if context[0] == '~':
            return context
        return '{}/{}'.format(self.context.path, context)

    def get_context_level(self, context=None):
        """Return level that this context is currently in."""
        if context is None:
            context = self.context.path

        levels = context.split('/')
        return ContextLevel(len(levels))
