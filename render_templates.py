"""
Takes content in the "posts" directory, and makes a bunch of html
pages out of them. Then it builds the blog index based on all the
pages built
"""
import json
import os

from datetime import datetime

import markdown

from jinja2 import Environment, PackageLoader


TEMPLATES_LOC = "./templates"
POSTS_LOC = "./content/posts"
BASE_TEMPLATE = "base.html.j2"
STORE_LOC = "./content/posts/modified"


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


def page_has_been_modified(filepath: str, store: dict):
    """Returns a bool indicating whether or not the page has
    been modified since this script has last been run

    If the page can't be found in the store, the function will
    return True
    """
    modified_at = store.get(filepath, None)
    if modified_at:
        return modified_at != os.stat(filepath).st_mtime
    return True


def blog_index_needs_to_be_updated():
    """Examines the blog posts that have been picked up and determines if the
    index page needs to be updated
    """
    # TODO: Implement
    return True


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
                if page_has_been_modified(entry.path, store):
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
    if blog_index_needs_to_be_updated():
        posts.sort(key=lambda p: datetime.fromisoformat(p["date"]), reverse=True)
        print("Working on blog index", "🌈🗂")
        template = env.get_template("list.html.j2")
        with open("./public/blog/index.html", "w+", encoding="utf-8") as f:
            f.write(template.render(posts=posts))
    with open(STORE_LOC, "w+", encoding="utf-8") as f:
        print("Updating store 📙")
        json.dump(store, f)
