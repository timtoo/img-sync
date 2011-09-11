
class Image(object):
    def __init__(self, id):
        self.id = id
        self.fileTimestamp = None
        self._hashTitle = None
        self._hashDescription = None
        self._hashGeocode = None
        self._hashComments = None
        self._hashTags = None
        self._hashRaw = None

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


