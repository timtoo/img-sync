"""Code for handling local albums/images"""

import os, time, datetime, re

import gdata.photos.service
import gdata.media
import gdata.geo

from album import Album
from image import Image


class PicasaImage(Image):

    def setDetails(self):
        pass

    def setTags(self):
        pass

    def setDescription(self):
        pass

    def setGeolocation(self):
        pass

    def setComments(self):
        pass



class PicasaAlbum(Album):
    """Adapt Album with support for picasa folder functionality. Album ID is the full path."""
    service_name = 'local'

    img_regex = re.compile(r'\.(png|jpg|jpeg)$', re.I)

    def postinit(self):
        self._client = None

    def getAlbumInfo(self):
        pass

    def getImages(self):
        pass

    @property
    def client(self):
        if not self._client:
            client = gdata.photos.service.PhotosService()
            client.email = self.registry.config['service']['picasa']['user']
            client.password = self.registry.config['service']['picasa']['password']
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
            print a.gphoto_id.text, a.timestamp.isoformat(), a.access.text[:4], a.name.text



if __name__ == '__main__':
#    a = LocalAlbum(c['local'][0])
#    data = a.getAlbum()
#    #print a.album.dumps()
#    print a.album.dumpDict()

    def SearchUserAlbums(query, user='default', limit=100):
        uri = '/data/base/api/user/%s?kind=album' % (user,)
        return client.GetFeed(uri, limit=limit)

    #albums = client.GetUserFeed()
    album = PicasaAlbum('')
    album.printAlbumList()






