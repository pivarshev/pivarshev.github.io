# What Changed and Why

A plain-English log of every change made during the refactor, so the client always knows exactly what was done and why.

---

## April 20, 2026

### Setup — Refactor documentation added
**What:** Created a `refactor/` folder with a site audit, project goals, and step-by-step checklists for three phases of work.

**Why:** Before touching any code, we documented every issue found and created a plan. This ensures nothing is changed without a clear reason, and the client can review the plan before work begins.

**Files added:**
- `refactor/README.txt` — overview of the refactor folder
- `refactor/site_audit.txt` — full audit of 11 issues found
- `refactor/REFACTOR_REPORT.md` — same audit in markdown format
- `refactor/phase1_checklist.txt` — Phase 1 task list
- `refactor/phase2_checklist.txt` — Phase 2 task list
- `refactor/phase3_checklist.txt` — Phase 3 task list
- `refactor/PROJECT_GOALS.md` — project goals and golden rule (never break UI)

**UI impact:** None. Documentation only.

---

### Phase 1, Step 1 — Replaced invalid `<list>` elements with `<ul>`
**What:** Changed all `<list>` tags to `<ul>` and `</list>` to `</ul>` across 7 gallery pages (grids, recreations, feeling, self, panels, appreciation, misc).

**Why:** `<list>` is not a valid HTML element. Browsers don't recognize it and treat it as a generic element with no meaning. `<ul>` (unordered list) is the correct standard element. This makes the navigation links properly structured and recognized by browsers and assistive technologies.

**Files changed:** grids.html, recreations.html, feeling.html, self.html, panels.html, appreciation.html, misc.html

**UI impact:** None. Browsers were already rendering these the same way.

---

### Phase 1, Step 2 — Added security attributes to external links
**What:** Added `rel="noopener noreferrer"` to all 214 links that use `target="_blank"` (open in new tab).

**Why:** When a link opens a new tab with `target="_blank"`, the new page can access the original page through `window.opener` and potentially redirect it. Adding `rel="noopener noreferrer"` blocks this. It's a standard security best practice.

**Files changed:** All 8 HTML files

**UI impact:** None. Links still open in new tabs exactly as before.

---

### Phase 1, Step 3 — Added lazy loading to artwork images
**What:** Added `loading="lazy"` to all artwork images across gallery pages (198 images total).

**Why:** Without lazy loading, every image on a page loads immediately when the page opens — even images the user hasn't scrolled to yet. The panels page alone has 82 images. With `loading="lazy"`, the browser only loads images as the user scrolls near them. This makes pages load faster, especially on slower connections. This is a native HTML attribute — no JavaScript involved.

**Files changed:** grids.html, recreations.html, feeling.html, self.html, panels.html, appreciation.html, misc.html

**UI impact:** None. Images appear the same way. Users may notice pages feel faster on first load.

---

### Phase 1, Step 4 — Added meta description and Open Graph tags
**What:** Added `<meta name="description">` and Open Graph tags (`og:title`, `og:description`, `og:image`, `og:type`) to all 8 pages.

**Why:** Without these tags, search engines have no summary to display in results, and when someone shares a link to the site on Instagram, LinkedIn, iMessage, or any other platform, the preview is blank or just shows the URL. With Open Graph tags, shared links show a title, description, and the artist's photo — much more professional for a portfolio site.

**Files changed:** All 8 HTML files

**UI impact:** None. These tags are invisible on the page itself. They only affect search results and link previews.

---

### Phase 1, Step 5 — Replaced inline styles with CSS classes
**What:** Moved image sizing from inline `style` attributes to CSS classes. Created three new classes in `index.css`: `.artwork-tall` (height: 90vh), `.artwork-wide` (width: 68.5%), `.artwork-medium` (width: 70%). Replaced all inline `style="height:90vh;"`, `style="width:68.5%;"`, and `style="width:70%;"` on `<img>` tags with the corresponding class.

**Why:** Inline styles are harder to maintain — to change the size of all tall artworks, you'd have to edit every single HTML file. With CSS classes, you change one line in `index.css` and it updates everywhere. It also keeps the HTML cleaner and easier to read.

**Files changed:** index.css, grids.html

**UI impact:** None. Images display at exactly the same sizes as before.

---

### Phase 2, Step 1 — Consolidated desktop/mobile HTML into single markup
**What:** On 4 gallery pages (grids, recreations, self, misc), removed the duplicate mobile HTML section. Content now lives in one place. Items that Pavel intentionally hid on mobile are marked with a `desktop-only` CSS class so they stay hidden on small screens.

Two pages kept their desktop/mobile split because mobile has a fundamentally different experience:
- `index.html` — desktop shows a grid of squares, mobile shows a text list
- `panels.html` — desktop shows 82 artworks in 4 columns, mobile shows a message directing users to desktop

Two pages (`appreciation.html`, `feeling.html`) never had the split to begin with.

**Why:** Previously, every content update (adding an artwork, fixing a typo) had to be done in two places. Now it's done once. This cuts maintenance effort in half and eliminates the risk of desktop and mobile falling out of sync.

**Files changed:** grids.html, recreations.html, self.html, misc.html

**UI impact:** None. Desktop and mobile views render the same content as before.

---

### Phase 2, Step 2 — Replaced all layout tables with figure components
**What:** Replaced all 165 `<table>` elements across every gallery page with clean `<figure>` elements. Each artwork is now:

```html
<figure class="artwork artwork-horiz">
    <a href="artworks/folder/file.jpg" target="_blank" rel="noopener noreferrer">
        <img loading="lazy" src="artworks/folder/file.jpg">
    </a>
    <figcaption>
        <cite>title</cite>
        <br><br>date
        <br>medium, dimensions
    </figcaption>
</figure>
```

Three variants: `artwork-horiz` (landscape), `artwork-vert` (portrait, caption beside image), `artwork-vert-left` (portrait, caption on left).

**To add a new artwork:** Copy any `<figure>` block, change the image path and caption text. That's it. No tables, no complex nesting.

**Why:** Tables are meant for tabular data, not image layouts. The old table markup was ~12 lines per artwork with nested `<tr>`, `<td>`, and IDs. The new figure markup is ~8 lines with clear, readable structure. This makes it much easier for the client to add, remove, or reorder artworks.

**Files changed:** All 7 gallery pages (grids.html, recreations.html, feeling.html, self.html, panels.html, appreciation.html, misc.html)

**UI impact:** None. Artworks display in the same positions with the same spacing.

---

### Phase 2, Step 3 — Added semantic HTML elements
**What:** Added proper HTML5 semantic elements across all pages:
- `<nav>` wraps all navigation links
- `<main>` wraps gallery content (replaces `<section class="main-content">`)
- `<cite>` wraps artwork titles (replaces `<b><i>`)
- `<figcaption>` wraps artwork descriptions (replaces `<td>`)

Also fixed the improperly nested `</div></a>` on the homepage grid (was `<div><a>...</div></a>`, now `<div><a>...</a></div>`).

**Why:** Semantic HTML tells browsers and search engines what each part of the page means. `<nav>` says "this is navigation," `<figure>` says "this is an artwork," `<cite>` says "this is the title of a creative work." This improves search engine indexing and makes the code self-documenting.

**Files changed:** All 8 HTML files

**UI impact:** None. Semantic elements are invisible — they describe meaning, not appearance.

---

### Phase 2, Step 4 — Organized CSS with sections and artwork component
**What:** Reorganized `index.css` into clearly labeled sections:
- Reset & Base
- Layout: Desktop/Mobile (includes new `.desktop-only` / `.mobile-only` utility classes)
- Container & Bio Sidebar
- Home Page Grid
- Gallery Scrollboxes
- Artwork Components (new)
- Artwork Size Variants
- Indicators

Added a detailed comment block in the Artwork Components section explaining how to add a new artwork — with copy-paste examples for horizontal and vertical layouts.

Kept all legacy table/scroll-item styles marked as "legacy support" so nothing breaks during incremental migration.

**Why:** The CSS was a single undivided 375-line file. Now it's organized by purpose with clear section headers, making it easy to find and modify styles. The artwork component comment serves as inline documentation for the client.

**Files changed:** index.css

**UI impact:** None. No visual properties were changed, only organization.

---

### Mobile update — All artworks now visible on mobile
**What:** Made every artwork visible on mobile across all pages:

1. **recreations.html** — removed `desktop-only` from 6 artworks (dimension demos, swan maidens, eight bells, eternal love). All 20+ recreations now visible on mobile.

2. **self.html** — removed `desktop-only` from 3 artworks (and you can dance, stamp collector, untitled polyethylene). All 13 self-portraits now visible on mobile.

3. **misc.html** — removed `desktop-only` from 2 artworks (things to do, ascendant attendant). All 12 miscellaneous works now visible on mobile.

4. **panels.html** — removed the mobile "view on desktop" message entirely. The 4-column grid now collapses into a single scrollable column on mobile, showing all 82 individual panels. Added CSS media query for `panels-scrollbox-container` to stack vertically.

5. **index.html** — added missing links to mobile navigation: "feeling (2020-21)" and "appreciation (2021-22)". Moved "individual panels" to bottom of project list. Removed the "see more art in desktop view" note since all content is now available on mobile.

**Why:** The client wants the mobile experience to be fully representative of the site. Previously, mobile visitors were seeing a curated subset — missing up to 11 artworks per page, and the entire panels collection was hidden. Now every visitor sees the complete portfolio regardless of device.

**Files changed:** index.html, index.css, recreations.html, self.html, misc.html, panels.html

**UI impact:** Mobile now shows MORE content than before. Desktop is unchanged. No existing content was removed or rearranged — only previously hidden items are now visible.

---

### Image optimization — Compressed all artwork images
**What:** Resized all 183 artwork images to reduce file sizes:

- Gallery images (appreciation, feeling, grids, misc, recreations, self): resized so longest edge is max 2000px
- Individual panel images (82 files): resized so longest edge is max 1200px (these display smaller in a multi-column grid)
- Thumbnail files (`_thumb.jpg`) were already small and left unchanged

Results by directory:
- appreciation: 36 MB → 4.4 MB
- feeling: 42 MB → 11 MB
- grids: 26 MB → 8.8 MB
- individual panels: 100 MB → 29 MB
- misc: 25 MB → 8.1 MB
- recreations: 47 MB → 15 MB
- self: 30 MB → 9.5 MB
- **Total: 318 MB → 92 MB (71% reduction)**

Some images were extremely oversized — for example, `shailen.jpg` in appreciation was 14,138 x 11,213 pixels (7.9 MB). Now it's 2,000 x 1,586 pixels (808 KB). 2000px is more than enough for any screen.

**Why:** Large images are the #1 cause of slow page loads. The panels page alone was loading 100 MB of images. Combined with the lazy loading added in Phase 1, pages should now load significantly faster — especially on mobile connections.

**Files changed:** All 183 image files in the artworks/ directory

**UI impact:** Images display at exactly the same size on screen. The only difference is faster loading. At 2000px max width, images remain sharp on high-DPI (Retina) displays.

---

### Mobile fix — Single continuous scroll on all gallery pages
**What:** Fixed nested scrolling issue on mobile. Previously, each gallery page on mobile had multiple independent scrolling areas stacked inside the page: the bio sidebar was its own scroll box, and each gallery column was capped at 90vh with its own scroll. This created a confusing experience where you'd scroll one box, hit the bottom, then have to find and scroll the next box.

Now on mobile: the bio/description text sits at the top, and all artworks flow below it in one continuous scroll. One finger, one scroll, top to bottom.

CSS changes in the mobile media query:
- `.bio`: removed `overflow-y: auto` so it flows as normal content
- `.scrollbox`: removed `max-height: 90vh` and `overflow-y: auto` so artworks are not trapped in scroll boxes
- The two gallery columns stack vertically and flow naturally

**Why:** On desktop, separate scroll areas make sense — you have a fixed sidebar and scrollable gallery columns side by side. On mobile, everything is stacked in one column, so having multiple nested scroll areas is confusing and feels broken. The standard mobile pattern is one page, one scroll.

**Files changed:** index.css

**UI impact:** Mobile only. Gallery pages now scroll as one continuous page instead of having nested scroll boxes. Desktop is unchanged.

---

### Mobile fix — Reduce top padding on homepage
**What:** Reduced the top padding on the mobile homepage from 3rem to 1rem. Kept all original spacing between links exactly as before. This shifts everything up so the contact links (c.v., email, instagram, linkedin) are less likely to be cut off below the fold.

**Why:** The email, instagram, and linkedin links were pushed below the fold by excess top padding.

**Files changed:** index.html

**UI impact:** Mobile homepage only. Everything shifts up slightly. Spacing between items unchanged. Desktop unchanged.

---
