'''
This module provides a set of utility classes
'''

class Rect(object):
    '''
    a simple rectangle class plus a list of convenience functions
    '''
    def __init__(self, *args):
        '''
        constructor - try to make sense of the passed args
        '''
        if len(args) == 2:
            self._left = 0
            self._top = 0
            (self._width, self._height) = args
        elif len(args) == 4:
            (self._left, self._top, self._width, self._height) = args
        else:
            raise ValueError('can not understand Rect%s', args)

    @property
    def width(self):
        '''
        produce the width of the rect
        '''
        return self._width

    @property
    def height(self):
        '''
        produce the height of the rect
        '''
        return self._height

    @property
    def size(self):
        '''
        produce the size of the rect
        '''
        return (self._width, self._height)

    @property
    def offset(self):
        '''
        produce the offset of the rect
        '''
        return (self._left, self._top)

    def scaled_to(self, other):
        '''
        scale the given rect to the given other, while maintaining aspect ratio
        '''
        factor = min(other.width / self._width, other.height / self._height)
        return Rect(
            self._left,
            self._top,
            round(self._width * factor),
            round(self._height * factor))

    def centered_in(self, other):
        '''
        produce the offset to center the given rect in self
        '''
        return Rect(
            round((other.width - self._width) / 2),
            round((other.height - self._height) / 2),
            self._width,
            self._height)

    def __repr__(self):
        return 'Rect((%d, %d), (%d, %d))' % (self._left, self._top, self._width, self._height)


class QuitGame(Exception):
    pass
