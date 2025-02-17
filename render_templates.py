"""
Takes content in the "content" directory, and makes a bunch of html
pages out of them. Then it builds the blog index based on all the
pages built
"""

import argparse
import json
import os
import re

from datetime import datetime
from pathlib import Path

import markdown

from jinja2 import Environment, PackageLoader, Template
from extras.ex_footnotes import FootnoteExtension

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

OUTPUT_DIR = Path(".")

# Right now, this is how we check if any sub-templates have been modified
DEPENDENCIES = ["footer.html.j2", "head.html.j2", "nav.html.j2"]


def get_post(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_store(store_loc=None):
    """Loads the modified store to see if a file should be updated"""
    if os.path.isfile(store_loc):
        with open(store_loc, "r", encoding="utf-8") as f:
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


def dependency_has_been_modified(filepath: str | Path, store: dict):
    """Looks for any sub-templates using regex and returns a bool indicating
    whether or not one of them has been modified
    """
    pattern = r"\w+\.\w+\.j2"
    template = get_post(filepath)
    if sub_templates := re.findall(pattern, template):
        for template in sub_templates:
            if file_has_been_modified(TEMPLATES_LOC.joinpath(template), store):
                return True
    return False


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
    if (
        file_has_been_modified(tmpl_path, store=store)
        or file_has_been_modified(INDEX_LOC, store=store)
        or dependency_has_been_modified(tmpl_path, store=store)
    ):
        return True
    return False


def about_page_needs_to_be_updated(store: dict) -> bool:
    templ_path = TEMPLATES_LOC.joinpath(ABOUT_TEMPLATE)
    if (
        file_has_been_modified(templ_path, store=store)
        or file_has_been_modified(ABOUT_LOC, store=store)
        or dependency_has_been_modified(templ_path, store=store)
    ):
        return True
    return False


def err_page_needs_to_be_updated(store: dict) -> bool:
    if (
        file_has_been_modified(ERR_LOC, store)
        or file_has_been_modified(ERR_TMPL_LOC, store)
        or dependency_has_been_modified(ERR_TMPL_LOC, store=store)
    ):
        return True
    return False


def blog_list_needs_to_be_updated(store: dict, store_snapshot: dict) -> bool:
    """Examines the blog posts that have been picked up and determines if the
    blog list page needs to be updated
    """
    if (
        store != store_snapshot
        or file_has_been_modified(TEMPLATES_LOC.joinpath(LIST_TEMPLATE), store=store)
        or dependency_has_been_modified(
            TEMPLATES_LOC.joinpath(LIST_TEMPLATE), store=store
        )
    ):
        return True
    return False


def output_page(template: Template, content_loc: str):
    """Outputs a page, given an jinja template and location of content file"""
    with open(content_loc, "r", encoding="utf-8") as f:
        content = f.read()
    parser = markdown.Markdown(extensions=["meta"], output_format="html")
    kwargs = {}
    # we'll convert the post from markdown to html, and
    # add it as a kwarg to the template
    kwargs["post"] = parser.convert(content)
    # if there's any metadata, we'll convert it from
    # having list values to str values and use them
    # as keyword arguments for the template
    if parser.Meta:
        for k in parser.Meta:
            # we assume there's no underlying list of content
            # rather, the first value in the list is the only
            # thing we need
            val = parser.Meta[k].pop()
            kwargs[k] = val
    return template.render(**kwargs)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Render Templates",
        description="Creates all the blog pages on my website",
    )
    # Where to output files
    parser.add_argument(
        "-o",
        "--output_dir",
        required=False,
        type=str,
        help="The location to write html files to",
        default=".",
    )
    # location of the modified store. If not present the script
    # will look in ./content
    parser.add_argument(
        "-s",
        "--store_loc",
        required=False,
        type=str,
        help="""Where the modified store is to be located. If not provided, 
                the script will look in the content directory""",
        default=STORE_LOC,
    )
    return parser


parser = create_parser()

# TODO: Before outputting any page, I wanna check if either
# the template has been modified or the content file. If either
# has been modified, the page will be output.
if __name__ == "__main__":
    # NOTE: all args could potentially be null, so I want to
    # use dict.get(item, default) whenever pulling args
    qwargs = parser.parse_args()
    arg_dict = vars(qwargs)
    output_dir = arg_dict.get("output_dir", OUTPUT_DIR)
    env = Environment(
        loader=PackageLoader("render_templates", TEMPLATES_LOC),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(BLOG_TEMPLATE)
    posts = []
    # store_location is potentially null
    store_loc = arg_dict.get("store_loc", STORE_LOC)
    store = load_store(store_loc)
    # creating this snapshot to see if anything
    # changes with the store while we build the
    # blog pages
    snapshot = store.copy()
    with os.scandir(POSTS_LOC) as dir:
        for entry in dir:
            if entry.path.endswith(".md") and "_" not in entry.path:
                mkdn = get_post(entry.path)
                parser = markdown.Markdown(
                    extensions=[
                        "tables",
                        "meta",
                        "codehilite",
                        "attr_list",
                        FootnoteExtension(),
                    ],
                    output_format="html",
                )
                post = parser.convert(mkdn)
                suffix = ".html"
                filename = os.path.basename(entry.path)[:-3]
                # if the blog post is a draft, we'll add the following suffix
                # to make sure it doesn't get pushed to my deployment
                if parser.Meta.get("draft"):
                    suffix = ".draft.html"
                    # we'll add today's date so drafts get published at the top of the blog list
                    parser.Meta["date"].append(
                        datetime.strftime(datetime.today(), "%Y-%m-%d")
                    )
                bp = {
                    "title": parser.Meta.get("title").pop(),
                    "date": parser.Meta.get("date").pop(),
                    # this path should be absolute since
                    # the server is using this to find it
                    "path": f"/blog/{filename}",
                    "description": (
                        parser.Meta.get("description").pop()
                        if parser.Meta.get("description")
                        else None
                    ),
                }
                # This is a silly temporary way to avoid publishing changes to my blog
                # the blog index if a new post is a draft page
                if not parser.Meta.get("draft"):
                    posts.append(bp)
                if (
                    file_has_been_modified(entry.path, store)
                    or file_has_been_modified(BLOG_TEMPLATE_LOC, store)
                    or dependency_has_been_modified(BLOG_TEMPLATE_LOC, store)
                ):
                    # looking for posts that need syntax highlighting, and
                    # including it if necessary
                    codehilite = None
                    if parser.Meta.get("code"):
                        codehilite = True
                    print("Working on", entry.path, "🪩")

                    with open(
                        f"{output_dir}/public/blog/{filename}{suffix}",
                        "w+",
                        encoding="utf-8",
                    ) as f:
                        f.write(
                            template.render(
                                title=bp["title"],
                                description=bp["description"],
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
        with open(f"{output_dir}/public/blog/index.html", "w+", encoding="utf-8") as f:
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
        with open(f"{output_dir}/public/about.html", "w+") as f:
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
        with open(f"{output_dir}/public/index.html", "w+") as f:
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
        with open(f"{output_dir}/public/404.html", "w+") as f:
            f.write(page)
        store.update(
            {
                ERR_LOC.as_posix(): os.stat(ERR_LOC).st_mtime,
                ERR_TMPL_LOC.as_posix(): os.stat(ERR_TMPL_LOC).st_mtime,
            }
        )
    # adding all of the sub-templates/dependencies to the store
    # we wait till the end to make sure that all pages that need to be updated
    # are output
    store.update(
        {
            TEMPLATES_LOC.joinpath(i)
            .as_posix(): os.stat(TEMPLATES_LOC.joinpath(i))
            .st_mtime
            for i in DEPENDENCIES
        }
    )
    # we'll add the base blog template to the store, now that we've created all the posts
    store.update(
        {
            BLOG_TEMPLATE_LOC.as_posix(): os.stat(BLOG_TEMPLATE_LOC).st_mtime,
        }
    )
    with open(store_loc, "w+", encoding="utf-8") as f:
        print("Updating store 📙")
        json.dump(store, f)
