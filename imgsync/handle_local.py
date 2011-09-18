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

    def firstExiv2Val(self, keys, default=None, raw=False):
        meta = self.getExiv2()
        if meta:
            for k in keys:
                if k in meta.iptc_keys and meta[k].value or \
                        k in meta.exif_keys or \
                        k in meta.xmp_keys:
                    if raw:
                        print k, meta[k]
                        return meta[k].raw_value
                    else:
                        return meta[k].value
        return default

    def openFile(self):
        return open(self.id, 'rb')

    def setDetails(self):
        st = os.stat(self.id)
        self.timestamp = self.stat2datetime(st)
        self.title = self.filename
        self.size = os.stat(self.id)[6]

        meta = self.getExiv2()
        if 'Exif.Photo.DateTimeOriginal' in meta.exif_keys:
            self.original = meta['Exif.Photo.DateTimeOriginal'].value
        else:
            self.original = self.timestamp

    def setTags(self):
        self.tags = self.firstExiv2Val((
                        'Iptc.Application2.Keywords',
                        'Xmp.dc.subject',
                        'Xmp.digiKam.TagsList',
                        'Xmp.MicrosoftPhoto.LastKeywordXMP',
                        'Xmp.lr.hierarchicalSubject',
                         ), default=[])

    def setDescription(self):
        meta = self.getExiv2()
        if meta:
            self.description = meta.comment
        else:
            self.description =  ''

    def setGeolocation(self):
        latitude = self.firstExiv2Val((
                        'Exif.GPSInfo.GPSLatitude',
                        'Xmp.exif.GPSLatitude'
                         ), raw=True)
        latitudeRef = self.firstExiv2Val((
                        'Exif.GPSInfo.GPSLatitudeRef',
                        'Xmp.exif.GPSLatitudeRef'
                         ), raw=True)
        longitude = self.firstExiv2Val((
                        'Exif.GPSInfo.GPSLongitude',
                        'Xmp.exif.GPSLongitude'
                         ), raw=True)
        longitudeRef = self.firstExiv2Val((
                        'Exif.GPSInfo.GPSLongitudeRef',
                        'Xmp.exif.GPSLongitudeRef'
                         ), raw=True)
        if latitude:
            self.geocode = str((latitude, latitudeRef, longitude, longitudeRef))

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
        super(LocalAlbum, self).__init__(os.path.abspath(id.rstrip(os.sep)))

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




