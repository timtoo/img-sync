import os, time, datetime
from album import Album

class LocalAlbum(Album):
    """Represent an album on a local disk. Album ID is the full path."""
    service = 'local'
    def __init__(self, id):
        # remove trailing slash
        super(LocalAlbum, self).__init__(id.rstrip(os.sep))

    def getAlbumInfo(self):
        path = self.id
        if os.path.exists(path):
            self.url = 'file://' + path
            # directory modification time
            self.date = datetime.datetime(*(time.localtime(os.stat(self.id)[8]))[0:6])
            self.description = ''
            # last element in path, with underscores converted to spaces
            self.title = os.path.split(path)[-1].strip(os.sep).replace('_', ' ')

            print self.id
            print self.title

        else:
            raise ValueError, "Album path does not exist: %s" % self.id

    def getPhotos(self):
        return []

if __name__ == '__main__':
    import config
    c = config.Config()

    a = LocalAlbum(c['source'][0])
    data = a.getAlbum()
    print a.dumps()




