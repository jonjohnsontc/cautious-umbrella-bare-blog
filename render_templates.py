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
INDEX_TMPL_LOC = TEMPLATES_LOC.joinpath("index.html.j2")
ABOUT_LOC = CONTENT_LOC.joinpath("about.md")
ABOUT_TMPL_LOC = TEMPLATES_LOC.joinpath("about.html.j2")
STORE_LOC = CONTENT_LOC.joinpath("modified")

BLOG_TEMPLATE = "base.html.j2"
BLOG_TEMPLATE_LOC = TEMPLATES_LOC.joinpath(BLOG_TEMPLATE)
INDEX_TEMPLATE = "index.html.j2"
ABOUT_TEMPLATE = "about.html.j2"
LIST_TEMPLATE = "list.html.j2"
ERR_TEMPLATE = "404.html.j2"
ERR_TMPL_LOC = TEMPLATES_LOC.joinpath(ERR_TEMPLATE)
ERR_LOC = CONTENT_LOC.joinpath("404.md")


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


def file_has_been_modified(filepath: str | Path, store: dict):
    """Returns a bool indicating whether or not the file has
    been modified since this script has last been run

    If the page can't be found in the store, the function will
    return True
    """
    if isinstance(filepath, os.PathLike):
        filepath = str(filepath)
    modified_at = store.get(filepath, None)
    if modified_at:
        return modified_at != os.stat(filepath).st_mtime
    return True


def index_page_needs_to_be_updated(store: dict) -> bool:
    tmpl_path = TEMPLATES_LOC.joinpath(INDEX_TEMPLATE)
    if file_has_been_modified(tmpl_path, store=store) or file_has_been_modified(
        INDEX_LOC, store=store
    ):
        return True
    return False


def about_page_needs_to_be_updated(store: dict) -> bool:
    templ_path = TEMPLATES_LOC.joinpath(ABOUT_TEMPLATE)
    if file_has_been_modified(templ_path, store=store) or file_has_been_modified(
        ABOUT_LOC, store=store
    ):
        return True
    return False


def err_page_needs_to_be_updated(store: dict) -> bool:
    if file_has_been_modified(ERR_LOC, store) or file_has_been_modified(
        ERR_TMPL_LOC, store
    ):
        return True
    return False


def blog_list_needs_to_be_updated(store: dict, store_snapshot: dict) -> bool:
    """Examines the blog posts that have been picked up and determines if the
    blog list page needs to be updated
    """
    if store != store_snapshot or file_has_been_modified(
        TEMPLATES_LOC.joinpath(LIST_TEMPLATE), store=store
    ):
        return True
    return False


def output_page(template: Template, content_loc: str):
    """Outputs a page, given an jinja template and location of content file"""
    with open(content_loc, "r", encoding="utf-8") as f:
        content = f.read()
    parser = markdown.Markdown(extensions=["meta"], output_format="html")
    kwargs = {}
    # we'll convert the post to from markdown to html, and
    # add it as a kwarg to the template
    kwargs["post"] = parser.convert(content)
    # if there's any metadata, we'll convert it from
    # having list values to str values and use them
    # as keyword arguments for the template
    if parser.Meta:
        for k in parser.Meta:
            # we assume there's no underlying list of content
            # i don't think the meta-data extension can parse
            # shit like that anyhoot
            val = parser.Meta[k].pop()
            kwargs[k] = val
    return template.render(**kwargs)


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
    template = env.get_template(BLOG_TEMPLATE)
    posts = []
    store = load_store()
    # creating this snapshot to see if anything
    # changes with the store while we build the
    # blog pages
    snapshot = store.copy()
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
    if blog_list_needs_to_be_updated(store, snapshot):
        posts.sort(key=lambda p: datetime.fromisoformat(p["date"]), reverse=True)
        print("Working on blog index 🌈🗂")
        template = env.get_template(LIST_TEMPLATE)
        with open("./public/blog/index.html", "w+", encoding="utf-8") as f:
            f.write(template.render(posts=posts))
        store.update(
            {
                TEMPLATES_LOC.joinpath(LIST_TEMPLATE)
                .as_posix(): os.stat(TEMPLATES_LOC.joinpath(LIST_TEMPLATE))
                .st_mtime
            }
        )
    if about_page_needs_to_be_updated(store):
        print("Working on the about page 🤗")
        template = env.get_template(ABOUT_TEMPLATE)
        page = output_page(template, ABOUT_LOC)
        with open("./public/about.html", "w+") as f:
            f.write(page)
        store.update(
            {
                ABOUT_TMPL_LOC.as_posix(): os.stat(ABOUT_TMPL_LOC).st_mtime,
                ABOUT_LOC.as_posix(): os.stat(ABOUT_LOC).st_mtime,
            }
        )
    if index_page_needs_to_be_updated(store):
        print("Working on the index page 🙈")
        template = env.get_template(INDEX_TEMPLATE)
        page = output_page(template, INDEX_LOC)
        with open("./public/index.html", "w+") as f:
            f.write(page)
        store.update(
            {
                INDEX_TMPL_LOC.as_posix(): os.stat(INDEX_TMPL_LOC).st_mtime,
                INDEX_LOC.as_posix(): os.stat(INDEX_LOC).st_mtime,
            }
        )
    if err_page_needs_to_be_updated(store):
        print("Working on the 404 page ❌")
        template = env.get_template(ERR_TEMPLATE)
        page = output_page(template, ERR_LOC)
        with open("./public/404.html", "w+") as f:
            f.write(page)
        store.update(
            {
                ERR_LOC.as_posix(): os.stat(ERR_LOC).st_mtime,
                ERR_TMPL_LOC.as_posix(): os.stat(ERR_TMPL_LOC).st_mtime,
            }
        )
    with open(STORE_LOC, "w+", encoding="utf-8") as f:
        print("Updating store 📙")
        json.dump(store, f)
