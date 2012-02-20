import datetime

class Album(object):
    """Album adaptor base class. Create an subclass of this, as well as the Image class
    to support a new service type.
    """
    service_name = ''

    def __init__(self, id, config=None):
        self.id = id
        self.title = None
        self.description = None
        self.date = None
        self.url = None
        self.images = []
        self.config = config
        self.postinit()

    def postinit(self):
        """Stuff to do by subclasses after __init__ takes place"""
        pass

    def scanImages(self):
        """Populate self.imagesi and call self.setAll() on each"""
        raise RuntimeError, "getImages not implemented"

    def scanInfo(self):
        """Set the album attributes"""
        raise RuntimeError, "scanInfo not implemented"

    def scan(self):
        """Scan album for info and list of image objects"""
        self.scanInfo()
        self.scanImages()
        return self

    def lookupImage(self, key, val):
        """Iterate self.images and return image with given value on key"""
        for i in self.images:
            if getattr(i, key, None) == val:
                return i
        return None

    def dumpDict(self):
        """Return album data as a dictionary"""
        album = {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'date': self.date,
                'url': self.url,
                'timestamp': datetime.datetime.now(),
                'images': []
            }

        for i in self.images:
            album['images'].append(i.dumpDict())

        return album

    def locate(self, album, image):
        pass


    def diff(self, album):
        """Return dictionary of differences of the given album compared
                to the current album.

            the "images" key will contain a dictionary
            with the keys:

                - changed (list of image objects from
                        this album with differences),
                - same (list of images which match up),
                - new (list of images not found in this album),
                - unique (list of images in this album which are not
                        in the provided album)

        """
        this = self.dumpDict()
        that = album.dumpDict()

        diff = {
                'same': [],
                'new': [],
                'unique': [],
                'changed': [],
                }

        # look for differences in album attributes
        for k in ('title', 'description', 'date'):
            if getattr(self, k) != getattr(album, k):
                diff[k] = getattr(album, k)

        thatDict = dict([(x.id, x) for x in album.images])

        for img in self.images:
            if thatDict.has_key(img.id):
                imgdiff = i.diff(thatDict(img.id))
                if imgdiff:
                    diff['changed'].append(imgdiff)
                else:
                    diff['same'].append(img)
                del thatDict[img.id]
            else:
                diff['unique'].append(img)

        diff['new'] = thatDict.values()

        return diff


    def create(self, album):
        """Given an album object create/update album on this service
        """

    def exists(self):
        """Return boolean result to a check whether this album
            yet physically exists
        """
        raise RuntimeError, "exists not implemented"

    def getAlbumList(self):
        raise RuntimeError, "getting album list not implemented"

    def printAlbumList(self):
        print "Printing album list for %s service is not available." % self.service_name



