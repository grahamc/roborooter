
from optparse import OptionParser


class CommandLine(object):
    def __init__(self):
        self.parser = OptionParser()
        self._add_options()

    def parse(self, args=None):
        return self.parser.parse_args(args=None)

    def _add_options(self):
        self.parser.add_option(
            '-c',
            '--config',
            dest='config',
            default='/etc/roborooter.ini',
            help='load roborooter config from CONFIG'
        )
        self.parser.add_option(
            '-d',
            '--dry',
            action='store_true',
            dest='dry_run'
        )
        self.parser.add_option(
            '-f',
            '--force',
            action='store_true',
            dest='actually_run'
        )
        self.parser.add_option(
            '-v',
            '--verbose',
            action='count',
            default=False,
            dest='verbose'
        )
        self.parser.add_option(
            '-q',
            '--quiet',
            action='count',
            default=False,
            dest='quiet'
        )
