'''htmlentities compatibility

'''

# stdlib
import string
import sys
import unittest

if sys.version_info[0] == 2:
    from htmlentitydefs import codepoint2name, name2codepoint
elif sys.version_info[0] == 3:
    from html.entities import codepoint2name, name2codepoint
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
        f = lambda self: self.assertEqual(func(src), dst)
        f.__name__ = 'test_{}'.format(name)
        setattr(cls, f.__name__, f)




##############################################################################

data_encode_map = (
    ('ascii', string.ascii_letters, string.ascii_letters),
    ('digits', string.digits, string.digits),
    ('punct', string.punctuation, "!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\\]^_`{|}~"),
    ('white', string.whitespace, string.whitespace),
    ('x00_1f', chars.x00_1f, chars.x00_1f),
    ('x80_9f', chars.x80_9f, chars.x80_9f),
    ('xa0_ff', chars.xa0_ff, '&nbsp;&iexcl;&cent;&pound;&curren;&yen;&brvbar;&sect;&uml;&copy;&ordf;&laquo;&not;&shy;&reg;&macr;&deg;&plusmn;&sup2;&sup3;&acute;&micro;&para;&middot;&cedil;&sup1;&ordm;&raquo;&frac14;&frac12;&frac34;&iquest;&Agrave;&Aacute;&Acirc;&Atilde;&Auml;&Aring;&AElig;&Ccedil;&Egrave;&Eacute;&Ecirc;&Euml;&Igrave;&Iacute;&Icirc;&Iuml;&ETH;&Ntilde;&Ograve;&Oacute;&Ocirc;&Otilde;&Ouml;&times;&Oslash;&Ugrave;&Uacute;&Ucirc;&Uuml;&Yacute;&THORN;&szlig;&agrave;&aacute;&acirc;&atilde;&auml;&aring;&aelig;&ccedil;&egrave;&eacute;&ecirc;&euml;&igrave;&iacute;&icirc;&iuml;&eth;&ntilde;&ograve;&oacute;&ocirc;&otilde;&ouml;&divide;&oslash;&ugrave;&uacute;&ucirc;&uuml;&yacute;&thorn;&yuml;'),
)

# warning: htmlentities does not encode characters without a named entity
# ie: code points over 0xff

for name, src, dst in data_encode_map:
    HTMLEntities.create_assert_equal('encode_{}'.format(name), characterentities.encode, src, dst)

HTMLEntities.create_assert_equal(
    'encode_ignore_special_chars',
    lambda s: characterentities.encode(s, False),
    '''<>'"&,''',
    '''<>'"&,''',
)

##############################################################################

ascii_letters_decent = chars['&#41_5b'] + chars['&#61_7b']
ascii_letters_hexent = chars['&#x41_5b'] + chars['&#x61_7b']
ascii_digit_decent = chars['&#30_39']
ascii_digit_hexent = chars['&#x30_39']
ascii_punct_decent = chars['&#21_40'] + chars['&#5b_7e']
ascii_punct_hexent = chars['&#x21_40'] + chars['&#x5b_7e']
ascii_white_decent = chars['&#9_b'] + chars['&#20_20']
ascii_white_hexent = chars['&#x9_b'] + chars['&#x20_20']
x00_x1f_decent = chars['&#00_1f']
x00_x1f_hexent = chars['&#x00_1f']
x80_x9f_decent = chars['&#80_9f']
x80_x9f_hexent = chars['&#x80_9f']
xa0_ff_decent = chars['&#xa0_ff']
xa0_ff_hexent = chars['&#xa0_ff']

# warning: htmlentities does not decode well all known codepoints;
# ie: htmlentities.decode('&lArr;') => &lArr;
know_entities_ref, know_entities = map(
    ''.join,
    zip(*[('&{};'.format(k), unichr(v)) for k, v in name2codepoint.items()])
)

maxunicodeoverflow_dechex = '&#{0};&#x{0:x};'.format(sys.maxunicode + 1)
int32t_dechex = '&#{0};&#x{0:x};'.format((2<<30)-1)
int32t_overflow_dechex = '&#{0};&#x{0:x};'.format(2<<30)
data_decode_map = (
    ('ascii_letters_decent', ascii_letters_decent, ascii_letters_decent),
    ('ascii_letters_hexent', ascii_letters_hexent, ascii_letters_hexent),
    ('ascii_digit_decent', ascii_digit_decent, ascii_digit_decent),
    ('ascii_digit_hexent', ascii_digit_hexent, ascii_digit_hexent),
    ('ascii_punct_decent', ascii_punct_decent, ascii_punct_decent),
    ('ascii_punct_hexent', ascii_punct_hexent, ascii_punct_hexent),
    ('ascii_white_decent', ascii_white_decent, ascii_white_decent),
    ('ascii_white_hexent', ascii_white_hexent, ascii_white_hexent),
    ('x00_x1f_decent', x00_x1f_decent, x00_x1f_decent),
    ('x00_x1f_hexent', x00_x1f_hexent, x00_x1f_hexent),
    ('x80_x9f_decent', x80_x9f_decent, x80_x9f_decent),
    ('x80_x9f_hexent', x80_x9f_hexent, x80_x9f_hexent),
    ('xa0_ff_decent', xa0_ff_decent, xa0_ff_decent),
    ('xa0_ff_hexent', xa0_ff_hexent, xa0_ff_hexent),
    ('known_entities', know_entities_ref, know_entities),
    ('cover_unknown_entity', '&foo;&bar;', '&foo;&bar;'),
    ('cover_unknown_dec', '&#ff;', '&#ff;'),
    ('cover_unknown_hex', '&#xyz;&#xfffffff;', '&#xyz;&#xfffffff;'),
    ('maxunicode', '&#{0};&#x{0:x};'.format(sys.maxunicode), unichr(sys.maxunicode) * 2),
    ('maxunicode_over', maxunicodeoverflow_dechex, maxunicodeoverflow_dechex),
    ('unicode_int32t', int32t_dechex, int32t_dechex),
    ('int32t_overflow', int32t_overflow_dechex, int32t_overflow_dechex),
)

for name, src, dst in data_decode_map:
    HTMLEntities.create_assert_equal('decode_{}'.format(name), characterentities.decode, src, dst)
