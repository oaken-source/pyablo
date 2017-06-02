'''
This module provides game resource handling used by pyablo
'''

import mpq


_ERROR_UNITIALIZED = 'Resources.open called, but resource store uninitialized.'


_NAMED_RESOURCES = {
    'intro_logos.smk':          'File00002910.smk',
    'intro_cinematic.smk':      'File00001475.smk',
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
        cls._mpq = mpq.MPQFile(path)

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
