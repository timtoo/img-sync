import hashlib, json
from cStringIO import StringIO
import logging

class Image(object):
    """Base object for represeting single images.

    All of the set* methods must be overridden, to provide functionality.
    If a particular set* method is not needed, it still must be overridden
    to avoid an exception (to ensure it explicitely is not needed).

    meta - an arbitrary object that can be passed in or set on an
    image object. it may have different meaning specific to the service
    an image belongs to.

    album - the album object that this photo belongs to
    """
    def __init__(self, id, filename=None, timestamp=None, title=None,
            description=None, meta=None, album=None):
        self.service = {}
        self.id = id
        self.filename = filename
        self.timestamp = timestamp
        self.title = title
        self.description = description
        self.tags = []
        self.comments = []
        self.size = None
        self.geocode = None
        self.original = None
        self._hashMeta = None
        self._hashFile = None
        self.localid = None
        self._meta = meta
        self.album = album
        self.logger = logging.getLogger('imgsync.image')

    @property
    def meta(self):
        """Wrapper around self._meta to call makeMeta() if needed"""
        if self._meta is None:
            self._meta = self.makeMeta()
        return self._meta

    def calcHash(self, source):
        """Given a file handle or string, return a hash string; this method
        is to standardize the hashing method for all handlers
        """
        if source:
            if not hasattr(source, 'read'):
                source = StringIO(source)
            else:
                # if this is a file handle, assume image file and check config permission
                if self.album.config and ((self.album.config.opts.check_meta) or (not self.album.config.opts.check_all)):
                    return None

            hash = hashlib.sha256()
            while True:
                data = source.read(1024000)
                if not data:
                    break
                hash.update(data)
            return hash.hexdigest()

    def calcImageHash(self):
        """Method called to calculate hash value for image file.
        The job of this method is to create a file handle to
        the image data, and return the result of passing that
        filehandle to self.calcHash()
        """
        raise RuntimeError, "calcImageHash not implemented"

    @property
    def imageHash(self):
        """Wrapper around calcImageHash() to use as a property"""
        if self._hashFile is None:
            self._hashFile = self.calcImageHash()
        return self._hashFile

    @property
    def metaHash(self):
        """This, used to detect a meta data change, includes:
                - title
                - description
                - comments
                - tags
                - geocode
                - embedded photo creation date
        """
        if self._hashMeta is None:
            data = []
            self.title and data.append(self.title)
            self.description and data.append(self.description)
            self.comments and data.append(','.join(self.comments))
            self.tags and data.append(','.join(self.tags))
            self.geocode and data.append(json.dumps(self.geocode))
            self.original and data.append(str(self.original))
            # should size (bytes) be added?

            self._hashMeta = self.calcHash('\n'.join(data))
        return self._hashMeta

    def openFile(self):
        """Return a new file handle to the raw image"""
        raise RuntimeError, "openFile not implemented"

    def setDetails(self):
        """Set object attribute details such as title, size, date, etc.
        This method is always called before any other set* methods, so
        it can set up object attributes to be used by other set* methods.
        """
        raise RuntimeError, "setDetails not implemented"

    def setTags(self):
        """Load tags associated with object"""
        raise RuntimeError, "setTags not implemented"

    def setDescription(self):
        """Get any description applied to the object"""
        raise RuntimeError, "setDescription not implemented"

    def setComments(self):
        """Get any description attached to the object"""
        raise RuntimeError, "setComments not implemented"

    def setGeolocation(self):
        """set self.geocode with (latitude, longitude)"""
        raise RuntimeError, "setGeolocation not implemented"

    def makeMeta(self):
        """Code to return data for the self.meta object"""
        pass

    def setAll(self):
        """Execute all the self.set* methods to attach data to image"""
        self.setDetails()
        self.setTags()
        self.setDescription()
        self.setGeolocation()
        self.setComments()
        return self

    def loadDict(self, data):
        """Take dictionary from data into object"""
        self._hashFile = data.get('hash')
        self._hashMeta = data.get('meta')
        self.filename = data.get('filename')
        self.title = data.get('title')
        self.description = data.get('description')
        self.timestamp = data.get('timestamp')
        self.original = data.get('original')
        self.localid = data.get('localid')
        self.size = data.get('size')
        self.geocode = data.get('geocode')
        self.tags = data.get('tags')
        return self

    def dumpDict(self):
        """Dump object data to a config file"""
        data = {
                'id': self.id,
                'hash': self.imageHash,
                'meta': self.metaHash,
                }
        if self.filename: data['filename'] = self.filename
        if self.title: data['title'] = self.title
        if self.description: data['description'] = self.description
        if self.timestamp: data['timestamp'] = self.timestamp
        if self.original: data['original'] = self.original
        if self.localid: data['localid'] = self.localid
        if self.size: data['size'] = self.size
        if self.geocode: data['geocode'] = self.geocode
        if self.tags: data['tags'] = self.tags
        return data

    def diffImage(self, image):
        """Given an image object, return the differences as it exists on
            this service.

            Return dictionary containing keys of differences,
            the values being True or other difference details if appropriate.

            Return None if no matching image exists at this service.
        """
        raise RuntimeError, "Not implemented"

    def storeImage(self, image):
        """Pass the image object on the given service

            This should update an existing matching image already stored on
            the service if necessary/possible.
        """
        raise RuntimeError, "store Image not implemented for service"







