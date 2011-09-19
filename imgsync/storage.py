import datetime
import cStringIO
import ConfigParser

CONFIG_VERSION = "1.0"

class Storage(object):
    """Encapsulate dumping/loading of persistent (cached) album data"""
    def __init__(self, album):
        """Pass in the album object to dump data from or load data to

        Note: in the future the album object collect all data and
        pass it in as a simple dictionary, to make writing storage backends
        easier.
        """
        self.album = album

    def dump(self, handle):
        """Given a file handle or some other I/O object, dump the data to it"""
        raise RuntimeError, "No implemented"

    def dumps(self):
        """Return dumped data as a string"""
        raise RuntimeError, "No implemented"

    def load(self, handle):
        """Given a file handle or some other I/O object, load data into album object"""
        raise RuntimeError, "No implemented"



class LocalFileStorage(Storage):
    """Use ConfigParser to create config file to store in local directory"""

    def dump(self, f):
        """Write out the album to storage
        """
        config = ConfigParser.ConfigParser()
        config.add_section('global')
        config.set('global', 'service', ', '.join(sorted(self.album.service.keys())))
        config.set('global', 'config', CONFIG_VERSION)

        for s in sorted(self.album.service.keys()):
            album = self.album.service[s]

            config.add_section(s)

            config.set(s, 'id', album.id)
            config.set(s, 'title', album.title)
            config.set(s, 'description', album.description)
            config.set(s, 'date', album.date)
            config.set(s, 'url', album.url)
            config.set(s, 'count', len(album.images))
            config.set(s, 'config', CONFIG_VERSION)
            config.set(s, 'timestamp', datetime.datetime.now())

            for i in range(len(album.images)):
                section = s+'-image-' + str(i+1)
                config.add_section(section)
                album.images[i].dumpConfig(config, section)

            config.write(f)


    def load(self, f):
        """
        """

    def dumps(self):
        f = cStringIO.StringIO()
        self.dump(f)
        return f.getvalue()



