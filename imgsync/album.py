
class Album(object):
    """Album base class"""
    service = ''
    title = None
    description = None
    date = None
    url = None
    id = None

    images = []

    def __init__(self, id):
        self.id = id

    def getPhotos(self):
        raise RuntimeError, "not implemented"

    def getAlbumInfo(self):
        raise RuntimeError, "not implemented"

    def getAlbum(self):
        """Load album info and list of photo objects"""
        self.getAlbumInfo()
        self.getPhotos()

    def dump(self, f):
        """
        """

    def load(self, f):
        """
        """

