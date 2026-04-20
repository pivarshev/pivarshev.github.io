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
