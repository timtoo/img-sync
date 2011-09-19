import os
import argparse
import ConfigParser

SERVICE = ( 'digikam', 'picasa', )

class Config(object):
    """Unfied interface to commandline and config file options.

    See self.data for config file options.
    """

    def __init__(self):
        self._config_filename = '.pycasa-sync.rc'
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
        parser.add_argument('--config')
        parser.add_argument('--picasa-user')
        parser.add_argument('--picasa-password', '--password')
        parser.add_argument('-t', '--sync-to', choices=SERVICE)
        parser.add_argument('-f', '--sync-from', choices=SERVICE)

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


if __name__ == '__main__':
    import pprint
    c = Config()
    pprint.pprint(c._config_path)
    pprint.pprint(c.data)



