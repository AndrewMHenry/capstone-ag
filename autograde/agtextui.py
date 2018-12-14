from autograde.results import read_results
import json

def generate_report(filename):
    """
    TODO: What data exactly do we get from grading results?

    Return a string with the report text.
    """
    results = read_results(filename)

    questions = results['questions']
    numquestions = len(questions)
    numcorrect = sum([subdict['score'] for subdict in questions.values()])


    # turn myobject into our report text
    report_text = results['name'] + ' got a grade of ' + str(100 * numcorrect / numquestions) + '%\n'

    for question, questiondict in questions.items():
        report_text += (
                'Our confidence that question '
                + question
                + ' is correct is '
                + str(questiondict['correctConf'])
                + '.\n')

    report_text += '\n'

    for question, questiondict in questions.items():
        report_text += 'Question ' + question + ':\n'
        report_text += '  Correctness confidence: ' + str(questiondict['correctConf']) + '\n'
        report_text += '  Evaluation confidence: ' + str(questiondict['evalConf']) + '\n'
        report_text += '\n'

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
