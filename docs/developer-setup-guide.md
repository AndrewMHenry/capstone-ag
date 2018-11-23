# Setup

## Step 1: Obtain Python 3

If Python 3 is not already on your system, I would recommend
searching the web for "Python 3" and your operating system.
This should point you in the right direction for finding
install instructions.

## Step 2: Set up a virtual environment

In my experience, installing Python projects is easiest using
a virtual environment.  A virtual environment is a directory
that contains a copy of the Python interpreter and allows you
to install Python packages locally without affecting the rest
of your system.  These instructions are based on the full
tutorial found [here](https://docs.python.org/3/tutorial/venv.html).

The first step is to creating a virtual environment is finding
a place to put it.  I put my virtual environments in an
`envs` directory under my home directory (`~`), but the
specific location does not matter as long as
you have write permission there.  If you have not made virtual
environments before, I would recommend making a new directory
just for storing virtual environments.

The next step is to create the virtual environment.  To do
this, open a terminal, change directory to your virtual
environments directory, and run
```
python3 -m venv capstone-ag
```
In this example, `capstone-ag` is the name of the created
virtual environment, so you should now be able to see
a `capstone-ag` directory in your directory of virtual
environments.

The last step is to *activate* the virtual environment.
To activate your virtual environment, change directory
into `capstone-ag` and do one of the following, based
on your operating system:

### Windows:
Run `Scripts\activate.bat`.

### Linux/MacOS:
Run `source bin/activate`.

Your terminal prompt should change to reflect the fact that
you have activated the virtual environment.  *Note*: The
virtual environment has only been activated in the current
terminal; to use your environment in a new terminal, you
will have to activate it again there.

## Step 3: Download repository and install AutoGrade
To download this repository, clone it by running
```
git clone https://github.com/AndrewMHenry/capstone-ag
```
With your virtual environment activated, run
```
pip install -e .
```
from the cloned `capstone-ag` directory.  The `.` means
`pip` will install the `autograde` package from the current
directory (using `setup.py`), and the `-e` means that the
installed code will change as you modify the code in the
repository.
