import datetime

from storage import LocalFileStorage
from config import Config

class AlbumRegistry(object):
    """A singleton intended for all Album instances to share

    It collects all of the album instances and provides methods that act on
    all existing Album instances.

    This class is created automatically if it doesn't already exist when
    instantiating an Album.

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

    def dump(self):
        """Gather all data into a simple dictionary stucture to provide
            to a storage backend"""
        return self._storage(self).dump()

    def dumps(self):
        return self._storage(self).dumps()

    def load(self, f):
        """load stored config(s)"""
        return self._storage(self).load()

    def loads(self):
        return self._storage(self).loads()



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
        """Populate self.imagesi and call self.setAll() on each"""
        raise RuntimeError, "getImages not implemented"

    def getAlbumInfo(self):
        """Set the album attributes"""
        raise RuntimeError, "getAlbumInfo not implemented"

    def getAlbum(self):
        """Load album info and list of image objects"""
        self.getAlbumInfo()
        self.getImages()
        return self

    def lookupImage(self, key, val):
        """Iterate self.images and return image with given value on key"""
        for i in self.images:
            if getattr(i, key, None):
                return i
        return None

    def diffAlbum(self, album):
        """Return dictionary of differences.

            the "images" key will contain a dictionary
            with the keys:

                - different (contining list of
                    image objects from this album with differences),
                - same (containing images which match up),
                - new (containing images not found in this album),
                - unknown (images in this album which are not
                    in the source album)

        """

    def createAlbum(self, album):
        """Given an album object create/update album on this service
        """

    def exists(self):
        """Return boolean result to a check whether this album
            yet physically exists
        """
        raise RuntimeError, "exists not implemented"




