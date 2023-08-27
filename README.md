# Blog Bare

My new and improved* blog site. A JAMstack special, hosted on Cloudflare pages, and built with the `render_template` script. There's a simple dev server in `server.py` that will render all the pages, including any 'draft' posts that I don't think are ready to publish.

I've mostly been committing directly to main, though if I have to work on some feature long term, I could consider branching. Part of me thinks this is a bad idea for eventually merging the feature branches in, however.

## Content

Blog posts are written in the `./posts` directory, and then built into html pages via the `render_templates.py` script. Right now, the pages are output into the working version of the site in the `./public` directory.

### Drafts

Draft posts can be identified in yaml frontmatter (with `draft: true`), and `render_templates` will output the file with the suffix `draft.html`. These files have been added to our .gitignore, so that they don't make their way to the deployment/version control.

## Templates

I'm using jinja templating to put together each blog post. Eventually, I'd like to build or iterate on all of my pages with templates (or at least, some method where I can keep things DRY).

## Issues

Issues and upcoming features are all noted in issue_tracker.md
