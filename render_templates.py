"""
Takes content in the "posts" directory, and makes a bunch of html
pages out of them
"""
import os

import markdown
import yaml

from jinja2 import Environment, PackageLoader

# I want to take base.html.j2, along with a markdown file that has some frontmatter
# parse the frontmatter into variables, along with the content, and output
# some html
TEMPLATES = "./templates"
POSTS = "./posts"
BASE_TEMPLATE = "base.html.j2"


def get_post(path: str):
    with open(path, "r", encoding="utf-8") as f:
        contents = f.read()

    # We're naively splitting the markdown content from the frontmatter using
    # string split, so if anything is malformed, I'm not going to notice it until
    # it's on the site (or way after :0\)
    _, frontmatter, post = contents.split("---")
    return frontmatter, post


def reformat_val(value: str):
    """Parses date formatted as YYYY-MM-DD, and returns it as MM-DD-YYYY"""
    year = value[:4]
    month = value[5:7]
    day = value[8:]
    return f"{month}-{day}-{year}"


def parse_frontmatter(frontmatter: str):
    return yaml.safe_load(frontmatter)


if __name__ == "__main__":
    env = Environment(
        loader=PackageLoader("render_templates", TEMPLATES), autoescape=False
    )
    env.filters["date_format"] = reformat_val
    template = env.get_template(BASE_TEMPLATE)
    with os.scandir(POSTS) as dir:
        for entry in dir:
            if entry.path.endswith(".md"):
                config, mkdn = get_post(entry.path)
                frontmatter: dict = parse_frontmatter(config)
                post = markdown.markdown(mkdn)
                filename = os.path.basename(entry.path)[:-3]
                with open(
                    f"./public/blog/{filename}.html", "w+", encoding="utf-8"
                ) as f:
                    f.write(
                        template.render(
                            title=frontmatter["title"],
                            post=post,
                            date=frontmatter["date"],
                            license=frontmatter["license"],
                        )
                    )
