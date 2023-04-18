# Blog Bare

Remaking jons.gay with no framework or build tools, unless I'm constructing them myself.

## Content

Blog posts are written in the `./posts` directory, and then built into html pages via the `render_templates.py` script. Right now, the pages are output into the working version of the site in the `./public` directory.

## Templates

I'm using jinja templating to put together each blog post. Eventually, I'd like to build or iterate on all of my pages with templates (or at least, some method where I can keep things DRY).

## To-Do:

- [x] why is the index page being served from /blog/twil-20210821?
  - wrong address! That's the 404 basically?
- [x] remove `<meta name="note" content="environment=development">` from pages
- [x] Automated way of keeping blog index in sync with blog pages
- [x] get dropdown to fire/remove-itself correctly on click
- [] add themes
- [x] generate about and index pages with templates
- [] add footnotes
- [] update colors for links
- [] add a 404.html page
- [] include fonts

## Nice to Have's:

- [] consolidate classes that aren't being used in templates, or aren't listed in styles.css + codehilite-styles.css
- [] add dark mode via os-system settings

## Keeping Blog index in sync with blog pages

- Use a jinja template for the blog index page
  - (nice to have) if the file's have changed, the blog page is updated
  - Runs during the `render_templates` script

## Generate all pages in site instead of just blog

Right now, I'm just generating all blog related pages. But, dealing with multiple versions of the nav bar, and hand editing the other html files has me thinking this will feature less pain if all pages are generated.

Ideally, I'd like to get to a place where I'm not modifying code for every release. I want to just add a markdown file, (template if needed,) and run `render_templates`.

Part of me thinks if I codify what pages should be built in data somewhere, I could avoid making more changes to code if I do want to add more pages in the future. Like, some sort of layout.json file or similar.

I think I'm gonna plan on having the structure (e.g, what pages are being created) happening in code. I don't think my website will add a bunch of pages over time (outside of blog posts), and if I wanna remove about or index or something, it'll be easy enough.

### Should I piecemeal all the repeated elements with macros?

No, I think some elements should customized through `render_templates` (i.e., in code), while other elements should be defined completely in the template.
