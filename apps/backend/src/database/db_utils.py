import pathlib


def get_path(name: str):
    """Function that returns the path to the file."""

    management_path = pathlib.Path(__file__).parent
    parent_path = management_path.parent.parent
    path = name
    return parent_path / path
