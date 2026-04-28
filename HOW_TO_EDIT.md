# How to Edit This Site

## Adding a New Artwork to an Existing Project

1. **Add your image files:**
   - Put the full-resolution image in `artworks_full/PROJECT_NAME/`
   - Run the resize script (see below) to generate the smaller versions
   - Or manually put a ~2000px version in `artworks/PROJECT_NAME/` and a ~400px version in `artworks_small/PROJECT_NAME/`

2. **Open the project HTML file** (e.g. `grids.html`)

3. **Find one of the two columns** — look for `<!-- Column 1 -->` and `<!-- Column 2 -->` comments in the HTML

4. **Copy this block and paste it into either column:**

```html
<figure class="artwork">
    <a href="viewer.html?img=artworks_full/PROJECT_NAME/your_image.jpg">
        <img loading="lazy" src="artworks_small/PROJECT_NAME/your_image.jpg">
    </a>
    <figcaption>
        <span class="pink-dot"></span> <cite>artwork title</cite>
        <br><br>date
        <br>medium, dimensions
    </figcaption>
</figure>
```

5. **Change these things:**
   - `PROJECT_NAME/your_image.jpg` → your actual folder and filename (appears twice)
     - In the `href`: keep `artworks_full/` prefix (this is the full-res version for zoom)
     - In the `src`: keep `artworks_small/` prefix (this is the small version that loads fast)
   - `artwork title` → the title of the piece
   - `date` → when you made it
   - `medium, dimensions` → e.g. "oil on canvas, 24"x36""
   - `pink-dot` → use `pink-dot` if available for sale, `gray-dot` if not

6. **Save and push to GitHub.** The site updates automatically in about 1-2 minutes.


## Adding a New Project (New Gallery Page)

1. Copy `_template.html` and rename it (e.g. `newproject.html`)

2. Edit the title, description, and date range at the top

3. Add your artworks using the block from step 4 above

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

- `<span class="pink-dot"></span>` = available (pink)
- `<span class="gray-dot"></span>` = not available (gray)

To change the colors, search for `.pink-dot` and `.gray-dot` in `index.css`.
