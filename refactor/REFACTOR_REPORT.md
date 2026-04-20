# pivarshev.github.io — Code Refactor Report

**Prepared for:** Pavel Pivarshev
**Prepared by:** Shailen Parmar
**Date:** April 20, 2026
**Scope:** Code quality, structure, accessibility, and performance improvements. No changes to visual design or UI functionality.

---

## Executive Summary

The site is a well-designed artist portfolio with strong visual identity and smooth transitions. However, the underlying code has significant structural issues that make it difficult to maintain, hurt search engine visibility, and fail modern accessibility standards. This report outlines recommended improvements organized by priority.

---

## Current Tech Stack

- **Hosting:** GitHub Pages (static)
- **Languages:** HTML, CSS, vanilla JavaScript
- **Build tools:** Two Python helper scripts for generating gallery HTML
- **Assets:** 183 image files across 7 directories, 2 PDFs
- **Pages:** 8 HTML files (index + 7 gallery pages)

---

## Issues Found

### 1. CRITICAL — Accessibility (WCAG Compliance)

**Missing alt text on all artwork images (183 images)**
- Only 1 image on the entire site has alt text (the artist photo on the homepage)
- Screen readers cannot describe any artwork to visually impaired users
- This is a legal liability under ADA/Section 508 and fails WCAG 2.1 Level A
- **Fix:** Add descriptive alt text to every image (e.g., `alt="Grid 1: paranoia, acrylic on canvas, 2023"`)

**Invalid HTML element: `<list>`**
- Every gallery page uses a custom `<list>` element instead of the standard `<ul>` (unordered list)
- Browsers do not recognize `<list>` as a semantic element — assistive technologies skip it entirely
- **Fix:** Replace all `<list>` tags with `<ul>`

**Layout tables misused for content**
- 420+ `<table>` elements are used to position images and descriptions
- Assistive technologies interpret these as data tables, confusing the content structure
- **Fix:** Replace with CSS Flexbox or Grid layouts using `<figure>` and `<figcaption>`

**Missing `rel="noopener noreferrer"` on external links**
- 192 links with `target="_blank"` lack this attribute
- This is a security concern (the opened page can access `window.opener`)
- **Fix:** Add `rel="noopener noreferrer"` to all `target="_blank"` links

---

### 2. HIGH — Code Duplication

**Desktop and mobile layouts are fully duplicated**
- Every page contains two complete copies of its content: one inside `<div class="desktop-layout">` and one inside `<div class="mobile-layout">`
- These are toggled with `display: none` via a CSS media query at 768px
- This means every content change must be made in two places, doubling maintenance effort and increasing the risk of the two versions falling out of sync
- **Current duplication estimate:** ~40-60% of each HTML file is duplicate content

**Fix:** Remove the duplicate mobile markup entirely. Use a single HTML structure with CSS media queries and responsive design to adapt the layout across screen sizes. This is standard modern practice and cuts the HTML in each file roughly in half.

---

### 3. HIGH — Semantic HTML

**No `<nav>` element for navigation**
- The homepage grid and all back-links lack semantic `<nav>` wrapping
- Search engines and assistive technologies cannot identify the site navigation

**No `<figure>` / `<figcaption>` for artwork**
- Artwork images and their descriptions (title, date, medium) are inside `<table>` cells
- The semantic equivalent is `<figure>` with `<figcaption>`, which tells browsers and search engines "this is an artwork with a caption"

**Inconsistent heading hierarchy**
- Some pages use `<h1>` for the page title, others don't
- No consistent `<h1>` > `<h2>` > `<h3>` structure across pages
- **Fix:** Each page should have exactly one `<h1>` (page title) with subheadings as needed

**Artwork titles use `<b><i>` instead of semantic tags**
- `<b><i>title</i></b>` should be `<em>` or `<cite>` for artwork titles
- `<cite>` is the correct HTML element for the title of a creative work

---

### 4. MEDIUM — CSS Organization

**All styles in a single 375-line file**
- `index.css` contains styles for all 8 pages
- As the site grows, this becomes harder to navigate and maintain

**30+ inline styles scattered across HTML files**
- Image widths/heights set via `style="width:68.5%;"` directly on elements
- These should be CSS classes (e.g., `.artwork-horizontal`, `.artwork-vertical`) for consistency

**Inconsistent image sizing**
- Some images: `style="width:68.5%;"`
- Some images: `style="height:90vh;"`
- Some images: no style at all
- **Fix:** Define 2-3 standard image size classes and apply consistently

---

### 5. MEDIUM — SEO and Social Sharing

**Missing meta descriptions**
- No `<meta name="description">` on any page
- Search engines have no summary to display in results

**Missing Open Graph tags**
- No `og:title`, `og:description`, `og:image` tags
- When shared on Instagram, LinkedIn, or iMessage, the link preview will be blank or generic
- For an artist portfolio, rich link previews are especially valuable

**Fix:** Add meta description and Open Graph tags to each page. Example:
```html
<meta name="description" content="Pavel Pivarshev — artist portfolio featuring grids, recreations, self-portraits, and more.">
<meta property="og:title" content="Pavel Pivarshev">
<meta property="og:image" content="newpavel.png">
```

---

### 6. MEDIUM — Performance

**No lazy loading on images**
- All 183 images load immediately when any page is opened
- On the panels page alone, 82 images load at once
- **Fix:** Add `loading="lazy"` to images below the fold. This is a single HTML attribute per image — no JavaScript needed.

**No image optimization pipeline**
- Images appear to be full-resolution originals
- No WebP/AVIF versions for modern browsers
- **Fix:** Consider compressing images or providing smaller versions for faster load times

---

### 7. LOW — Code Cleanup

**Empty placeholder elements**
- `<img class="bio-image-placeholder">` appears on every gallery page with no `src` or `alt`
- Renders as a broken image icon in some browsers
- **Fix:** Remove or replace with a proper element

**Python scripts reference missing files**
- `html_rewriter.py` reads from `matrix_html.txt` (not in repo)
- `name_rewriter.py` reads from `matrix_labels.txt` (not in repo)
- These scripts are useful build tools but should be documented or moved to a `/scripts` directory

**Back navigation uses HTML entities**
- `&lt; &lt; &lt;` (renders as `< < <`) used for back links
- **Fix:** Use a proper arrow character: `←` or `← back`

---

## Recommended Refactor Plan

### Phase 1 — Quick Wins (no structural changes)
- [ ] Add `alt` text to all 183 images
- [ ] Replace `<list>` with `<ul>` on all pages
- [ ] Add `rel="noopener noreferrer"` to all `target="_blank"` links
- [ ] Add `loading="lazy"` to images below the fold
- [ ] Add meta descriptions and Open Graph tags
- [ ] Remove empty placeholder `<img>` elements

### Phase 2 — Structural Refactor
- [ ] Consolidate desktop/mobile into single responsive HTML per page
- [ ] Replace layout `<table>` elements with `<figure>` + CSS Flexbox/Grid
- [ ] Move inline styles to CSS classes
- [ ] Add semantic elements: `<nav>`, `<main>`, `<figure>`, `<figcaption>`, `<cite>`
- [ ] Organize CSS (consider splitting by page or using CSS custom properties)

### Phase 3 — Enhancements
- [ ] Optimize/compress images
- [ ] Document Python build scripts and their input file formats
- [ ] Move scripts to `/scripts` directory
- [ ] Consider a static site generator (e.g., 11ty) to template repeated layouts

---

## File Inventory

| File | Purpose | Lines (est.) |
|------|---------|-------------|
| index.html | Homepage — bio + navigation grid | 86 |
| index.css | All site styles | 375 |
| index.js | Page fade transitions | 49 |
| grids.html | Grids gallery (14 works) | ~400 |
| recreations.html | Art recreations (20+ works) | ~600 |
| feeling.html | Feeling project (20 works) | ~500 |
| self.html | Self-portraits (13 works) | ~400 |
| panels.html | Individual panels (82 works) | ~1200 |
| appreciation.html | Friend portraits (6 works) | ~300 |
| misc.html | Miscellaneous works | ~400 |
| html_rewriter.py | HTML generator for panels | 45 |
| name_rewriter.py | Label generator for panels | 40 |

**Total image assets:** 183 files across 7 directories

---

*This report covers code structure and best practices only. No visual design or UI functionality changes are proposed.*
