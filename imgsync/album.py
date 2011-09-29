import datetime

from storage import LocalFileStorage
from config import Config

class AlbumRegistry(object):
    """A singleton intended for all Album instances to share

    It collects all of the album instances and provides methods that act on all
    existing Album instances.

    This class is created automatically if it doesn't already exist when instantiating an Album.

    This class contains a Config() object to be shared by all processes.
    """

    def __init__(self, storage=LocalFileStorage):
        self.service = {}
        self._storage = storage
        self.config = Config()

    def getAlbum(self, service, default=None):
        """Load album info and list of image objects"""
        return self.service.get(service, default)

    def dumpDict(self):
        """Gather all data into a dictionary with the following structure:

            {
                global: info
                service: { service: info,
                           images: [
                                { image: data }
                            ]
                         }
            }

        Note: values in the dictionary should be of the expected types.
        (DateTime objects, where appropriate, etc)
        """
        data = { 'service': { } }
        for s in sorted(self.service.keys()):
            album = {
                    'id': self.service[s].id,
                    'title': self.service[s].title,
                    'description': self.service[s].description,
                    'date': self.service[s].date,
                    'url': self.service[s].url,
                    'timestamp': datetime.datetime.now(),
                    'images': []
                }

            for i in self.service[s].images:
                album['images'].append(i.dumpDict())

            data['service'][s] = album
        return data

    def dump(self, f):
        """Gather all data into a simple dictionary stucture to provide
            to a storage backend"""
        return self._storage(self).dump(f)

    def dumps(self):
        return self._storage(self).dumps()



class Album(object):
    """Album adaptor base class. Create an subclass of this, as well as the Image class
    to support a new service type.
    """
    service_name = ''

    def __init__(self, id, registry=None):
        self.registry = registry or AlbumRegistry()
        self.id = id
        self.title = None
        self.description = None
        self.date = None
        self.url = None
        self.images = []
        self.registry.service[self.service_name] = self
        self.postinit()

    def postinit(self):
        """Stuff to do by subclasses after __init__ takes place"""
        pass

    def getImages(self):
        """Populate self.images"""
        raise RuntimeError, "getImages not implemented"

    def getAlbumInfo(self):
        """Set the album attributes"""
        raise RuntimeError, "getAlbumInfo not implemented"

    def getAlbum(self):
        """Load album info and list of image objects"""
        self.getAlbumInfo()
        self.getImages()
        return self


