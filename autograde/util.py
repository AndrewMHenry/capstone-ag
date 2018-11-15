import os

def get_data_filename(filename):
    """ """
    return os.path.join(os.path.dirname(__file__), 'data', filename)
