from storage import LocalFileStorage

class Album(object):
    """Album base class"""

    def __init__(self, storage=LocalFileStorage):
        self.service = {}
        self._storage = storage

    def getAlbum(self, service, default=None):
        """Load album info and list of image objects"""
        return self.service.get(service, default)

    def dump(self, f):
        """Gather all data into a simple dictionary stucture to provide
            to a storage backend"""
        return self._storage(self).dump(f)

    def dumps(self):
        return self._storage(self).dumps()



class AlbumAdaptor(object):
    """Album adaptor base class"""
    type = ''

    def __init__(self, id, album=None):
        self.album = album or Album()
        self.id = id
        self.service = {}
        self.title = None
        self.description = None
        self.date = None
        self.url = None
        self.images = []
        print "hello", self.service,
        self.album.service[self.type] = self

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








