import tkinter as tk
import tkinter.ttk as ttk

from agtextui import generate_report, get_letter_grade
from results import read_results

"""
Program organization adapted from StackOverflow question:
https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
(accepted answer by Bryan Oakley)
"""

EVAL_CONFIDENCE_THRESHOLD = 0.6

def read_file(filename):
    """Return contents of file."""
    with open(filename, 'r') as f:
        source = f.read()
    return source


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
SAMPLE_REPORT = generate_report(SAMPLE_GRADED_OUTPUT)

SAMPLE_RESULTS = read_results(SAMPLE_GRADED_OUTPUT)

class AutoGradeGui(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        """ """
        super().__init__(parent, *args, **kwargs)

        self.summary_label = tk.Label(self, text='Summary')
        self.summary_label.grid(column=0, row=0, sticky='NSEW')

        self.summary_treeview = ttk.Treeview(self)
        self.summary_treeview['show'] = 'headings'
        self.summary_treeview['columns'] = ('studentID', 'numericalGrade', 'letterGrade')
        self.summary_treeview.heading('#1', text='Student ID')
        self.summary_treeview.heading('#2', text='Numerical Grade')
        self.summary_treeview.heading('#3', text='Letter Grade')
        self.summary_treeview.column('#2', anchor=tk.E)
        self.summary_treeview.column('#3', anchor=tk.CENTER)
        self.summary_treeview.grid(column=0, row=1, sticky='NSEW')

        self.detail_label = tk.Label(self, text='Details')
        self.detail_label.grid(column=1, row=0, sticky='NSEW')

        self.detail_treeview = ttk.Treeview(self)
        self.detail_treeview['show'] = 'headings'
        self.detail_treeview['columns'] = ('question', 'score', 'evaluationConfidence')
        self.detail_treeview.heading('#1', text='Question')
        self.detail_treeview.heading('#2', text='Score')
        self.detail_treeview.heading('#3', text='Evaluation Confidence')
        self.detail_treeview.column('#1', anchor=tk.E)
        self.detail_treeview.column('#2', anchor=tk.E)
        self.detail_treeview.column('#3', anchor=tk.E)
        self.detail_treeview.tag_configure('lowConfidence', foreground='red')
        self.detail_treeview.grid(column=1, row=1, sticky='NSEW')

        self.textbox = tk.Text(self)
        self.textbox.config(state='disabled')
        #self.textbox.grid(column=2, row=1, sticky='NSEW')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        #self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def read_graded_output(self, graded_output):
        """Read information in graded output and add it to GUI."""
        self.textbox.config(state='normal')
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, generate_report(graded_output))
        self.textbox.config(state='disabled')

        results = read_results(graded_output)

        studentID = results['name']
        numericalScore = 100 * get_fraction_correct(results)
        letterGrade = get_letter_grade(numericalScore)

        self.summary_treeview.insert(
                '',
                0,
                values=(studentID, numericalScore, letterGrade)
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
                    values=(question, str(score), str(evaluationConfidence)),
                    tags=tags
                    )



if __name__ == '__main__':
    root = tk.Tk()
    root.title('AutoGrade')

    gui = AutoGradeGui(root)
    gui.read_graded_output(SAMPLE_GRADED_OUTPUT)
    gui.pack(fill='both', expand='true')
    root.mainloop()
