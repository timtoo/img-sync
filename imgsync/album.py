import cStringIO
import ConfigParser

class Album(object):
    """Album base class"""
    service = ''


    def __init__(self, id):
        self.id = id
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







