"""
Runs `render_templates` for a number of test scenarios, and ensures that it
runs as expected.
"""
from pathlib import Path

import glob
import json
import os
import sys
import subprocess

TEST_DIR = Path(__file__).parents[1].joinpath('test_output')
CONTENT_DIR = Path(__file__).parents[1].joinpath('content')
TEMPLATES_DIR = Path(__file__).parents[1].joinpath('templates')


def get_dependencies() -> list:
    """Globs the default templates and content directories, and returns
    all dependencies used to make the blog
    """
    dependencies = []
    # we're going to write to these relative path locations in the store
    # because that's how render_templates does it
    local_content_dir = "content"
    local_templates_dir = "templates"
    # any top level content posts (e.g., about.md, index.md) 
    # probably won't change much over time
    top_level_content = glob.glob(f"{str(CONTENT_DIR)}/*.md")
    for entry in top_level_content:
        path = Path(entry)
        dependencies.append(os.path.join(local_content_dir, path.name))
    # individual posts, we expect this list to grow over time
    posts = glob.glob(f"{str(CONTENT_DIR)}/posts/*.md")
    for entry in posts:
        path = Path(entry)
        # we don't want to include any _template posts
        if not path.name.startswith("_"):
            dependencies.append(os.path.join(local_content_dir, "posts", path.name))
    # templates, we don't expect this to grow much
    templates = glob.glob(f"{str(TEMPLATES_DIR)}/*.html.j2")
    for entry in templates:
        path = Path(entry)
        dependencies.append(os.path.join(local_templates_dir, path.name))
    return dependencies


def run_render_templates_in_fresh_environment(output_folder: str) -> bool:
    """Runs the render templates script against the current state of the
    `content` and `templates` directories to a new folder in `test_output`
    """
    output_folder = TEST_DIR.joinpath(output_folder)
    res = subprocess.run(
        ['python3', 'render_templates.py', '-o', output_folder, '-s', output_folder.joinpath("modified")],
        capture_output=True,
        text=True,
        )
    # print any errors to stderr
    if res.returncode != 0:
        print("Test setup FAILED: ", res.stderr)
        return False
    return True


def test_all_dependencies_are_written_to_modified_file(output_folder: str) -> bool:
    """After running the script, we want to make sure that all of the
    dependencies used to create the html files (aka content and template files)
    are listed in the modified store.
    """
    print("Testing all_dependencies_are_written_to_modified_file")
    expected_deps = get_dependencies()
    with open(TEST_DIR.joinpath(output_folder, "modified"), "r") as f:
        store = json.load(f)
    # we want to compare this dictionary against the list of dependencies
    actual_deps = list(store.keys())
    expected_deps.sort()
    actual_deps.sort()
    result = set(expected_deps) == set(actual_deps)
    if result is False:
        print("Test FAILED, actual dependencies different from expected dependencies")
        print("Expected dependencies: ", expected_deps)
        print("Actual dependencies: ", actual_deps)
        return result
    print("Test all_dependencies_are_written_to_modified_file PASSED")
    return result



# for each environment, we'll run render_templates and check the resulting
# files.
if __name__ == "__main__":
    default_test_output_dir = TEST_DIR.joinpath('default')
    if not default_test_output_dir.joinpath("public", "blog").exists():
        print(f"Creating test output directory at {default_test_output_dir}")
        os.makedirs(default_test_output_dir.joinpath("public", "blog"))
    test_run_result = run_render_templates_in_fresh_environment(str(default_test_output_dir))
    if test_run_result:
        results = True
        results = test_all_dependencies_are_written_to_modified_file(default_test_output_dir) and results
    else:
        # We have to fail everything if we can't create the test output
        raise Exception("Test setup FAILED")
    if results:
        print("Tests PASSED")
        sys.exit(0)
    raise Exception("One or more tests FAILED")
    