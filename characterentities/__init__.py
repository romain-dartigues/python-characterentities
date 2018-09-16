#!/usr/bin/env python
# This file is licensed under the terms of the BSD 3-clause "New" or "Revised" license.
# See the LICENSE file in the root of this repository for complete details.
'''characterentities - converter for SGML characters references

'''

__version__ = '0.1.1dev'

import re
import sys

if sys.version_info[0] == 2:
    from htmlentitydefs import codepoint2name, name2codepoint
elif sys.version_info[0] == 3:
    from html.entities import codepoint2name, name2codepoint
    unichr = chr


class CharacterEntities(object):
    __r_decode = re.compile(r'&(' + r'|'.join(name2codepoint) + r');')
    @classmethod
    def decode(cls, data):
        '''convert HTML encoded characters to ordinary characters
        :param str data: data to be decoded
        :rtype: str
        '''
        def fixup(m):
            return unichr(name2codepoint[m.group(1)])
        return cls.__r_decode.sub(fixup, data)

    @staticmethod
    def encode(data, specialchars=True):
        '''
        :param str data: data to be encoded
        :param bool specialchars: whenether to encode SGML special characters
        :rtype str:
        '''
        regexp = r'[^\x00-\x9f]'
        if specialchars:
            regexp += r'|[<>"&]'
        def fixup(m):
            o = ord(m.group(0))
            try:
                return '&{};'.format(codepoint2name[o])
            except KeyError:
                return '&#x{:x};'.format(o)
        return re.sub(regexp, fixup, data)


_ce = CharacterEntities()
encode = _ce.encode
decode = _ce.decode
