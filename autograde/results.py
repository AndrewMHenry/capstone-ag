"""This module implements converting results to and from text."""

import json


def write_results(filename, results):
    """Write a list of results to a file.

    `filename` - the name of the file
    
    `results` - the list of result dicts to write

    """
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(results))


def read_results(filename):
    """Return a list of results from a file.

    filename -- the name of the file to read

    """
    with open(filename, 'r') as infile:
        text = infile.read()
    return json.loads(text)

