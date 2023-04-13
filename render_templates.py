"""
Takes content in the "posts" directory, and makes a bunch of html
pages out of them
"""
import os

import markdown

from jinja2 import Environment, PackageLoader


TEMPLATES_LOC = "./templates"
POSTS_LOC = "./posts"
BASE_TEMPLATE = "base.html.j2"


class BlogPost:
    """Helper class to represent a blog post"""

    def __init__(self, name, date, path) -> None:
        self.name = name
        self.date = date
        self.path = path

    def __repr__(self) -> str:
        return f"{self.name} published on {self.date}"


def get_post(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    env = Environment(
        loader=PackageLoader("render_templates", TEMPLATES_LOC),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
    )
    template = env.get_template(BASE_TEMPLATE)
    posts = []
    with os.scandir(POSTS_LOC) as dir:
        for entry in dir:
            if entry.path.endswith(".md"):
                mkdn = get_post(entry.path)
                parser = markdown.Markdown(extensions=["tables", "meta", "codehilite"])
                post = parser.convert(mkdn)
                print("Working on", entry.path)
                filename = os.path.basename(entry.path)[:-3]
                bp = BlogPost(
                    name=parser.Meta.get("title").pop(),
                    date=parser.Meta.get("date").pop(),
                    # this path should be absolute since
                    # the server is using this to find it
                    path=f"/blog/{filename}",
                )
                posts.append(bp)
                with open(
                    f"./public/blog/{filename}.html", "w+", encoding="utf-8"
                ) as f:
                    f.write(
                        template.render(
                            title=bp.name,
                            post=post,
                            date=bp.date,
                            license=parser.Meta.get("license").pop(),
                        )
                    )
    print("Working on blog index")
    template = env.get_template("list.html.j2")
    with open("./public/blog/index.html", "w+", encoding="utf-8") as f:
        f.write(template.render(posts=posts))
