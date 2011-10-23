import datetime

from storage import LocalFileStorage
from config import Config
from image import Image
from album import Album


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

    def register(self, service_name, albumid, *arg, **kw):
        """Create an album object for the specified service.
        Returns self (registry object), as well as album object for convenience."""
        self.service[service_name] = ServicePlugin.createAlbum(service_name, albumid, *arg, **kw)
        return self, self.service[service_name]

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
    def createAlbum(service_name, albumid, *arg, **kw):
        """Return an Album instance for the given service"""
        if ServicePlugin._service.has_key(service_name):
            return ServicePlugin._service[service_name]['album'](albumid, *arg, **kw)

    @staticmethod
    def createImage(service_name, imageid, *arg, **kw):
        """Return an Image instance for the given service"""
        if ServicePlugin._service.has_key(service_name):
            return ServicePlugin._service[service_name]['image'](imageid, *arg, **kw)


ServicePlugin.load()



