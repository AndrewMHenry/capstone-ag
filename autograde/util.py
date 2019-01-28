import os

def read_file(filename):
    """Return contents of file."""
    with open(filename, 'r') as f:
        source = f.read()
    return source


def get_data_filename(filename):
    """ """
    return os.path.join(os.path.dirname(__file__), 'data', filename)
