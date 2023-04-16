"""
Takes content in the "posts" directory, and makes a bunch of html
pages out of them. Then it builds the blog index based on all the
pages built
"""
import json
import os

from datetime import datetime
from pathlib import Path

import markdown

from jinja2 import Environment, PackageLoader, Template

# Different paths that we rely on to build the website
CONTENT_LOC = Path("content")
TEMPLATES_LOC = Path("templates")
POSTS_LOC = CONTENT_LOC.joinpath("posts")
INDEX_LOC = CONTENT_LOC.joinpath("index.md")
ABOUT_LOC = CONTENT_LOC.joinpath("about.md")
STORE_LOC = CONTENT_LOC.joinpath("modified")

# Templates to pass through to Jinja
BASE_TEMPLATE = "base.html.j2"
INDEX_TEMPLATE = "index.html.j2"
ABOUT_TEMPLATE = "about.html.j2"
LIST_TEMPLATE = "list.html.j2"


def get_post(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_store():
    """Loads the modified store to see if a file should be updated"""
    if os.path.isfile(STORE_LOC):
        with open(STORE_LOC, "r", encoding="utf-8") as f:
            try:
                store: dict = json.load(f)
            # if we have trouble opening the store we'll just
            # make a new one. If the store is a completely empty
            # file, this will also happen
            except json.JSONDecodeError:
                store = {}
    else:
        store = {}
    return store


def file_has_been_modified(filepath: str, store: dict):
    """Returns a bool indicating whether or not the file has
    been modified since this script has last been run

    If the page can't be found in the store, the function will
    return True
    """
    modified_at = store.get(filepath, None)
    if modified_at:
        return modified_at != os.stat(filepath).st_mtime
    return True


def index_page_needs_to_be_updated(store: dict):
    return True


def about_page_needs_to_be_updated(store: dict):
    return True


def blog_list_needs_to_be_updated(store: dict):
    """Examines the blog posts that have been picked up and determines if the
    blog list page needs to be updated
    """
    if file_has_been_modified(INDEX_LOC, store=store) or file_has_been_modified():
        pass
    return True


def output_page(template: Template, content: str, **kwargs):
    """Outputs a page, given an jinja template and content parsed through
    python-markdown
    """
    mkdn = markdown.markdown(content)
    return template.render(mkdn, **kwargs)


def output_blog_pages():
    pass


# TODO: Before outputting any page, I wanna check if either
# the template has been modified or the content file. If either
# has been modified, the page will be output.
if __name__ == "__main__":
    env = Environment(
        loader=PackageLoader("render_templates", TEMPLATES_LOC),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
    )
    template = env.get_template(BASE_TEMPLATE)
    posts = []
    store = load_store()
    with os.scandir(POSTS_LOC) as dir:
        for entry in dir:
            if entry.path.endswith(".md"):
                mkdn = get_post(entry.path)
                parser = markdown.Markdown(
                    extensions=["tables", "meta", "codehilite"], output_format="html"
                )
                post = parser.convert(mkdn)
                filename = os.path.basename(entry.path)[:-3]
                bp = {
                    "title": parser.Meta.get("title").pop(),
                    "date": parser.Meta.get("date").pop(),
                    # this path should be absolute since
                    # the server is using this to find it
                    "path": f"/blog/{filename}",
                }
                posts.append(bp)
                if file_has_been_modified(entry.path, store):
                    # looking for posts that need syntax highlighting, and
                    # including it if necessary
                    codehilite = None
                    if parser.Meta.get("code"):
                        codehilite = True
                    print("Working on", entry.path, "🪩")
                    with open(
                        f"./public/blog/{filename}.html", "w+", encoding="utf-8"
                    ) as f:
                        f.write(
                            template.render(
                                title=bp["title"],
                                post=post,
                                date=bp["date"],
                                license=parser.Meta.get("license").pop(),
                                code=codehilite,
                            )
                        )
                    store.update({entry.path: os.stat(entry.path).st_mtime})
    if blog_list_needs_to_be_updated(store):
        posts.sort(key=lambda p: datetime.fromisoformat(p["date"]), reverse=True)
        print("Working on blog index", "🌈🗂")
        template = env.get_template("list.html.j2")
        with open("./public/blog/index.html", "w+", encoding="utf-8") as f:
            f.write(template.render(posts=posts))
    if about_page_needs_to_be_updated(store):
        pass
    if index_page_needs_to_be_updated(store):
        pass

    with open(STORE_LOC, "w+", encoding="utf-8") as f:
        print("Updating store 📙")
        json.dump(store, f)
