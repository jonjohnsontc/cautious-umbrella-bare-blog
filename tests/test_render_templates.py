"""
Runs `render_templates` for a number of test scenarios, and ensures that it
runs as expected.

I've structured this so that some scenarios can share the same test output,
while others should always be run in a fresh environment, therefore, 
the tests are structured into two types of functions, ones that create new 
output files, and ones that are run against a folder of test results.
"""
from pathlib import Path

import subprocess

TEST_DIR = Path(__file__).parent.joinpath('test_output')

def run_render_templates_in_fresh_environment(output_folder: str):
    """Runs the render templates script against the current state of the
    `content` and `templates` directories to a new folder in `test_output`
    """
    output_folder = TEST_DIR.joinpath(output_folder)
    subprocess.run(
        ['python3', 'render_templates.py', '-o', output_folder],
        # if this fails, we want to fail the whole script
        check=True
        )


def all_dependencies_are_written_to_modified_file(output_folder: str) -> bool:
    """After running the script, we want to make sure that all of the
    dependencies used to create the html files (content and template files)
    are listed in the modified store.
    """
    pass


# for each environment, we'll run render_templates and check the resulting
# files.
if __name__ == "__main__":
    pass