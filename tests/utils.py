'''
'''

import re



class Chars(object):
    '''generate strings based on hexadecimal patterns (inclusives)

    Example::

       >>> chars = Chars()
       >>> chars.x30_39
       '0123456789'
       >>> chars['x30_39']
       '0123456789'
       >>> chars['&#00_03']
       '&#0;&#1;&#2;&#3;'
       >>> chars['&#x00_03']
       '&#x0;&#x1;&#x2;&#x3;'
    '''
    __r_valid_attr = re.compile(r'^(&#x?|x)([a-z0-f]+)_([a-z0-f]+)$')

    @staticmethod
    def chars(start, stop):
        return ''.join(map(chr, range(start, stop + 1)))

    @staticmethod
    def decent(start, stop):
        '''decimal entity
        '''
        return ''.join(map('&#{};'.format, range(start, stop + 1)))

    @staticmethod
    def hexent(start, stop):
        '''hexadecimal entity
        '''
        return ''.join(map('&#x{:x};'.format, range(start, stop + 1)))

    def __getattr__(self, name):
        m = self.__r_valid_attr.match(name)
        if not m:
            return m
        start = int(m.group(2), 16)
        stop = int(m.group(3), 16)
        return self._to[m.group(1)](start, stop)

    __getitem__ = __getattr__

    _to = {
        'x': chars.__func__,
        '&#': decent.__func__,
        '&#x': hexent.__func__,
    }
