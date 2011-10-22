import datetime

from storage import LocalFileStorage
from config import Config
from image import Image


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

    def loadDict(self, data):
        """Load object data from config dictionary"""
        # need to load the particular proper album/image object for the service type
        # means we need a registry somewhere mapping objects to service name - or else rely on name convention and make them accessable somewhere.
        for service_name in data['service'].keys():

            if not self.service.has_key(service_name):
                self.service[service_name] = ServicePlugin.createAlbum(service_name, data[service_name]['id'])
            service = self.service[service_name]
            service.title = data['service'][service_name]['title']
            service.description = data['service'][service_name]['description']
            service.date = data['service'][service_name]['date']
            service.url = data['service'][service_name]['url']
            service.timestamp = data['service'][service_name]['timestamp']
            service.images = []

            for idata in data['service'][service_name]['images']:
                image = ServicePlugin.createImage(service_name, idata['id'])
                image.loadDict(idata)
                service.images.append(image)

        return self










    def dump(self):
        """Gather all data into a simple dictionary stucture to provide
            to a storage backend"""
        return self._storage(self).dump()

    def dumps(self):
        return self._storage(self).dumps()

    def load(self):
        """load stored config(s)"""
        data = self._storage(self).load()


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


import os
import inspect
class ServicePlugin(object):

    _service = {}

    _path = os.path.abspath(os.path.dirname(__file__))
    handlers = [ os.path.split(x)[-1].split('.')[0][7:] for x in os.listdir(_path) if os.path.split(x)[-1].startswith('handle_') ]

    @staticmethod
    def load():
        for h in ServicePlugin.handlers:
            ServicePlugin._service[h] = {
                'album': None,
                'image': None,
                }
            module = __import__('handle_'+h, globals(), locals())
            for o in dir(module):
                if inspect.isclass(getattr(module, o)):
                    if issubclass(getattr(module, o), Album):
                        ServicePlugin._service[h]['album'] = getattr(module, o)
                    elif issubclass(getattr(module, o), Image):
                        ServicePlugin._service[h]['image'] = getattr(module, o)


    @staticmethod
    def createAlbum(service_name, *arg, **kw):
        """Return an Album instance for the given service"""
        if ServicePlugin.service.has_key(service_name):
            return ServicePlugin._service[service_name]['album'](*arg, **kw)

    @staticmethod
    def createImage(service_name, *arg, **kw):
        """Return an Image instance for the given service"""
        if ServicePlugin._service.has_key(service_name):
            return ServicePlugin._service[service_name]['image'](*arg, **kw)


ServicePlugin.load()



