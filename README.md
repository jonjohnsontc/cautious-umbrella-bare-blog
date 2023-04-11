# Blog Bare

Remaking jons.gay with no framework or build tools, unless I'm constructing them myself.

## Content

Blog posts are written in the `./posts` directory, and then built into html pages via the `render_templates.py` script. Right now, the pages are output into the working version of the site in the `./public` directory.

## Templates

I'm using jinja templating to put together each blog post. Eventually, I'd like to build or iterate on all of my pages with templates (or at least, some method where I can keep things DRY).

## To-Do:

- [] why is the index page being served from /blog/twil-20210821?
- [] remove `<meta name="note" content="environment=development">` from pages
- [] Automated way of keeping blog index in sync with blog pages
- [] get dropdown to fire/remove-itself correctly on click
- [] add themes
- [] add footnotes
- [] update colors for links
