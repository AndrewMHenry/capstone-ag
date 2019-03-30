import argparse
import os
import random

from results import write_results


FILENAME_FORMAT = 'graded_{}.json'
NUM_SAMPLES = 10


NUM_QUESTIONS = 10
QUESTIONS = [str(number) for number in range(1, NUM_QUESTIONS + 1)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('destdir')
    args = parser.parse_args()

    qualified_format = os.path.join(args.destdir, FILENAME_FORMAT)
    for samplenum in range(NUM_SAMPLES):
        filename = qualified_format.format(samplenum)
        results = {'name': 'student {}'.format(samplenum)}
        results['questions'] = {
                question: {
                    'score': random.randint(0, 1),
                    'evalConf': random.random()
                    }
                for question in QUESTIONS
                }
        write_results(filename, results)
