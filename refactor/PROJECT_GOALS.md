# Refactor Project Goals

## Golden Rule

**DO NOT change or break any UI functionality of the website.**

Every page must look and behave exactly the same before and after any refactor work. If a change risks altering the visual output or user interactions, it must be tested thoroughly in both desktop and mobile views before committing.

## What We Are Doing

- Improving code quality and maintainability
- Following modern software engineering best practices
- Making the codebase easier to update and extend
- Improving SEO and page load performance
- Documenting everything for the client

## What We Are NOT Doing

- Changing colors, fonts, spacing, or layout
- Adding new pages or features
- Removing or rearranging any content
- Changing how navigation, links, or transitions work
- Redesigning anything

## Testing Checklist (Before Every Commit)

- [ ] Desktop view: every page looks identical to before
- [ ] Mobile view (< 768px): every page looks identical to before
- [ ] All navigation links work (forward and back)
- [ ] All artwork image links open correctly in new tabs
- [ ] Page fade transitions still work
- [ ] Bio sidebar links (CV, email, Instagram, LinkedIn) all work
- [ ] Scroll behavior works on all gallery pages

## Phases

### Phase 1 — Quick Wins
Low-risk, no structural changes. Find-and-replace level work.
- Replace invalid `<list>` elements with `<ul>`
- Add `rel="noopener noreferrer"` to external links
- Add `loading="lazy"` to images below the fold
- Add meta description and Open Graph tags
- Remove empty placeholder images
- Replace inline styles with CSS classes

### Phase 2 — Structural Refactor
Changes HTML structure. Visual output must stay identical.
- Merge duplicate desktop/mobile HTML into single responsive markup
- Replace layout tables with `<figure>` + Flexbox/Grid
- Add semantic HTML elements (`<nav>`, `<main>`, `<figure>`, `<cite>`)
- Fix heading hierarchy
- Organize CSS

### Phase 3 — Enhancements
Optional. Only after Phase 1 and 2 are done and verified.
- Optimize/compress images
- Document Python build scripts
- Consider shared templating approach
- Add .gitignore

## Progress Log

| Date | What was done | Phase | Verified? |
|------|---------------|-------|-----------|
| 2026-04-20 | Created refactor folder with audit and checklists | Setup | N/A |
| 2026-04-20 | Replaced `<list>` with `<ul>` on all gallery pages | Phase 1 | Yes |
| 2026-04-20 | Added `rel="noopener noreferrer"` to 214 external links | Phase 1 | Yes |
| 2026-04-20 | Added `loading="lazy"` to 198 artwork images | Phase 1 | Yes |
| 2026-04-20 | Added meta description and Open Graph tags to all pages | Phase 1 | Yes |
| 2026-04-20 | Replaced inline image styles with CSS classes | Phase 1 | Yes |
| | | | |
