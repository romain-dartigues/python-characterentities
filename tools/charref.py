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


DUMPER = {
    'json': {
        'opts': {
            'indent': 2,
            'sort_keys': True,
        },
    },
    'yaml': {
        'dump': 'safe_dump',
        'opts': {
            'default_flow_style': False,
            'explicit_start': True,
            'explicit_end': True,
        },
    },
}



def get_dumper(name):
    conf = DUMPER.get(name, {})
    dumper = getattr(__import__(name), conf.get('dump', 'dumps'))
    if 'opts' in conf:
        return lambda o: dumper(o, **conf['opts'])
    return dumper


def main():
    FORMATS = (
        'json',
        'msgpack',
        'yaml',
    )
    parser = optparse.OptionParser()
    parser.add_option('-q', '--quiet', action='store_const', const=0, dest='verbose')
    parser.add_option('-v', '--verbose', action='count', default=2)
    parser.add_option('-m', '--man', action='store_true')
    parser.add_option('-f', '--format', choices=FORMATS, default='json',
        help='output format (possible: {}, default: %default)'.format(', '.join(FORMATS)))

    opt, args = parser.parse_args()
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        datefmt='%F %T',
        level=min(max(logging.CRITICAL - (opt.verbose * 10), logging.DEBUG), logging.CRITICAL)
    )

    if opt.man:
        help(__name__)
        return 0

    dumper = get_dumper(opt.format)

    fobj = fetch(
        'https://dev.w3.org/html5/html-author/charref',
        '/tmp/charref',
    )
    document = parse_html5(fobj)
    table = extract(document)

    sys.stdout.write(dumper(table))



def fetch(src, dst, force=False):
    '''
    :param str src: URL to fetch
    :param str dst: output for cache
    :param bool force: force download
    :rtype: file
    '''
    return open('charref')



def extract(etree):
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
