# Main interpreter interface for the Trello CLI.

from trcli import Trcli


if __name__ == '__main__':
    cli = Trcli()
    cli.cmdloop()
