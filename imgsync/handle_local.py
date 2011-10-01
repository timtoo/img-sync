"""Code for handling local albums/images"""

import os, time, datetime, re
import logging
from album import Album
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
        meta = self.meta
        if meta:
            for k in keys:
                if k in meta.iptc_keys and meta[k].value or \
                        k in meta.exif_keys or \
                        k in meta.xmp_keys:
                    if raw:
                        return meta[k].raw_value
                    else:
                        return meta[k].value
        return default

    def openFile(self):
        self.logger.debug("""Opening image: %s""", self.id)
        return open(self.id, 'rb')

    def setDetails(self):
        st = os.stat(self.id)
        self.timestamp = self.stat2datetime(st)
        self.title = self.filename
        self.size = os.stat(self.id)[6]

        if self.meta:
            if 'Exif.Photo.DateTimeOriginal' in self.meta.exif_keys:
                self.original = self.meta['Exif.Photo.DateTimeOriginal'].value
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
        if self.meta:
            self.description = self.meta.comment
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
            self.geocode = (latitude, latitudeRef, longitude, longitudeRef)

    def setComments(self):
        pass

    def makeMeta(self):
        """meta means an exiv2 metadata object for local files"""
        meta = None
        if pyexiv2:
            meta = pyexiv2.ImageMetadata(self.id)
            meta.read()
        return meta

    def calcImageHash(self):
        f = self.openFile()
        return self.calcHash(f)


class LocalAlbum(Album):
    """Adapt Album with support for local directory functionality. Album ID is the full path."""
    service_name = 'local'

    img_regex = re.compile(r'\.(png|jpg|jpeg)$', re.I)

    def postinit(self):
        if self.id:
            # clean/normalize path
            self.id = os.path.abspath(self.id.strip().rstrip(os.sep))

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
                i.setAll()
                self.images.append(i)

            # XXX todo
            # - get comment from jpeg comment
            # - get tags from iptc keywords
            # - get geocode from



if __name__ == '__main__':
    import logging
    logging.basicConfig()

    import config
    c = config.Config()
    c.pprint()

    a = LocalAlbum(c['local'][0])
    data = a.getAlbum()
    #print a.registry.dumps()
    print a.registry.dumpDict()





