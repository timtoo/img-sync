
class Album(object):
    """Album adaptor base class. Create an subclass of this, as well as the Image class
    to support a new service type.
    """
    service_name = ''

    def __init__(self, id):
        self.id = id
        self.title = None
        self.description = None
        self.date = None
        self.url = None
        self.images = []
        self.postinit()

    def postinit(self):
        """Stuff to do by subclasses after __init__ takes place"""
        pass

    def getImages(self):
        """Populate self.imagesi and call self.setAll() on each"""
        raise RuntimeError, "getImages not implemented"

    def getAlbumInfo(self):
        """Set the album attributes"""
        raise RuntimeError, "getAlbumInfo not implemented"

    def getAlbum(self):
        """Load album info and list of image objects"""
        self.getAlbumInfo()
        self.getImages()
        return self

    def lookupImage(self, key, val):
        """Iterate self.images and return image with given value on key"""
        for i in self.images:
            if getattr(i, key, None) == val:
                return i
        return None

    def diffAlbum(self, album):
        """Return dictionary of differences.

            the "images" key will contain a dictionary
            with the keys:

                - different (contining list of
                    image objects from this album with differences),
                - same (containing images which match up),
                - new (containing images not found in this album),
                - unknown (images in this album which are not
                    in the source album)

        """

    def createAlbum(self, album):
        """Given an album object create/update album on this service
        """

    def exists(self):
        """Return boolean result to a check whether this album
            yet physically exists
        """
        raise RuntimeError, "exists not implemented"


