import os
import paramiko
from paramiko import SSHClient
import scp
import shutil
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font

from agtextui import get_letter_grade
from results import read_results, write_results
from transfer_file import transfer, send
from transfer_file import REMOTE_HOST_IP, USERNAME, PASSWORD

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




GO_COMMAND = 'cd capstone-ag/autograde; ./our_python autograde_toplevel.py'


ID_PREFIX = '#'


COPY_PERIOD_MS = 1000


USE_LOCAL_SOURCE = False

REMOTE_BASE = 'capstone-ag/autograde/'

NUM_QUESTIONS = 10

"""on-laptop locations"""
DESTINATION_FILE = 'input/graded.json'
ANSWER_KEY_FILE = 'output/answer_key.json'

"""dummy local locations"""
LOCAL_SOURCE_FILE = 'graded.json'
LOCAL_ANSWER_KEY_FILE = 'answer_key.json'

"""actual remote locations"""
REMOTE_SOURCE_FILE = REMOTE_BASE + 'graded.json' # SHOULD PHASE OUT!
REMOTE_ANSWER_KEY_FILE = REMOTE_BASE + 'answer_key.json'


"""TO BE REMOVED REMOTELY!"""
REMOTE_GRADED_FILE = REMOTE_BASE + 'graded.json'
REMOTE_AI_FILE = REMOTE_BASE + 'aiOut.json'
REMOTE_SCANNED_FILE = REMOTE_BASE + 'scannedPFAS'
REMOTE_FILES = ' '.join([REMOTE_GRADED_FILE, REMOTE_AI_FILE, REMOTE_SCANNED_FILE])
REMOTE_RM_COMMAND = 'rm ' + REMOTE_FILES


def receive_single_graded_file(destination):
    """Copy a single graded results file to path destination."""
    if USE_LOCAL_SOURCE:
        shutil.copyfile(LOCAL_SOURCE_FILE, DESTINATION_FILE)
    else:
        try:
            transfer(REMOTE_SOURCE_FILE, DESTINATION_FILE)
        except scp.SCPException as e:
            print('SOILED IT! ({})'.format(e))
        else:
            print('FOUND IT!')


def send_answer_key_file(source):
    """Copy answer key file `source` to remote board."""
    if USE_LOCAL_SOURCE:
        shutil.copyfile(source, LOCAL_ANSWER_KEY_FILE)
    else:
        send(source, REMOTE_ANSWER_KEY_FILE)


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
        dict(name='answer', title='Answer', anchor=tk.E),
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
        """Call super() insert with convenient value specifications."""
        values = [kwargs[column['name']] for column in self.columns]
        if tags is None:
            return super().insert(parent, index, values=values)
        else:
            return super().insert(parent, index, tags=tags, values=values)

    def clear_all(self):
        """Clear all entries!"""

        # from StackOverflow!
        self.delete(*self.get_children())

class AnswerKeyWidget(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        """Initialize AnswerKeyWidget."""
        super().__init__(parent, *args, **kwargs)
        self.labels = [
                self.create_question_label(question_number)
                for question_number in range(NUM_QUESTIONS)
                ]
        self.entries = [
                tk.Entry(self)
                for i in range(NUM_QUESTIONS)
                ]
        self.save_button = tk.Button(
                self,
                text='Save and apply',
                command=self.apply_answer_key
                )

        for row in range(NUM_QUESTIONS):
            self.labels[row].grid(row=row, column=0, sticky='NSEW')
            self.entries[row].grid(row=row, column=1, sticky='NSEW')
        self.save_button.grid(
                row=NUM_QUESTIONS, column=0, columnspan=2, sticky='NSEW'
                )

    def create_question_label(self, question_number):
        """Create and return question label for 0-based question number."""
        question_name = self.get_question_name(question_number)
        label_text = 'Question {}.'.format(question_name)
        return tk.Label(self, text=label_text)

    def get_question_name(self, question_number):
        """Get name of question from 0-based question_number."""
        return str(question_number + 1)

    def create_answer_key(self):
        """Return answer key data structure."""
        answer_key = {}
        for question_number in range(NUM_QUESTIONS):
            question_name = self.get_question_name(question_number)
            entry = self.entries[question_number]
            answer_key[question_name] = entry.get()

        return answer_key

    def apply_answer_key(self):
        """Callback to save and send answer key."""
        write_results(ANSWER_KEY_FILE, self.create_answer_key())
        send_answer_key_file(ANSWER_KEY_FILE)


class AutoGradeGui(tk.Frame):
    """Custom widget to implement AutoGrade GUI."""

    def __init__(self, parent, *args, **kwargs):
        """Initialize AutoGradeGui widget."""
        super().__init__(parent, *args, **kwargs)

        self.student_results = {}
        self.student_summary_ids = {}

        self.summary_label = tk.Label(self, text='Summary')
        self.detail_label = tk.Label(self, text='Details')
        self.answer_label = tk.Label(self, text='Answer Key')
        self.summary_treeview = CustomTreeview(self, SUMMARY_COLUMNS)
        self.detail_treeview = CustomTreeview(self, DETAIL_COLUMNS)
        self.answer_key = AnswerKeyWidget(self)

        self.summary_treeview.bind(
                '<<TreeviewSelect>>',
                self.handle_summary_treeview_selection
                )

        self.detail_treeview.tag_configure('lowConfidence', foreground='red')

        self.button_frame = tk.Frame(self)
        self.go_button = tk.Button(self.button_frame, text='GO', fg='green', command=self.go)
        self.stop_button = tk.Button(self.button_frame, text='STOP', fg='red', command=self.stop)
        self.clear_button = tk.Button(self.button_frame, text='CLEAR', fg='blue', command=self.clear)

        self.summary_label.grid(column=0, row=0, sticky='NSEW')
        self.summary_treeview.grid(column=0, row=1, sticky='NSEW')
        self.detail_label.grid(column=0, row=2, sticky='NSEW')
        self.detail_treeview.grid(column=0, row=3, sticky='NSEW')
        self.answer_label.grid(column=1, row=0, sticky='NSEW')
        self.answer_key.grid(column=1, row=1, rowspan=1, sticky='NSEW')
        self.button_frame.grid(column=1, row=2, rowspan=1, sticky='NSEW')

        self.go_button.grid(column=0, row=0, sticky='NSEW')
        self.stop_button.grid(column=1, row=0, sticky='NSEW')
        self.clear_button.grid(column=2, row=0, sticky='NSEW')
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        #self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.update_results()

    def go(self):
        """Start pipeline running on processing unit."""
        ssh.exec_command(GO_COMMAND)

    def stop(self):
        """Stop pipeline running on processing unit."""
        ssh.exec_command('touch capstone-ag/autograde/quit')

    def clear(self):
        """Clear entries and pipeline."""
        print('CLEARING!!!')
        for tv in [self.summary_treeview, self.detail_treeview]:
            tv.clear_all()
        self.detail_label.config(text='Details')

        self.student_results.clear()
        self.student_summary_ids.clear()

        ssh.exec_command(REMOTE_RM_COMMAND)
        os.remove(DESTINATION_FILE)

    def update_results(self):
        """Get and add new results, and schedule to repeat periodically."""
        try:
            receive_single_graded_file(DESTINATION_FILE)
            self.read_graded_output_file(DESTINATION_FILE)
        except FileNotFoundError:
            pass
        self.after(COPY_PERIOD_MS, self.update_results)


    def read_graded_output(self, results):
        """Read information in graded output dict and add it to GUI.

        The new output is not added if it corresponds to an already-
        stored studentID.

        """
        studentID = results['StudentID']['answer']

        if studentID in self.student_results:
            return

        self.student_results[studentID] = results

        numericalGrade = 100 * get_fraction_correct(results)
        letterGrade = get_letter_grade(numericalGrade)
        scanOrder = str(len(self.student_results))

        self.student_summary_ids[studentID] = self.summary_treeview.insert(
                '', 'end',
                studentID=ID_PREFIX+studentID,
                numericalGrade=numericalGrade,
                letterGrade=letterGrade,
                scanOrder=scanOrder,
                )

        self.show_student_details(studentID)

    def read_graded_output_file(self, graded_output_file):
        """Read information in graded output and add it to GUI."""
        self.read_graded_output(read_results(graded_output_file))

    def show_student_details(self, studentID):
        """Show details for student with given ID.

        (Initial delete inspired by top answer to StackOverflow question 22812134)

        """
        self.detail_treeview.delete(*self.detail_treeview.get_children())
        try:
            question_items = self.student_results[studentID]['questions'].items()
        except KeyError as e:
            print(self.student_results)
            raise e
        for question, data in question_items:

            score = data['score']
            evaluationConfidence = data['min_conf']
            answer = data['answer']

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
                    evaluationConfidence='{:.2f}'.format(evaluationConfidence),
                    answer=answer,
                    )

        self.detail_label.config(text='Details for ' + studentID)

    def handle_summary_treeview_selection(self, event):
        """Event handler to print studentID for focused student.

        This method is designed to be bound to the <<TreeviewSelect>>
        event of the summary_treeview.  When the selection status of
        that Treeview changes, this method shows the details for
        the currently selected student.

        """
        item = self.summary_treeview.item(self.summary_treeview.focus())
        studentID = str(item['values'][0])[len(ID_PREFIX):]
        self.show_student_details(studentID)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('AutoGrade')

    gui = AutoGradeGui(root)

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(REMOTE_HOST_IP, username=USERNAME, password=PASSWORD)

    gui.clear()
    stdin, stdout, stderr = ssh.exec_command(GO_COMMAND)

    gui.pack(fill='both', expand='true')
    root.mainloop()

