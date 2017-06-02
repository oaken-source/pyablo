'''
This module provides game resource handling used by pyablo
'''

import mpq


ERROR_UNITIALIZED = 'Resources.open called, but resource store uninitialized.'


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
        try:
            return cls._mpq.open(resource)
        except AttributeError as ex:
            raise ValueError(ERROR_UNITIALIZED) from ex
