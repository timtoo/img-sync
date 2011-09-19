import cStringIO
import ConfigParser
import datetime
import json

CONFIG_VERSION = "1.0"

class Album(object):
    """Album base class"""

    def __init__(self):
        self.service = {}

    def getAlbum(self, service, default=None):
        """Load album info and list of image objects"""
        return self.service.get(service, default)

    def dump(self, f):
        """Write out the album to storage
        """
        config = ConfigParser.ConfigParser()
        config.add_section('global')
        config.set('global', 'service', ', '.join(sorted(self.service.keys())))
        config.set('global', 'config', CONFIG_VERSION)

        for s in sorted(self.service.keys()):
            album = self.service[s]

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



class AlbumAdaptor(object):
    """Album adaptor base class"""
    service = ''

    def __init__(self, id):
        self.id = id
        self.service = {}
        self.title = None
        self.description = None
        self.date = None
        self.url = None
        self.images = []

    def getImages(self):
        """Populate self.images"""
        raise RuntimeError, "getImages not implemented"

    def getAlbumInfo(self):
        """Set the album attributes"""
        raise RuntimeError, "getAlbumInfo not implemented"

    def getAlbum(self):
        """Load album info and list of image objects"""
        self.getAlbumInfo()
        self.getImages()

    def dump(self, f):
        """Write out the album to storage
        """
        config = ConfigParser.ConfigParser()
        config.add_section('album')

        config.set('album', 'id', self.id)
        config.set('album', 'title', self.title)
        config.set('album', 'description', self.description)
        config.set('album', 'date', self.date)
        config.set('album', 'url', self.url)
        config.set('album', 'count', len(self.images))

        for i in range(len(self.images)):
            section = 'image-' + str(i+1)
            config.add_section(section)
            self.images[i].dumpConfig(config, section)

        config.write(f)


    def load(self, f):
        """
        """

    def dumps(self):
        f = cStringIO.StringIO()
        self.dump(f)
        return f.getvalue()







