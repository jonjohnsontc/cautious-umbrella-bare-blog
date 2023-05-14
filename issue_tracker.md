# Issue Tracker

Bare bones checklist to figure out what I'd like to do next with my blog

## To-Do for release:

- [x] why is the index page being served from /blog/twil-20210821?
  - wrong address! That's the 404 basically?
- [x] remove `<meta name="note" content="environment=development">` from pages
- [x] Automated way of keeping blog index in sync with blog pages
- [x] get dropdown to fire/remove-itself correctly on click
- [x] add themes
- [x] generate about and index pages with templates
- [x] add footnotes
- [x] add a 404.html page
- [x] include fonts
- [x] green lighthouse scores
- [x] fix blog list page title
- [x] 'OS default' in theme selector
- [x] show correct code styles on load
- [x] add favicon
- [] update colors for links
- [] remove footnote demo
- [] finish 'moving-from-spa-to-mpa'

### OS default in theme selector

Right now, I store a value in local storage if someone has selected a theme. That changes the value of the body attribute on load via javascript.

I want the default theme to be 'gruvbox' during the day, but 'dark' if prefers-color-scheme: dark is set. 