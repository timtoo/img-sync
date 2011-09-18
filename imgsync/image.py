import hashlib, json

class Image(object):
    """Base object for represeting single images.

    All of the set* methods must be overridden, to provide functionality.
    If a particular set* method is not needed, it still must be overridden
    to avoid an exception (to ensure it explicitely is not needed).
    """
    def __init__(self, id, filename=None, timestamp=None, title=None, description=None):
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

    @property
    def fileHash(self):
        if self._hashFile is None:
            _hash = hashlib.sha256()
            f = self.openFile()
            while True:
                data = f.read(1024000)
                if not data:
                    break
                _hash.update(data)
            self._hashFile = _hash.hexdigest()
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
            self.geocode and data.append(self.geocode)
            self.original and data.append(str(self.original))

            _hash = hashlib.sha256()
            _hash.update('\n'.join(data))
            self._hashMeta = _hash.hexdigest()
        return self._hashMeta

    def openFile(self):
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
        """Get any description associated with the object"""
        raise RuntimeError, "setGeolocation not implemented"

    def loadConfig(self, config, section):
        """ load object from config file"""
        pass

    def setMeta(self):
        self.setDetails()
        self.setTags()
        self.setDescription()
        self.setGeolocation()
        self.setComments()
        return self

    def dumpConfig(self, config, section):
        """Dump object data to a config file"""
        config.set(section, 'id', self.id)
        config.set(section, 'hash', self.fileHash)
        config.set(section, 'meta', self.metaHash)
        self.filename and config.set(section, 'filename', self.filename or '')
        self.title and config.set(section, 'title', self.title or '')
        self.description and config.set(section, 'description',
                self.description or '')
        self.timestamp and config.set(section, 'timestamp', self.timestamp)
        self.original and config.set(section, 'original', self.original)
        self.size and config.set(section, 'size', self.size)
        self.geocode and config.set(section, 'geocode', self.geocode)
        config.set(section, 'tags', json.dumps(self.tags))

