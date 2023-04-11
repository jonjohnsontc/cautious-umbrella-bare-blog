"""
Takes content in the "posts" directory, and makes a bunch of html
pages out of them
"""
import os

import markdown

from jinja2 import Environment, PackageLoader

# I want to take base.html.j2, along with a markdown file that has some frontmatter
# parse the frontmatter into variables, along with the content, and output
# some html
TEMPLATES = "./templates"
POSTS = "./posts"
BASE_TEMPLATE = "base.html.j2"


def get_post(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def reformat_val(value: str):
    """Parses date formatted as YYYY-MM-DD, and returns it as MM-DD-YYYY"""
    year = value[:4]
    month = value[5:7]
    day = value[8:]
    return f"{month}-{day}-{year}"


if __name__ == "__main__":
    env = Environment(
        loader=PackageLoader("render_templates", TEMPLATES),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
    )
    env.filters["date_format"] = reformat_val
    template = env.get_template(BASE_TEMPLATE)
    with os.scandir(POSTS) as dir:
        for entry in dir:
            if entry.path.endswith(".md"):
                mkdn = get_post(entry.path)
                parser = markdown.Markdown(extensions=["tables", "meta", "codehilite"])
                post = parser.convert(mkdn)
                print("Working on", entry.path)
                filename = os.path.basename(entry.path)[:-3]
                with open(
                    f"./public/blog/{filename}.html", "w+", encoding="utf-8"
                ) as f:
                    f.write(
                        template.render(
                            title=parser.Meta.get("title").pop(),
                            post=post,
                            date=parser.Meta.get("date").pop(),
                            license=parser.Meta.get("license").pop(),
                        )
                    )
