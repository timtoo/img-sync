class Config(object):
    """Unfied interface to commandline and config file options.

    See self.data for config file options.
    """

    def __init__(self):
        self._config_filename = None
        self.data = {
            'user': None,
            'password': None,
            'source': None,
            }
        self.config_from_file()
        self.config_from_cli()

    def get(self, key, default=None):
        return self.data.get(key)

    def __getitem__(self, key):
        return self.data[key]

    def command_line_help(self):
        print "Usage: pycasa-sync [directory]"

    def config_from_cli(self):
        """Get options from command line"""
        parser = optparse.OptionParser()
        parser.add_option('-u', '--user')
        parser.add_option('-p', '--password')
        opts, args = parser.parse_args()
        for k in self.data.keys():
            if getattr(opts,k,None):
                self.data[k] = getattr(opts,k,None)
        if args:
            self.data['source'] = args
        return self

    @property
    def config_filename(self):
        """try current file directory, then home directory, else None"""
        if self._config_filename is None:
            fn = '.pycasa-sync.rc'
            self._config_filename = os.path.join(os.path.split(__file__)[0], fn)
            if not os.path.exists(self._config_filename):
                self._config_filename = os.path.expanduser('~/'+fn)
                if not os.path.exists(self._config_filename):
                    self._config_filename = None
        return self._config_filename

    def config_from_file(self):
        """Read config file"""
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


