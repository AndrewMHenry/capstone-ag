import tkinter as tk
import tkinter.ttk as ttk

from agtextui import get_letter_grade
from results import read_results

"""
Program organization adapted from StackOverflow question:
https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
(accepted answer by Bryan Oakley)
"""

EVAL_CONFIDENCE_THRESHOLD = 0.6


def get_scores(results):
    """Get list of student's question scores from results dict."""
    return [subdict['score'] for subdict in results['questions'].values()]


def get_fraction_correct(results):
    """Get student's total grade from results dict."""
    scores = get_scores(results)
    if not scores:
        raise ValueError('No scores found.')
    return sum(scores) / len(scores)


SAMPLE_GRADED_OUTPUT = 'saved-results/graded'


SUMMARY_COLUMNS = [
        dict(name='studentID', title='Student ID', anchor=tk.W),
        dict(name='scanOrder', title='Scan Order', anchor=tk.E),
        dict(name='numericalGrade', title='Numerical Grade', anchor=tk.E),
        dict(name='letterGrade', title='Letter Grade', anchor=tk.CENTER),
        ]

DETAIL_COLUMNS = [
        dict(name='question', title='Question', anchor=tk.E),
        dict(name='score', title='Score', anchor=tk.E),
        dict(
            name='evaluationConfidence',
            title='Evaluation Confidence',
            anchor=tk.E
            ),
        ]


class CustomTreeview(ttk.Treeview):

    def __init__(self, parent, columns):
        """Initialize CustomTreeview widget.

        parent -- the parent widget (as usual)
        columns -- a list of column descriptor dicts

        """
        super().__init__(parent)

        self['show'] = 'headings'
        self['columns'] = [column['name'] for column in columns]

        for column in columns:
            self.heading(column['name'], text=column['title'])
            self.column(column['name'], anchor=column['anchor'])

        try:
            getattr(self, 'columns')
        except AttributeError:
            pass
        else:
            raise RuntimeError('Treeview already has a `columns` member!')

        self.columns = list(columns)

    def insert(self, parent, index, tags=None, **kwargs):
        """ """
        values = [kwargs[column['name']] for column in self.columns]
        if tags is None:
            super().insert(parent, index, values=values)
        else:
            super().insert(parent, index, tags=tags, values=values)


class AutoGradeGui(tk.Frame):
    """Custom widget to implement AutoGrade GUI."""

    def __init__(self, parent, *args, **kwargs):
        """Initialize AutoGradeGui widget."""
        super().__init__(parent, *args, **kwargs)

        self.student_results = {}

        self.summary_label = tk.Label(self, text='Summary')
        self.detail_label = tk.Label(self, text='Details')
        self.summary_treeview = CustomTreeview(self, SUMMARY_COLUMNS)
        self.detail_treeview = CustomTreeview(self, DETAIL_COLUMNS)

        self.detail_treeview.tag_configure('lowConfidence', foreground='red')

        self.summary_label.grid(column=0, row=0, sticky='NSEW')
        self.summary_treeview.grid(column=0, row=1, sticky='NSEW')
        self.detail_label.grid(column=1, row=0, sticky='NSEW')
        self.detail_treeview.grid(column=1, row=1, sticky='NSEW')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def read_graded_output(self, graded_output):
        """Read information in graded output and add it to GUI."""
        results = read_results(graded_output)
        studentID = results['name']
        self.student_results[studentID] = results

        numericalGrade = 100 * get_fraction_correct(results)
        letterGrade = get_letter_grade(numericalGrade)
        scanOrder = str(len(self.student_results))

        self.summary_treeview.insert(
                '', 0,
                studentID=studentID,
                numericalGrade=numericalGrade,
                letterGrade=letterGrade,
                scanOrder=scanOrder
                )

        for question, data in results['questions'].items():

            score = data['score']
            evaluationConfidence = data['evalConf']

            if evaluationConfidence < EVAL_CONFIDENCE_THRESHOLD:
                tags = 'lowConfidence'
            else:
                tags = ()

            self.detail_treeview.insert(
                    '',
                    'end',
                    tags=tags,
                    question=question,
                    score=str(score),
                    evaluationConfidence=str(evaluationConfidence),
                    )



if __name__ == '__main__':
    root = tk.Tk()
    root.title('AutoGrade')

    gui = AutoGradeGui(root)
    gui.read_graded_output(SAMPLE_GRADED_OUTPUT)
    gui.pack(fill='both', expand='true')
    root.mainloop()
