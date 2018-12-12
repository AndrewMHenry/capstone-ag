from autograde.results import read_results
import json

def generate_report(filename):
    """
    TODO: What data exactly do we get from grading results?

    Return a string with the report text.
    """
    with open(filename, 'r') as f:
        string = f.read()

    myobject = json.loads(string)

    # turn myobject into our report text
    report_text = myobject['Name'] + ' got a grade of ' + myobject['Grade']

    return report_text


def main():
    """Run AutoGrade UI."""
    # read arguments
    import argparse

    import sys

    # make a parser
    parser = argparse.ArgumentParser()

    # add arguments to the parser
    parser.add_argument('filename')

    # parse the arguments
    args = parser.parse_args()

    # TODO: remove
    print(args.filename)

    # extend to multiple files:
    print(generate_report(args.filename))

if __name__ == '__main__':
    main()
