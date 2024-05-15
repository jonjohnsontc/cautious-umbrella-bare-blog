# Issue Tracker

Bare bones checklist to figure out what I'd like to do next with my blog

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
- [x] ability to see draft posts in dev server
- [x] finish 'moving-from-spa-to-mpa'
- [x] start implementing some tests to validate these features
- [] change content font
- [] fix sorting posts without a date
- [] fix the 'modified' file
- [] update colors for links
- [] remove footnote demo

## Nice to Have's

- [] consolidate classes that aren't being used in templates, or aren't listed in styles.css + codehilite-styles.css
- [] add dark mode via os-system settings
- [x] some way to not have to deal with re-doing the css for TWIL 1 post
- [] checking all sub-templates to see if they've been updated too

## Including Fonts

- Looks like I can do so with @font-face declaration in my css
- Thought I have done it somewhere before, but not in my Gatsby blog or swg-remix

## Checking sub-templates

I'd like to recursively check all of the main templates, and see if any sub-templates are defined within

## Themes

- Add tango theme for codehilite styles (booberry)
- Add github-dark theme for codehilite styles (dark)

- You added a border for the code snippet, along with some padding
  - .codehilite { background: #f9f5d7; padding: 1em; border: 3px solid var(--primary)}

- One thing that I just remembered, the `<meta name="theme-color">` tag that 

## Adding Footnotes

I want to add footnotes as both clickable elements, and collected at the very bottom of any post.

Python-Markdown already has support for footnotes in the latter context

I could write an extension that adds what I need (I think.)

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

## OS default in theme selector

Right now, I store a value in local storage if someone has selected a theme. That changes the value of the body attribute on load via javascript.

I want the default theme to be 'gruvbox' during the day, but 'dark' if prefers-color-scheme: dark is set.

## ability to see draft posts in dev server

Right now, I have to execute `render_templates.py` if I want to see any changes that I've made to my website. However, every page that's output with render templates will make its way to the public folder, and exactly where Cloudflare pages looks for my pages every time I push.

Solution: I'm going to have `render_templates` add a .draft.html suffix to the draft files, and place that in my .gitignore file.

## start implementing some tests to validate these features

I wanna look at my `dependency_has_been_modified` functions, and make sure that render_templates is writing new versions of pages when I need to, and not writing them when I don't (aka working as intended).

### How will testing generally work?

For every test scenario, I'm going to run render_templates, and verify the output. My plan currently is to keep each test result around in a `test_output` directory, but not put that directory in version control.

In order for this to work, I need to modify the render_templates script to accept an argument for it's output directory.

### How do i test the situation of making sure all dependencies have been written to the modified file?

I think the easiest way would be to run the entire thing and check the resulting `modified` file. The same would go for any other scenarios.
