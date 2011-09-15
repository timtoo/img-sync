import hashlib, json

class Image(object):
    def __init__(self, id, filename=None, timestamp=None, title=None, description=None):
        self.service = {}
        self.id = id
        self.filename = filename
        self.timestamp = timestamp
        self.title = title
        self.description = description
        self.tags = []
        self.comments = []
        self.geocode = None
        self._hashMeta = None
        self._hashFile = None

    @property
    def hashFile(self):
        if self._hashFile is None:
            _hash = hashlib.sha256()
            f = open(self.id, 'rb')
            while True:
                data = f.read(1024000)
                if not data:
                    break
                _hash.update(data)
            self._hashFile = _hash.hexdigest()
        return self._hashFile

    @property
    def hashMeta(self):
        """This includes:
                - title
                - description
                - comments
                - tags
                - geocode
                - date
        """
        data = []
        if self._hashMeta is None:
            _hash = hashlib.sha256()
            _hash.update('\n'.join(data))
            self._hashMeta = _hash.hexdigest()
        return self._hashMeta

    def getRawImage(self):
        raise RuntimeError, "getRawImage not implemented"

    def getTags(self):
        return []

    def getDescription(self):
        return ''

    def getComments(self):
        return []

    def getGeocoding(self):
        return

    def loadConfig(self, config, section):
        pass

    def dumpConfig(self, config, section):
        config.set(section, 'id', self.id)
        self.filename and config.set(section, 'filename', self.filename or '')
        self.description and config.set(section, 'description',
                self.description or '')
        self.timestamp and config.set(section, 'timestamp', self.timestamp)
        print self.tags
        config.set(section, 'tags', json.dumps(self.tags))

