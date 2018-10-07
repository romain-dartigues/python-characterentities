#!/usr/bin/env python
# vim:set fileencoding=utf8 ts=4 sw=4 ai et:
'''generate charref database from W3C HTML5 charref
'''

# stdlib
import logging
import optparse
import sys

if sys.version_info[0] == 2:
    from urllib2 import urlopen
elif sys.version_info[0] == 3:
    from urllib.request import urlopen
    unichr = chr


# dependencies
try:
    import html5_parser
    parse_html5 = lambda fobj: html5_parser.parse(fobj.read())
except ImportError:
    import html5lib
    parse_html5 = lambda fobj: html5lib.parse(fobj, treebuilder="lxml", namespaceHTMLElements=False)


##############################################################################

STRIP = {
    'hex': lambda v:int(v[3:-1], 16),
    'dec': lambda v:int(v[2:-1]),
    'named': lambda v:[_[1:-1] for _ in v.split()],
    'desc': lambda v:v.rstrip(),
    'character': lambda v:v[1:],
}


python_header = """#!/usr/bin/env python
'''entities tables (auto-generated)
'''
"""

python_footer = '''
codepoint2name = {}
for k, v in name2codepoint.items():
    if v not in codepoint2name: codepoint2name[v] = []
    codepoint2name[v]+= [k]
del k, v
'''

def to_python(table, writer, header=python_header, footer=python_footer):
    '''
    :param table: result of :func:`extract`
    :param file writer:
    :param str header:
    :param str footer:
    :rtype: None
    '''
    data = [header]
    data+= ['\n' * 3]
    data+= ['name2codepoint = {\n']
    data+= [
        '    {!r}: {},\n'.format(name, row['dec'])
        for k, row in table.items()
        for name in row['named']
    ]
    data+= ['}']
    data+= ['\n' * 3]
    data+= [footer]
    writer.writelines(data)


def main(args=None):
    parser = optparse.OptionParser()
    parser.add_option('-q', '--quiet', action='store_const', const=0, dest='verbose')
    parser.add_option('-v', '--verbose', action='count', default=2)

    parser.add_option('-i', '--input',
        default='https://dev.w3.org/html5/html-author/charref',
        help='input source (default: %default)')

    opt, args = parser.parse_args()
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        datefmt='%F %T',
        level=min(max(logging.CRITICAL - (opt.verbose * 10), logging.DEBUG), logging.CRITICAL)
    )

    fobj = urlopen(opt.input)
    document = parse_html5(fobj)
    table = extract(document)

    to_python(table, sys.stdout)
    return 0



def extract(etree):
    '''
    :param etree: result of meth:`html5_parser.parse` or :meth:`html5lib.parse`
    :rtype: dict(dict)
    :return: a dict where the key is the character and the value is a row
        containing the keys: ``dec`` (decimal value of the point),
        ``desc`` (textual description), ``named`` (the entity names)
    '''
    table = {}
    for tr in etree.xpath('//tr'):
        row = {}
        for td in tr:
            key = td.get('class')
            val = STRIP[key](
                td.text
                if key in {'character', 'desc'}
                else td[0].text
            )
            row[key] = val
        if not row['hex'] == row['dec'] == ord(row['character']):
            raise AssertionError(row)
        table[ row['character'] ] = {
            'desc': row['desc'],
            'named': row['named'],
            'dec': row['dec'],
        }
    return table


if __name__ == '__main__':
    main()
