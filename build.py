#!/usr/bin/env python3
"""Fill in artworks on the gallery pages from catalog.csv.

In any page, write an empty figure with the piece's number:

    <figure class="artwork artwork-vert" data-piece="134"></figure>

then run (in Terminal, inside this folder):

    python3 build.py

and every figure with a data-piece number gets its image link and caption
filled in from that row of catalog.csv. Running it again is always safe:
it rewrites those figures from the spreadsheet and touches nothing else.

Options on the <figure> (all optional):
    data-caption="above"         caption above the image instead of below
    data-img-class="artwork-tall" class to put on the <img> (used on grids)
    data-space-after="none"      on a compact page, no extra space after the caption

Options on the <body> (optional):
    data-caption-style="compact" one line break before the date instead of two,
                                 plus space after each caption (panels page)

    python3 build.py --check     report what would change, write nothing
"""
import csv
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = 'catalog.csv'
REQUIRED = ['number', 'title', 'medium', 'dimensions', 'date', 'price',
            'available', 'notes', 'page', 'img large', 'img small']
TRUE = {'true', 'yes', 'y', '1'}
FALSE = {'false', 'no', 'n', '0'}

FIGURE = re.compile(
    r'<figure(?P<attrs>[^>]*\bdata-piece=(?P<q>["\'])(?P<num>.*?)(?P=q)[^>]*)>(?P<body>.*?)</figure>',
    re.S)
NOTICE = '<!-- filled in from catalog.csv by build.py: edit the spreadsheet, not this -->'


class CatalogError(Exception):
    pass


def attr(attrs, name):
    m = re.search(r'\b%s=(["\'])(.*?)\1' % re.escape(name), attrs)
    return m.group(2) if m else None


def cell(row, key):
    # spreadsheet line breaks (alt-enter in a cell) become HTML line breaks
    return (row.get(key) or '').strip().replace('\r\n', '\n').replace('\n', '<br>')


def load_catalog(path):
    with open(path, newline='', encoding='utf-8-sig') as fh:   # -sig: Excel adds a BOM
        reader = csv.DictReader(fh)
        header = [h.strip() for h in (reader.fieldnames or [])]
        missing = [c for c in REQUIRED if c not in header]
        if missing:
            raise CatalogError('%s is missing column(s): %s' % (path, ', '.join(missing)))
        reader.fieldnames = header
        pieces, errors = {}, []
        for line, row in enumerate(reader, start=2):
            if not any((v or '').strip() for v in row.values()):
                continue                                   # blank row
            raw = (row.get('number') or '').strip()
            if not raw.isdigit():
                errors.append('row %d: number "%s" is not a whole number' % (line, raw))
                continue
            num = int(raw)                                 # "007", "07" and "7" are the same piece
            if num in pieces:
                errors.append('row %d: number %03d is used twice' % (line, num))
                continue
            avail = cell(row, 'available').lower()
            if avail not in TRUE | FALSE | {''}:
                errors.append('row %d: available must be true, false or blank, not "%s"' % (line, avail))
            price = cell(row, 'price').lstrip('$').strip()
            if price and not re.fullmatch(r'\d+(\.\d\d)?', price):
                errors.append('row %d: price "%s" should be a plain number like 150' % (line, price))
            row = {k: cell(row, k) for k in REQUIRED}
            row['price'], row['available'] = price, avail
            pieces[num] = row
        if errors:
            raise CatalogError('\n'.join(errors))
        return pieces


def render(piece, indent, compact, img_class, above, space_after=True):
    i1, i2 = indent + '    ', indent + '        '
    large = piece['img large']
    small = piece['img small'] or large.replace('artworks_full/', 'artworks_small/', 1)
    cls = ' class="%s"' % img_class if img_class else ''
    link = [i1 + '<a href="viewer.html?img=%s">' % large,
            i2 + '<img loading="lazy" src="%s"%s>' % (small, cls),
            i1 + '</a>']

    title = piece['title']
    avail = piece['available']
    dot = ('<span class="pink-dot"></span> ' if avail in TRUE else
           '<span class="gray-dot"></span> ' if avail in FALSE else '')
    lines = [dot + (title if '<cite>' in title else '<cite>%s</cite>' % title)]
    if piece['notes']:
        lines.append('<br><br>' + piece['notes'])
    if piece['date']:
        lines.append(('<br>' if compact else '<br><br>') + piece['date'])
    medium, dims = piece['medium'], piece['dimensions']
    if medium or dims:
        sep = ', ' if medium and dims and not medium.endswith('<br>') else ''
        lines.append('<br>' + medium + sep + dims)
    if piece['price']:
        lines.append('<br><b>($%s)</b>' % piece['price'])
    if compact and space_after:
        lines[-1] += '<br><br>'
    caption = [i1 + '<figcaption>'] + [i2 + l for l in lines] + [i1 + '</figcaption>']

    parts = caption + link if above else link + caption
    return '\n' + i1 + NOTICE + '\n' + '\n'.join(parts) + '\n' + indent


def build_page(html, pieces, filename):
    body = re.search(r'<body([^>]*)>', html)
    compact = bool(body) and attr(body.group(1), 'data-caption-style') == 'compact'
    errors, used = [], []

    def fill(m):
        raw = m.group('num').strip()
        line = html.count('\n', 0, m.start()) + 1
        if '<figure' in m.group('body'):
            errors.append('%s line %d: this <figure> has no </figure> after it' % (filename, line))
            return m.group(0)
        if not raw.isdigit() or int(raw) not in pieces:
            errors.append('%s line %d: data-piece="%s", but there is no piece %s in %s' % (filename, line, raw, raw, CATALOG))
            return m.group(0)
        piece = pieces[int(raw)]
        if not piece['img large']:
            errors.append('%s line %d: piece %s has no "img large" in %s' % (filename, line, raw, CATALOG))
            return m.group(0)
        start = html.rfind('\n', 0, m.start()) + 1
        indent = re.match(r'[ \t]*', html[start:m.start()]).group(0)
        attrs = m.group('attrs')
        used.append(int(raw))
        return '<figure%s>%s</figure>' % (attrs, render(
            piece, indent, compact, attr(attrs, 'data-img-class'), attr(attrs, 'data-caption') == 'above',
            attr(attrs, 'data-space-after') != 'none'))

    out = FIGURE.sub(fill, html)
    return out, errors, used


def missing_images(pieces, used, root):
    errors = []
    for num in sorted(set(used)):
        p = pieces[num]
        small = p['img small'] or p['img large'].replace('artworks_full/', 'artworks_small/', 1)
        for path in (p['img large'], small):
            if not os.path.isfile(os.path.join(root, path)):
                errors.append('piece %03d: image not found: %s' % (num, path))
    return errors


def main(argv):
    check = '--check' in argv
    root = HERE
    try:
        pieces = load_catalog(os.path.join(root, CATALOG))
    except CatalogError as e:
        print('Problem in %s, nothing was changed:\n%s' % (CATALOG, e))
        return 1

    results, errors, used = {}, [], []
    for path in sorted(glob.glob(os.path.join(root, '*.html'))):
        with open(path, encoding='utf-8') as fh:
            html = fh.read()
        out, errs, nums = build_page(html, pieces, os.path.basename(path))
        errors += errs
        used += nums
        if out != html:
            results[path] = out
    errors += missing_images(pieces, used, root)
    if errors:
        print('Problems found, nothing was changed:\n' + '\n'.join(errors))
        return 1

    if check:
        for path in results:
            print('would update', os.path.basename(path))
        return 1 if results else 0
    for path, out in results.items():          # only write once everything checked out
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(out)
    print('Filled %d artworks. Updated: %s' % (
        len(used), ', '.join(os.path.basename(p) for p in results) or 'nothing, already up to date'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
