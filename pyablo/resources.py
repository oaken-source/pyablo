'''
This module provides game resource handling used by pyablo
'''

import mpq


_ERROR_UNITIALIZED = 'Resources.open called, but resource store uninitialized.'
_ERROR_OPEN_FAILED = 'unable to open resources file - incomplete installation?'


_NAMED_RESOURCES = {
    # video files
    'intro_logos.smk':          'File00002910.smk',
    'intro_cinematic.smk':      'File00001475.smk',
    # image files
    'intro_splash.pcx':         'File00000000.pcx',
}


class Resources(object):
    '''
    Resource management static class
    '''
    _mpq = None

    @classmethod
    def init(cls, path):
        '''
        Load the game resources from the mpq file
        '''
        try:
            cls._mpq = mpq.MPQFile(path)
        except OSError as ex:
            raise OSError(_ERROR_OPEN_FAILED) from ex

    @classmethod
    def open(cls, resource):
        '''
        return the queried resource
        '''
        if resource in _NAMED_RESOURCES:
            resource = _NAMED_RESOURCES[resource]

        try:
            return cls._mpq.open(resource)
        except AttributeError as ex:
            raise ValueError(_ERROR_UNITIALIZED) from ex
