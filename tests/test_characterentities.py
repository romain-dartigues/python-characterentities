'''htmlentities compatibility

'''

# stdlib
import string
import sys
import unittest

if sys.version_info[0] == 2:
    from htmlentitydefs import name2codepoint
elif sys.version_info[0] == 3:
    from html.entities import name2codepoint
    unichr = chr

# local
import characterentities
from . import utils


chars = utils.Chars()


class HTMLEntities(unittest.TestCase):
    @classmethod
    def create_assert_equal(cls, name, func, src, dst):
        '''
        :param cls:
        :param str name:
        :param function func: function which will be applied to "src"
        :param src: source data
        :param dst: expected data after transformation
        '''

        def f(self): return self.assertEqual(func(src), dst)
        f.__name__ = 'test_{}'.format(name)
        setattr(cls, f.__name__, f)

    def test_encode_punct(self):
        encoded = characterentities.encode(string.punctuation)
        self.assertEqual(
            encoded.lower(),
            "!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\\]^_`{|}~"
        )


##############################################################################


data_encode_map = (
    ('ascii', string.ascii_letters, string.ascii_letters),
    ('digits', string.digits, string.digits),
    ('white', string.whitespace, string.whitespace),
    ('x00_1f', chars.x00_1f, chars.x00_1f),
    ('x80_9f', chars.x80_9f, chars.x80_9f),
)

# warning: htmlentities does not encode characters without a named entity
# ie: code points over 0xff

for name, src, dst in data_encode_map:
    HTMLEntities.create_assert_equal('encode_{}'.format(
        name), characterentities.encode, src, dst)

HTMLEntities.create_assert_equal(
    'encode_ignore_special_chars',
    lambda s: characterentities.encode(s, False),
    '''<>'"&,''',
    '''<>'"&,''',
)

##############################################################################

ascii_letters = string.ascii_uppercase + string.ascii_lowercase
ascii_letters_decent = chars['&#41_5a'] + chars['&#61_7a']
ascii_letters_hexent = chars['&#x41_5a'] + chars['&#x61_7a']
ascii_digit_decent = chars['&#30_39']
ascii_digit_hexent = chars['&#x30_39']
ascii_punct_decent = ''.join('&#{};'.format(ord(_)) for _ in string.punctuation)
ascii_punct_hexent = ''.join('&#x{:x};'.format(ord(_)) for _ in string.punctuation)
ascii_white_decent = ''.join('&#{};'.format(ord(_)) for _ in string.whitespace)
ascii_white_hexent = ''.join('&#x{:x};'.format(ord(_)) for _ in string.whitespace)
x00_1f_decent = chars['&#00_1f']
x00_1f_hexent = chars['&#x00_1f']
x00_1f = chars.x00_1f
x80_9f_decent = chars['&#80_9f']
x80_9f_hexent = chars['&#x80_9f']
x80_9f = chars.x80_9f
xa0_ff_decent = chars['&#a0_ff']
xa0_ff_hexent = chars['&#xa0_ff']
xa0_ff = chars.xa0_ff

known_entities_ref, known_entities = map(
    ''.join,
    zip(*[
        ('&{};'.format(k), unichr(v))
        for k, v in name2codepoint.items()
        if k not in {'lang', 'rang'}  # Python maps have an error here
    ])
)

maxunicodeoverflow_dechex = '&#{0};&#x{0:x};'.format(sys.maxunicode + 1)
int32t_dechex = '&#{0};&#x{0:x};'.format((2 << 30) - 1)
int32t_overflow_dechex = '&#{0};&#x{0:x};'.format(2 << 30)
data_decode_map = (
    ('ascii_letters_decent', ascii_letters_decent, ascii_letters),
    ('ascii_letters_hexent', ascii_letters_hexent, ascii_letters),
    ('ascii_digit_decent', ascii_digit_decent, string.digits),
    ('ascii_digit_hexent', ascii_digit_hexent, string.digits),
    ('ascii_punct_decent', ascii_punct_decent, string.punctuation),
    ('ascii_punct_hexent', ascii_punct_hexent, string.punctuation),
    ('ascii_white_decent', ascii_white_decent, string.whitespace),
    ('ascii_white_hexent', ascii_white_hexent, string.whitespace),
    ('x00_1f_decent', x00_1f_decent, x00_1f),
    ('x00_1f_hexent', x00_1f_hexent, x00_1f),
    ('x80_9f_decent', x80_9f_decent, x80_9f),
    ('x80_9f_hexent', x80_9f_hexent, x80_9f),
    ('xa0_ff_decent', xa0_ff_decent, xa0_ff),
    ('xa0_ff_hexent', xa0_ff_hexent, xa0_ff),
    ('known_entities', known_entities_ref, known_entities),
    ('cover_unknown_entity', '&foo;&bar;', '&foo;&bar;'),
    ('cover_unknown_dec', '&#ff;', '&#ff;'),
    ('cover_unknown_hex', '&#xyz;&#xfffffff;', '&#xyz;&#xfffffff;'),
    ('maxunicode', '&#{0};&#x{0:x};'.format(
        sys.maxunicode), unichr(sys.maxunicode) * 2),
    ('maxunicode_over', maxunicodeoverflow_dechex, maxunicodeoverflow_dechex),
    ('unicode_int32t', int32t_dechex, int32t_dechex),
    ('int32t_overflow', int32t_overflow_dechex, int32t_overflow_dechex),
)

for name, src, dst in data_decode_map:
    HTMLEntities.create_assert_equal('decode_{}'.format(
        name), characterentities.decode, src, dst)
