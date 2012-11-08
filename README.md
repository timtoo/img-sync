IMG-SYNC
========

Synchronize image files between a local file system and remote services.

- maintain as much metadata as possible when syncronizing/uploading (tags, geolocation, etc)
- remember what images have been syncronized to what remote site
- ability to check for/list changed local files since last sync
- update only changed photos (sync!), either locally or remotely
- update only metadata when syncing, if possible, where only metadata has changed
- recursively upload/sync multiple albums with one command
- support multiple remote services

Status
------

Pre-Alpha. Nothing is working. Current focus is as follows:

- target picasaweb/google+ as remote service
- recursive uploader
- detect changes in local files


Command-line tool
-----------------

### General option modifiers ###

    --no-write       # do not write/upload any changes
    --verbose        # show extra information when available
    --interactive    # prompt for confirmation before doing some actions
    --check-all      # use meta and file hashes for comparisons (can be slow)
    --check-meta     # only compare meta data hashes/changes


### Common Usage Options ###

(Options in square brackets are defaults, so not needed to be specified)


`--diff-with local [--sync-from local] <path>`

+ display differences between local file and cache
+ if `--verbose` than display all local info and cache info first
+ `--check-all` the default for local albums
+ if `--check-meta` is specified, then only diff meta data


`--sync-to local [--sync-from local] <path>`

+ this basically upades the local cache
+ if `--verbose`, display the diff first
+ if `--no-write` then don't write the updated the cache
+ if `--interactive` then display `--verbose` info and prompt before writing
+ `--check-all` the default for local albums
+ if `--check-meta` is specified, then only diff meta data


Design
------

- configuration file `config/img-sync.cfg` (relative to HOME directory)
- *album database* is stored in a special file in each folder (`.img-sync.db`)
    - database is plain text for easy viewing/editing if necessary
    - separate database per album to make moving file system folders easy
    - database contains information about album sync state
        - unique identifiers for local files
        - seperate hash identifier for image and metadata
        - what services have been synced and when
        - unique identifiers for matching remote files
- command line tool for scripting
- (possible GUI in future)



