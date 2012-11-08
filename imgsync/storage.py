import datetime
import cStringIO as StringIO
import ConfigParser
import os
import json

class Storage(object):
    """Encapsulate dumping/loading of persistent (cached) album data"""
    def __init__(self, album):
        """Pass in the album object to dump data from or load data to

        Note: in the future the album object collect all data and
        pass it in as a simple dictionary, to make writing storage backends
        easier.
        """
        self.album = album

    def dump(self, handle=None):
        """Given a file handle or some other I/O object, dump the data
        to it if needed"""
        raise RuntimeError, "No implemented"

    def dumps(self):
        """Return dumped data as a string"""
        raise RuntimeError, "No implemented"

    def load(self, handle=None):
        """Given a file handle or some other I/O object, load data into
        album object if needed"""
        raise RuntimeError, "No implemented"

    def loads(self):
        """Load config file from a string"""
        raise RuntimeError, "No implemented"



class LocalFileStorage(Storage):
    """Use ConfigParser to create config file to store in local directory"""
    CONFIG_VERSION = "1.0"
    FILENAME = '.img-sync-album.db'

    @property
    def filename(self):
        path = self.album.service['local'].id
        return path + os.sep + self.FILENAME

    def exists(self):
        return os.path.exists(self.filename)

    def _addVal(self, config, section, data, key):
        if data.get(key):
            if isinstance(data[key], (tuple, list)):
                config.set(section, key, json.dumps(data[key]))
            else:
                config.set(section, key, data[key] or '')

    def _dumpImage(self, config, section, image):
        """Dump image data data to a config file"""
        config.set(section, 'id', image['id'])
        config.set(section, 'hash', image['hash'])
        config.set(section, 'meta', image['meta'])
        for k in ('filename', 'title', 'description', 'timestamp',
                'original', 'size', 'geocode'):
            self._addVal(config, section, image, k)
        config.set(section, 'tags', json.dumps(image.get('tags', [])))

    def _dump(self, f=None):
        """Write out the album to storage
        """
        data = self.album.dumpDict()

        config = ConfigParser.ConfigParser()
        config.add_section('global')
        config.set('global', 'service', ', '.join(sorted(data['service'].keys())))
        config.set('global', 'config', self.CONFIG_VERSION)

        for s in sorted(data['service'].keys()):
            album = data['service'][s]

            config.add_section(s)

            config.set(s, 'id', album['id'])
            config.set(s, 'title', album['title'])
            config.set(s, 'description', album['description'])
            config.set(s, 'date', album['date'])
            config.set(s, 'url', album['url'])
            config.set(s, 'count', len(album['images']))
            config.set(s, 'config', self.CONFIG_VERSION)
            config.set(s, 'timestamp', datetime.datetime.now())

            for i in range(len(album['images'])):
                section = s+'-image-' + str(i+1)
                config.add_section(section)
                self._dumpImage(config, section,
                        album['images'][i])

        if f is None:
            f = open(self.filename, 'w')
        config.write(f)
        return f

    def dump(self):
        return self._dump()

    def dumps(self):
        f = StringIO.StringIO()
        self._dump(f)
        return f.getvalue()

    def _sectionToDict(self, config, section, data):
        """Read a ConfigFile section and store info in dict"""
        for k, v in config.items(section):
            if k in ('timestamp', 'original'):
                if '.' in v:
                    v = datetime.datetime.strptime(v,
                            '%Y-%m-%d %H:%M:%S.%f')
                else:
                    v = datetime.datetime.strptime(v,
                            '%Y-%m-%d %H:%M:%S')
            elif k in ('count', 'size'):
                v = int(v)
            elif k in ('geocode',):
                v = json.loads(v)
            elif k in ('tags',):
                v = json.loads(v)
            data[k] = v
        return data

    def load(self):
        """
        """
        data = { 'service': {} }
        if self.exists():
            config = ConfigParser.ConfigParser()
            config.read([self.filename])
            data['config'] = config.get('global', 'config')
            service = config.get('global', 'service')
            service = [ x.strip() for x in service.split(',') if x.strip() ]
            for s in service:
                data['service'][s] = { 'images': [] }
                self._sectionToDict(config, s, data['service'][s])
                if data['service'][s].get('count'):
                    for i in range(data['service'][s]['count']):
                        photo = {}
                        self._sectionToDict(config, s+'-image-'+str(i+1),
                                photo)
                        data['service'][s]['images'].append(photo)

        return self.album.loadDict(data)



