from results import read_results
import json

CONFIDENCE_THRESHOLD = 0.6


LETTER_GRADES = 'A B C D'.split()
LETTER_GRADE_FAIL = 'F'
LETTER_GRADE_THRESHOLDS = [90, 80, 70, 60]

def get_letter_grade(grade):
    """Return letter grade for numerical grade (0-100)."""
    for letter, threshold in zip(LETTER_GRADES, LETTER_GRADE_THRESHOLDS):
        if grade >= threshold:
            return letter
    return LETTER_GRADE_FAIL


def percentage(fraction):
    """Return a string representing fraction as a percentage."""
    return '{:.2f}%'.format(fraction * 100)


def generate_report(filename):
    """
    TODO: What data exactly do we get from grading results?

    Return a string with the report text.
    """
    results = read_results(filename)

    questions = results['questions']
    numquestions = len(questions)
    numcorrect = sum([subdict['score'] for subdict in questions.values()])
    fractioncorrect = numcorrect / numquestions


    # turn myobject into our report text
    report_text = '\n'
    report_text += (
            results['name']
            + ' got a grade of '
            + percentage(fractioncorrect)
            + ' (' + get_letter_grade(100 * fractioncorrect) + ')'
            + '\n')
    report_text += '-' * 37 + '\n'
    report_text += '\n'

#    for question, questiondict in questions.items():
#        report_text += (
#                'Our confidence that question '
#                + question
#                + ' is correct is '
#                + str(questiondict['correctConf'])
#                + '.')
#
#        if questiondict['evalConf'] < CONFIDENCE_THRESHOLD:
#            report_text += ' [LOW EVALUATION CONFIDENCE]'
#        report_text += '\n'
#
#    report_text += '\n'

    for question, questiondict in questions.items():
        report_text += 'Question ' + question + ':\n'
        report_text += '  Correctness confidence: ' + percentage(questiondict['correctConf']) + '\n'
        report_text += '  Evaluation confidence: ' + percentage(questiondict['evalConf']) + '\n'

        if questiondict['evalConf'] < CONFIDENCE_THRESHOLD:
            report_text += '  [LOW EVALUATION CONFIDENCE]\n'

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

    # extend to multiple files:
    print(generate_report(args.filename))

if __name__ == '__main__':
    main()
