"""Code for handling local albums/images"""

import os, time, datetime, re
from album import Album, AlbumAdaptor
from image import Image

try:
    import pyexiv2
except ImportError:
    print "Warning: pyexiv2 not found: embedded local image metadata will be ignored"
    pyexiv2 = None

class LocalImage(Image):
    @staticmethod
    def stat2datetime(st):
        """Given an os.stat structure, return datetime object"""
        return datetime.datetime(*(time.localtime(st[8]))[0:6])

    def openFile(self):
        return open(self.id, 'rb')

    def setDetails(self):
        st = os.stat(self.id)
        self.timestamp = self.stat2datetime(st)
        self.title = self.filename

    def setTags(self):
        self.tags = []
        meta = self.getExiv2()
        if meta:
            for k in ('Iptc.Application2.Keywords',
                        'Xmp.dc.subject',
                        'Xmp.digiKam.TagsList',
                        'Xmp.MicrosoftPhoto.LastKeywordXMP',
                        'Xmp.lr.hierarchicalSubject'):
                if k in meta.iptc_keys and meta[k].value:
                    self.tags = meta[k].value
                    break

    def setDescription(self):
        meta = self.getExiv2()
        if meta:
            self.description = meta.comment
        else:
            self.description =  ''

    def setGeolocation(self):
        pass

    def setComments(self):
        pass

    def getExiv2(self):
        """Return exiv2 metadata object"""
        if not hasattr(self, '_exiv2'):
            if pyexiv2:
                self._exiv2 = pyexiv2.ImageMetadata(self.id)
                self._exiv2.read()
        return self._exiv2


class LocalAlbum(AlbumAdaptor):
    """Adapt Album with support for local directory functionality. Album ID is the full path."""
    service = 'local'
    img_regex = re.compile(r'\.(png|jpg|jpeg)$', re.I)

    def __init__(self, id, album=None):
        self.album = album or Album()
        self.album.service[self.service] = self

        # remove trailing slash from directory name
        super(LocalAlbum, self).__init__(id.rstrip(os.sep))

    def getAlbumInfo(self):
        path = self.id
        if os.path.exists(path):
            self.url = 'file://' + path
            # directory modification time
            self.date = LocalImage.stat2datetime(os.stat(self.id))
            self.description = ''
            # last element in path, with underscores converted to spaces
            self.title = os.path.split(path)[-1].strip(os.sep).replace('_', ' ')

        else:
            raise ValueError, "Album path does not exist: %s" % self.id

    def getImages(self):
        files = os.listdir(self.id)
        for fn in files:
            # recognize image files by extension
            if self.img_regex.search(fn):
                path = self.id + os.sep + fn
                i = LocalImage(path, filename=fn)
                i.setMeta()
                self.images.append(i)

            # XXX todo
            # - get comment from jpeg comment
            # - get tags from iptc keywords
            # - get geocode from



if __name__ == '__main__':
    import config
    c = config.Config()

    a = LocalAlbum(c['source'][0])
    data = a.getAlbum()
    print a.album.dumps()




