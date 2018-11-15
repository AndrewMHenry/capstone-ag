"""Implementation of data format for AG-Laptop transfers."""
import collections

ANSWER_ATTRIBUTES = 'question score evaluation_confidence'

Answer = collections.namedtuple('Answer', ANSWER_ATTRIBUTES)


"""Converting text to answers................................"""

def _split(text, sep, count=None):
    """Return tuple of stripped parts separated by sep."""
    parts = text.split(sep)
    if count is not None and len(parts) != count:
        raise SyntaxError(
                'Expected exactly {} instance(s) of `{}`'.format(count, sep))
    return tuple([part.strip() for part in parts])


def parse_answer(line):
    """Return Answer object parsed from the line of text."""
    header, data = _split(line, ':', 2)
    label, question = _split(header, ' ', 2)

    attributes = {'question': question}
    for definition in _split(data, ';'):
        attribute, value = _split(definition, '=', 2)
        attributes[attribute] = value

    return Answer(**attributes)


def read_answers(filename):
    """Return list of Answer objects from file."""
    with open(filename, 'r') as answerfile:
        lines = list(answerfile)
    return [parse_answer(line) for line in lines]


"""Converting answers to text................................"""

def format_definition(attribute, value):
    """Return fragment of answer line assigning value to attribute."""
    return '{}={}'.format(attribute, value)


def format_answer(answer):
    """Return line of text representing the Answer object."""
    definitions = [
            format_definition(attribute, value)
            for attribute, answer[attribute]
            in ANSWER_ATTRIBUTES]
    return 'answer {}: {}\n'.format(answer.question, definitions)


def write_answers(filename, answers):
    """Write list of answers to file."""
    answer_lines = [format_answer(answer) for answer in answers]
    with open(filename, 'w') as outfile:
        outfile.write(''.join(answer_lines))
