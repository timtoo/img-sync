"""Handle local albums/images"""

import os, time, datetime, re
from album import Album
from image import Image

try:
    import pyexiv2
except ImportError:
    pyexiv2 = None

class LocalAlbum(Album):
    """Represent an album on a local disk. Album ID is the full path."""
    service = 'local'
    img_regex = re.compile(r'\.(png|jpg|jpeg)$', re.I)

    def __init__(self, id):
        # remove trailing slash
        super(LocalAlbum, self).__init__(id.rstrip(os.sep))

    @staticmethod
    def stat2datetime(st):
        """Given an os.stat structure, return datetime object"""
        return datetime.datetime(*(time.localtime(st[8]))[0:6])

    def getAlbumInfo(self):
        path = self.id
        if os.path.exists(path):
            self.url = 'file://' + path
            # directory modification time
            self.date = self.stat2datetime(os.stat(self.id))
            self.description = ''
            # last element in path, with underscores converted to spaces
            self.title = os.path.split(path)[-1].strip(os.sep).replace('_', ' ')

            print self.id
            print self.title

        else:
            raise ValueError, "Album path does not exist: %s" % self.id

    def getImages(self):
        files = os.listdir(self.id)
        for fn in files:
            # recognize image files by extension
            if self.img_regex.search(fn):
                path = self.id + os.sep + fn
                st = os.stat(path)
                date = self.stat2datetime(os.stat(path))
                i = Image(path, filename=fn, timestamp=date)
                if pyexiv2:
                    meta = pyexiv2.ImageMetadata(path)
                    meta.read()
                    for k in ('Iptc.Application2.Keywords',
                                'Xmp.dc.subject',
                                'Xmp.digiKam.TagsList',
                                'Xmp.MicrosoftPhoto.LastKeywordXMP',
                                'Xmp.lr.hierarchicalSubject'):
                        if k in meta.iptc_keys and meta[k].value:
                            self.tags = meta[k].value
                            break

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
    print a.dumps()




