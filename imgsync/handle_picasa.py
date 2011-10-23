"""Code for handling local albums/images"""

import os, time, datetime, re
import urllib2

import gdata.photos.service
import gdata.media
import gdata.geo
from album import Album
from image import Image


class PicasaImage(Image):
        #  'albumid', 'author', 'category', 'checksum', 'client', 'commentCount', 'commentingEnabled', 'content', 'contributor', 'control', 'exif', 'extension_attributes', 'extension_elements', 'geo', 'gphoto_id', 'height', 'id', 'kind', 'link', 'media', 'position', 'published', 'rights', 'rotation', 'size', 'snippet', 'snippettype', 'source', 'summary', 'tags', 'text', 'timestamp', 'title', 'truncated', 'updated', 'version', 'width'

    def openFile(self):
        self.logger.debug("opening image: %s", self.id)
        return urllib2.urlopen(self.meta.content.src)

    def setDetails(self):
        self.size = int(self.meta.size.text)
        self.original = self.meta.timestamp.datetime()

    def setTags(self):
        tags = self.meta.media.keywords.text
        if tags:
            self.tags = tags.split(', ')

    def setDescription(self):
        # handled during instantiation
        pass

    def setGeolocation(self):
        if self.meta.geo.location():
            self.geocode = (self.meta.geo.latitude(),
                    self.meta.geo.longitude())

    def setComments(self):
        if self.meta.commentCount.text != '0':
            uri = '/data/feed/api/user/default/albumid/%s/photoid/%s?kind=comment'
            comments = self.album.client.GetFeed(uri % (self.meta.albumid.text, self.meta.gphoto_id.text))
            self.comments = []
            for e in comments.entry:
                comment = e.content.text
                if e.author:
                    comment += '  --' + e.author[0].name.text
                self.comments.append(comment)

    def calcImageHash(self):
        self.logger.debug("Reading image from net... %s" % self.filename)
        f = self.openFile()
        return self.calcHash(f)

    def makeMeta(self):
        raise RuntimeError, "Not implemented"



class PicasaAlbum(Album):
    """Adapt Album with support for picasa folder functionality. Album ID is
    the full path.
    """
    service_name = 'picasa'

    img_regex = re.compile(r'\.(png|jpg|jpeg)$', re.I)

    def postinit(self):
        self._client = None

    def getAlbumInfo(self):
        pass

    def getImages(self):
        uri = '/data/feed/api/user/default/albumid/%s?kind=photo'
        result = self.client.GetFeed(uri % self.id)
        self.images = []
        for p in result.entry:
            i = PicasaImage(p.gphoto_id.text, meta = p,
                    filename=p.content.src,
                    timestamp=p.timestamp.datetime(),
                    title = p.title and p.title.text or None,
                    description = p.summary and p.summary.text or None,
                    album = self)
            i.setAll()

            #print self.registry.dumpDict(), 'x'
            self.images.append(i)

    @property
    def client(self):
        if not self._client:
            client = gdata.photos.service.PhotosService()
            client.email = self.config['service']['picasa']['user']
            client.password = self.config['service']['picasa']['password']
            client.source = 'img-sync'
            client.ProgrammaticLogin()
            self._client = client
        return self._client

    def getAlbumList(self):
        """Fetch a list of albums from picasa"""
        result = self.client.GetUserFeed()
        return result.entry

    def printAlbumList(self):
        """Helper function to print list of recent albums to stdout to see the IDs"""
        for a in self.getAlbumList():
            print '%s %s [%s] %4s: %s' % (a.gphoto_id.text, a.timestamp.isoformat(),
                    a.access.text[:4], a.numphotos.text, a.title.text)



if __name__ == '__main__':
#    a = LocalAlbum(c['local'][0])
#    data = a.getAlbum()
#    #print a.album.dumps()
#    print a.album.dumpDict()

    def SearchUserAlbums(query, user='default', limit=100):
        uri = '/data/base/api/user/%s?kind=album' % (user,)
        return client.GetFeed(uri, limit=limit)

    albumid = '5649260481048764721' # ?
    albumid = '5658594342831965681' # imgsync
    #albums = client.GetUserFeed()
    album = PicasaAlbum(albumid)
    album.printAlbumList()
    #print album.getImages()
    #print album.registry.dumpDict()







