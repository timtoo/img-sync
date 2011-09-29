# test module is intended to be run via nosetests

import os, sys

# remove nose command line arguments before running tests (before Config sees them)
sys.argv = sys.argv[:1]

from album import AlbumRegistry


def test_registry():
    registry = AlbumRegistry()

    # service attribute exists and is empty
    assert(registry.service == {})

    # config object exists
    assert(hasattr(registry, 'config'))

    # dumpDict() method functions, resulting in a dict with service key
    assert(registry.dumpDict().has_key('service'))

    # _storage class is created
    assert(registry._storage)

    # try executing dumps() and see if it returns anything
    assert(registry.dumps())


def test_local():
    import handle_local

    # set path to test data
    path =  os.path.join(os.path.split(__file__)[0], '../tests/local/')

    album = handle_local.LocalAlbum(path)

    # album id is absolute path with trailing slash removed
    assert(album.id == os.path.abspath(path).rstrip('/'))

    # album has registry isntance
    assert(isinstance(album.registry, AlbumRegistry))

    # no images
    assert(len(album.images) == 0)

    # try to execute getAlbum and see if it returns itself
    assert(isinstance(album.getAlbum(), handle_local.LocalAlbum))



