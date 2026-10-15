"""Tests for build.py.  Run:  python3 -m unittest test_build"""
import csv
import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout

import build

HEADER = build.REQUIRED


def piece(**kw):
    p = {k: '' for k in HEADER}
    p.update(kw)
    return p


class Site:
    """A throwaway copy of the site layout: catalog.csv, pages and image files."""

    def __init__(self, rows, pages, images=()):
        self.dir = tempfile.mkdtemp()
        self.write_catalog(rows)
        for name, html in pages.items():
            self.write(name, html)
        for img in images:
            os.makedirs(os.path.dirname(os.path.join(self.dir, img)), exist_ok=True)
            open(os.path.join(self.dir, img), 'wb').close()

    def write_catalog(self, rows):
        with open(os.path.join(self.dir, 'catalog.csv'), 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, HEADER)
            w.writeheader()
            w.writerows(rows)

    def write(self, name, text):
        with open(os.path.join(self.dir, name), 'w', encoding='utf-8') as fh:
            fh.write(text)

    def read(self, name):
        with open(os.path.join(self.dir, name), encoding='utf-8') as fh:
            return fh.read()

    def run(self, *args):
        old = build.HERE
        build.HERE = self.dir
        out = io.StringIO()
        try:
            with redirect_stdout(out):
                code = build.main(list(args))
        finally:
            build.HERE = old
        return code, out.getvalue()

    def cleanup(self):
        shutil.rmtree(self.dir)


IMGS = ['artworks_full/x/a.jpg', 'artworks_small/x/a.jpg']
A = piece(number='007', title='a title', medium='oil on canvas', dimensions='24"x36"',
          date='may 2024', available='true', **{'img large': 'artworks_full/x/a.jpg'})
PAGE = '<html><body>\n    <div>\n        <figure class="artwork" data-piece="7"></figure>\n    </div>\n</body></html>\n'


class RenderTest(unittest.TestCase):
    def cap(self, p, compact=False):
        html = build.render(p, '', compact, None, False)
        start = html.index('<figcaption>') + len('<figcaption>')
        return ' '.join(html[start:html.index('</figcaption>')].split())

    def test_standard_caption(self):
        self.assertEqual(self.cap(A), '<span class="pink-dot"></span> <cite>a title</cite> <br><br>may 2024 <br>oil on canvas, 24"x36"')

    def test_dots(self):
        self.assertIn('gray-dot', self.cap({**A, 'available': 'false'}))
        self.assertNotIn('-dot', self.cap({**A, 'available': ''}))

    def test_notes_price_and_compact(self):
        c = self.cap({**A, 'notes': 'after x', 'price': '150', 'medium': '', 'dimensions': ''}, compact=True)
        self.assertEqual(c, '<span class="pink-dot"></span> <cite>a title</cite> <br><br>after x <br>may 2024 <br><b>($150)</b><br><br>')

    def test_compact_space_after_can_be_turned_off(self):
        html = build.render({**A, 'medium': '', 'dimensions': ''}, '', True, None, False, space_after=False)
        self.assertIn('<br>may 2024\n', html)

    def test_medium_line_break_instead_of_comma(self):
        self.assertIn('<br>oil on canvas<br>24"x36"', self.cap({**A, 'medium': 'oil on canvas<br>'}))

    def test_title_with_own_cite_is_not_wrapped(self):
        self.assertIn('</span> untitled <cite>(black)</cite>', self.cap({**A, 'title': 'untitled <cite>(black)</cite>'}))

    def test_image_paths_and_options(self):
        html = build.render(A, '  ', False, 'artwork-tall', True)
        self.assertIn('href="viewer.html?img=artworks_full/x/a.jpg"', html)
        self.assertIn('src="artworks_small/x/a.jpg" class="artwork-tall"', html)
        self.assertLess(html.index('<figcaption>'), html.index('<a '))
        html = build.render({**A, 'img small': 'artworks_small/x/thumb.jpg'}, '', False, None, False)
        self.assertIn('src="artworks_small/x/thumb.jpg"', html)
        self.assertLess(html.index('<a '), html.index('<figcaption>'))


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.site = None

    def tearDown(self):
        if self.site:
            self.site.cleanup()

    def make(self, rows=(A,), pages=None, images=IMGS):
        self.site = Site(list(rows), pages or {'page.html': PAGE}, images)
        return self.site

    def test_fills_figure_and_keeps_everything_else(self):
        s = self.make()
        code, out = s.run()
        self.assertEqual(code, 0, out)
        html = s.read('page.html')
        self.assertTrue(html.startswith('<html><body>\n    <div>\n        <figure class="artwork" data-piece="7">'))
        self.assertTrue(html.endswith('</figure>\n    </div>\n</body></html>\n'))
        self.assertIn('<cite>a title</cite>', html)

    def test_idempotent_and_check_mode(self):
        s = self.make()
        self.assertEqual(s.run('--check')[0], 1)          # needs building
        s.run()
        first = s.read('page.html')
        self.assertEqual(s.run()[0], 0)
        self.assertEqual(s.read('page.html'), first)
        self.assertEqual(s.run('--check')[0], 0)          # up to date

    def test_spreadsheet_edit_updates_page(self):
        s = self.make()
        s.run()
        s.write_catalog([{**A, 'title': 'renamed'}])
        s.run()
        html = s.read('page.html')
        self.assertIn('<cite>renamed</cite>', html)
        self.assertNotIn('a title', html)

    def test_number_formats_match(self):
        s = self.make(pages={'page.html': PAGE.replace('data-piece="7"', 'data-piece="007"')})
        self.assertEqual(s.run()[0], 0)

    def test_unknown_number_changes_nothing(self):
        bad = PAGE + '<figure data-piece="999"></figure>\n'
        s = self.make(pages={'page.html': bad, 'other.html': PAGE})
        code, out = s.run()
        self.assertEqual(code, 1)
        self.assertIn('data-piece="999"', out)
        self.assertEqual(s.read('page.html'), bad)
        self.assertEqual(s.read('other.html'), PAGE)      # all-or-nothing

    def test_unclosed_figure_is_an_error_not_a_swallow(self):
        bad = '<figure data-piece="7">\n<figure class="artwork" data-piece="7"></figure>\n'
        s = self.make(pages={'page.html': bad})
        code, out = s.run()
        self.assertEqual(code, 1)
        self.assertIn('line 1: this <figure> has no </figure>', out)
        self.assertEqual(s.read('page.html'), bad)

    def test_single_quotes(self):
        s = self.make(pages={'page.html': "<figure class='artwork' data-piece='7' data-caption='above'></figure>"})
        self.assertEqual(s.run()[0], 0)
        html = s.read('page.html')
        self.assertIn('<cite>a title</cite>', html)
        self.assertLess(html.index('<figcaption>'), html.index('<a '))

    def test_missing_image_changes_nothing(self):
        s = self.make(images=IMGS[:1])
        code, out = s.run()
        self.assertEqual(code, 1)
        self.assertIn('image not found: artworks_small/x/a.jpg', out)
        self.assertEqual(s.read('page.html'), PAGE)

    def test_catalog_validation(self):
        for rows, msg in [
            ([A, A], 'used twice'),
            ([{**A, 'number': 'abc'}], 'not a whole number'),
            ([{**A, 'available': 'maybe'}], 'available must be'),
            ([{**A, 'price': '1 50'}], 'price'),
        ]:
            with self.subTest(msg=msg):
                s = self.make(rows=rows)
                code, out = s.run()
                self.assertEqual(code, 1)
                self.assertIn(msg, out)
                self.assertEqual(s.read('page.html'), PAGE)
                s.cleanup()
                self.site = None

    def test_excel_style_csv(self):
        # Excel: BOM, CRLF line endings, TRUE/FALSE, "$150", leading zeros dropped, blank rows
        s = self.make()
        with open(os.path.join(s.dir, 'catalog.csv'), 'w', encoding='utf-8-sig', newline='') as fh:
            w = csv.DictWriter(fh, HEADER, lineterminator='\r\n')
            w.writeheader()
            w.writerow({**A, 'number': '7', 'available': 'TRUE', 'price': '$150', 'notes': 'line one\nline two'})
            w.writerow({k: '' for k in HEADER})
        code, out = s.run()
        self.assertEqual(code, 0, out)
        html = s.read('page.html')
        self.assertIn('pink-dot', html)
        self.assertIn('<b>($150)</b>', html)
        self.assertIn('line one<br>line two', html)

    def test_missing_column(self):
        s = self.make()
        s.write('catalog.csv', 'number,title\n7,x\n')
        code, out = s.run()
        self.assertEqual(code, 1)
        self.assertIn('missing column', out)

    def test_pages_without_figures_untouched(self):
        s = self.make(pages={'page.html': PAGE, 'plain.html': '<p>hi</p>'})
        s.run()
        self.assertEqual(s.read('plain.html'), '<p>hi</p>')


class RealSiteTest(unittest.TestCase):
    """The committed pages must already match catalog.csv (i.e. someone ran build.py)."""

    def test_site_is_built(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = build.main(['--check'])
        self.assertEqual(code, 0, out.getvalue())


if __name__ == '__main__':
    unittest.main()
