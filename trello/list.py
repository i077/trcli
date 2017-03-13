# Structure to hold lists

from colored import attr
from clint.textui import puts


class List:
    id = ''
    name = ''
    closed = False

    def __init__(self, content):
        self.id = content['id']
        self.name = content['name']
        self.closed = False if content['closed'] == 'false' else True

    def short_print(self):
        """Print short info about this list."""
        puts('{}{}{}'.format(attr(1), self.name, attr(0)))
