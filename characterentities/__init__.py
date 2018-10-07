#!/usr/bin/env python
# This file is licensed under the terms of the BSD 3-clause "New" or "Revised" license.
# See the LICENSE file in the root of this repository for complete details.
'''characterentities - converter for SGML characters references

'''

__version__ = '0.2.0dev'

import re
import sys

from characterentities.entities import codepoint2name, name2codepoint

if sys.version_info[0] == 3:
    unichr = chr


class CharacterEntities(object):
    __r_decode = re.compile(r'&#?\w+;')

    @classmethod
    def decode(cls, data):
        '''convert HTML encoded characters to ordinary characters
        :param str data: data to be decoded
        :rtype: str or unicode
        '''
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except (OverflowError, ValueError):
                    pass
            else:
                try:
                    text = unichr(name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text
        return cls.__r_decode.sub(fixup, data)

    @staticmethod
    def encode(data, specialchars=True):
        '''
        :param str data: data to be encoded
        :param bool specialchars: whenether to encode SGML special characters
        :rtype str or unicode:
        '''
        regexp = r'[^\x00-\x9f]'
        if specialchars:
            regexp += r'|[<>"&]'

        def fixup(m):
            o = ord(m.group(0))
            try:
                return '&{};'.format(codepoint2name[o][0])
            except KeyError:
                return '&#x{:x};'.format(o)
        return re.sub(regexp, fixup, data)


encode = CharacterEntities.encode
decode = CharacterEntities.decode
