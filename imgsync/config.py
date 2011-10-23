"""Parse command line and config/ini files and provide a dictionary-like interface"""

import os
import argparse
import ConfigParser

SERVICE = ( 'digikam', 'picasa', )  # this really should be dynamic from ServicePlugin._service

class Config(object):
    """Unfied interface to commandline and config file options.

    See self.data for config file options.
    """

    def __init__(self):
        self._config_filename = '.img-sync.rc'
        self._config_path = None
        self.parser = None
        self.opts = None
        self.args = None
        self.data = {
            'local': None,
            'service': {},
            }

        for s in SERVICE:
            self.data['service'][s] = {}

        self.config_from_cli()
        self.config_from_file()

    def get(self, key, default=None):
        return self.data.get(key)

    def __getitem__(self, key):
        return self.data[key]

    def command_line_help(self):
        print "Usage: pycasa-sync [directory]"

    def config_from_cli(self):
        """Get options from command line"""
        parser = argparse.ArgumentParser()
        parser.add_argument('local', nargs='*')
        parser.add_argument('--config', help="specify config file")
        parser.add_argument('--print-config', action='store_true',
                help="display config after parsing config file and command line.")
        parser.add_argument('--picasa-user')
        parser.add_argument('--picasa-password')
        parser.add_argument('--picasa-title',
                help="Name of album on Picassa (if lookup needed)")
        parser.add_argument('--picasa-id',
                help="ID of album on Picassa (overrides picasa-title)")
        parser.add_argument('-l', '--list', choices=SERVICE,
                help="List all albums on a specified service, if possible")
        parser.add_argument('-t', '--sync-to', choices=SERVICE)
        parser.add_argument('-f', '--sync-from', default='local',
                choices=SERVICE)
        parser.add_argument('-d', '--diff-with', default='local',
                choices=SERVICE, help="What to diff against")

        opts = parser.parse_args()
        for k in self.data.keys():
            if getattr(opts,k,None):
                self.data[k] = getattr(opts,k,None)

        if opts.picasa_user:
            self.data['service']['picasa']['user'] = opts.picasa_user
        if opts.picasa_password:
            self.data['service']['picasa']['password'] = opts.picasa_password

        if opts.config:
            self._config_path = opts.config

        self.opts = opts
        return self

    @property
    def config_filename(self):
        """Try current file directory, then home directory, else None"""
        if self._config_path is None:
            self._config_path = os.path.join(os.path.split(__file__)[0], self._config_filename)
            if not os.path.exists(self._config_path):
                self._config_path = os.path.expanduser('~/'+self._config_filename)
                if not os.path.exists(self._config_path):
                    self._config_path = None
        return self._config_path

    def config_from_file(self):
        """Read config file

        main options are in [global] section. Then a section may exist for each
        supported "service", to contain data needed to interact with that service.

        [picasa]
        user = <username>
        password = <password>

        """
        if self.config_filename:
            parser = ConfigParser.ConfigParser()
            parser.read(self.config_filename)
            for k in self.data.keys():
                try:
                    val = parser.get('global', k)
                    if val:
                        self.data[k] = val
                except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
                    pass

            for s in SERVICE:
                if parser.has_section(s):
                    for k,v in parser.items(s):
                        # do not overwrite settings already set via command line
                        if not self.data['service'][s].has_key(k):
                            self.data['service'][s][k] = v

            self.parser = parser

    def pprint(self):
        """Pretty Print the contents of the config object, for debugging"""
        import pprint
        print '### Config file: %r' % self._config_path
        pprint.pprint(self.data)
        print '### Command line options:'
        pprint.pprint(self.opts)
        print '### Command line arguments:'
        pprint.pprint(self.args)
        print


if __name__ == '__main__':
    c = Config()
    c.pprint()



