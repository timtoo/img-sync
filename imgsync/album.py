
class Album(object):
    """Album base class"""
    title = None
    description = None
    date = None
    url = None
    id = None

    images = []

    def __init__(self, id):
        self.id = id


    def getPhotos(self):

    def getAlbumInfo(self):


    def getAlbum(self):
        """Load album info and list of photo objects"""
        self.getAlbumInfo()
        self.getPhotos()
