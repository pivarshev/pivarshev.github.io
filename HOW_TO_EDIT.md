# How to Edit This Site

## The Catalog (catalog.csv)

Every artwork has one row in `catalog.csv`, with its own number. The pages
don't hold any titles or captions themselves. They just say *which* number
goes where, and `build.py` fills in the rest from the spreadsheet.

Open `catalog.csv` in Excel, Numbers or Google Sheets. The columns:

| column | what goes in it | example |
|---|---|---|
| number | the piece's unique number | `134` |
| title | the title (shown in italics) | `untitled demo 1` |
| medium | what it's made of | `oil on canvas` |
| dimensions | size | `30"x40"` |
| date | when you made it | `may 2025` |
| price | price in dollars, or blank | `150` |
| available | `true` = pink dot, `false` = gray dot, blank = no dot | `true` |
| notes | extra line(s) under the title, e.g. `after giambologna, 1583` | |
| page | which project it belongs to (just for your reference) | `recreations` |
| img large | the full-size image file | `artworks_full/recreations/demo.jpg` |
| img small | the small version, **only if its name is different** (leave blank otherwise) | |

Notes:
- You can use HTML in any text cell, e.g. `<br>` for a line break (a line break typed
  inside the cell works too).
- To put the dimensions on their own line instead of after a comma, end the medium with `<br>`.
- Leading zeros don't matter: `7`, `07` and `007` are the same piece.
- **Save it as CSV** (Excel: *File > Save As > CSV UTF-8*; Numbers: *File > Export To > CSV*;
  Google Sheets: *File > Download > CSV*, then replace `catalog.csv` with the download).


## Adding a New Artwork

1. **Add your image files:**
   - Put the full-resolution image in `artworks_full/PROJECT_NAME/`
   - Run the resize script (see below) to generate the smaller versions

2. **Add a row to `catalog.csv`** with a new number, and fill in the title, date, etc.
   For `img large`, put the path to the full image, e.g. `artworks_full/grids/new.jpg`.

3. **Open the project HTML file** (e.g. `grids.html`), find where you want it, and add one line:

```html
<figure class="artwork" data-piece="134"></figure>
```

   Keep the layout classes you like (`artwork-horiz`, `artwork-vert`, etc.) on the figure.
   Two optional extras:
   - `data-caption="above"` puts the caption above the picture
   - `data-img-class="artwork-tall"` adds a class to the picture (used on the grids page)

4. **Run the build** in Terminal, inside this folder:

```
python3 build.py
```

   It fills in every `data-piece` figure on every page. If something's wrong (a number
   that isn't in the catalog, an image file that doesn't exist, a typo in `available`)
   it tells you exactly where and **changes nothing**, so it's always safe to run.

5. **Save and push to GitHub.** The site updates automatically in about 1-2 minutes.

**Changing an existing piece** (sold it, new price, fixed a typo): edit its row in
`catalog.csv`, run `python3 build.py`, push. Every page showing it updates.

**Moving a piece** to a different spot or page: move its `<figure ... data-piece="N">` line.

Don't edit the caption HTML inside a filled-in figure. It gets rewritten from
the spreadsheet the next time you build.


## Adding a New Project (New Gallery Page)

1. Copy `_template.html` and rename it (e.g. `newproject.html`)

2. Edit the title, description, and date range at the top

3. Add your artworks with `data-piece` lines (see "Adding a New Artwork" above), then run `python3 build.py`

4. Add a link to the new page on the homepage:
   - **Desktop grid** (`index.html`): add a `<div class="grid-item">` in the `grid-container` nav
   - **Mobile list** (`index.html`): add a `<li><a href="newproject.html">...</a></li>` in the `bio-links` nav


## Resizing Images

After adding full-res images to `artworks_full/`, run this in Terminal:

```
cd /path/to/pivarshev.github.io
bash resize.sh
```

This creates the medium (~2000px) and small (~400px) versions automatically.


## Changing Colors

Open `index.css` and edit the variables at the very top:

```css
:root {
    --bg: #eee;           /* page background */
    --bg-bio: #eee;       /* sidebar background, grid squares */
    --bg-content: #fff;   /* gallery background, homepage right side */
    --text: #333;         /* main text color */
    --text-light: #555;   /* "hi, i'm pj" text */
    --text-link: #666;    /* link color */
    --hover-bg: #ddd;     /* hover background on links and grid squares */
}
```

For dark mode, edit the `[data-theme="dark"]` section right below it.


## Changing Fonts, Sizes, Alignment

See the **CHEAT SHEET** at the very top of `index.css` — it tells you exactly which line to edit for each thing (title size, description alignment, sidebar width, etc.)


## Available / Not Available Dots

These come from the `available` column in `catalog.csv`:

- `true` = available (pink)
- `false` = not available (gray)
- blank = no dot

To change the colors, search for `.pink-dot` and `.gray-dot` in `index.css`.
