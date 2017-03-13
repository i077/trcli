# Structure to hold cards

from colored import attr
from clint.textui import puts, indent


class Card:
    id = ''
    name = ''
    url = ''
    labels = []

    def __init__(self, content):
        self.id = content['id']
        self.name = content['name']
        self.closed = False if content['closed'] == 'false' else True
        self.url = content['shortUrl']

    def short_print(self):
        """Print short info about this card."""
        puts('{}{}{}'.format(attr(1), self.name, attr(0)))
        with indent():
            puts('{}{}{}'.format(attr(2), self.url, attr(0)))
