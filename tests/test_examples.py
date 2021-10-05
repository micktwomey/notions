"""Perform tests against a real Notion account using the examples

Examples are assumed to read the following env vars:

- NOTION_API_KEY
"""

import os
import pathlib
import subprocess
import sys

import pytest

pytestmark = pytest.mark.skipif(
    (
        "NOTION_API_KEY" not in os.environ
        or "NOTIONS_PARENT_PAGE_UUID" not in os.environ
    ),
    reason=(
        "Missing environment keys to test notions client against real api. "
        "Looking for NOTION_API_KEY and NOTIONS_PARENT_PAGE_UUID."
    ),
)

# Assuming examples are in a sibling folder to this `tests` folder
EXAMPLES_PATH = pathlib.Path(__file__).parent / "../examples"
assert EXAMPLES_PATH.is_dir(), f"{EXAMPLES_PATH=} not a directory!"

# Generate a list of all examples, assuming *.py are fair game to run
EXAMPLES = [f for f in EXAMPLES_PATH.glob("*.py") if f.is_file()]
EXAMPLE_IDS = [str(f.name) for f in EXAMPLES]  # create a nicer set of ids


@pytest.mark.parametrize("example_path", EXAMPLES, ids=EXAMPLE_IDS)
def test_example(example_path: pathlib.Path):
    print(example_path)
    assert example_path.is_file()
    print(sys.executable)
    subprocess.check_call([sys.executable, str(example_path)])
