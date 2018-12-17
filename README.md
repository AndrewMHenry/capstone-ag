![AutoGrade Logo](logo/logo.png)

# Introduction

Welcome to Team AutoGrade's Capstone project repository!
Team AutoGrade (or Team AG) consists of Kayla Carrigan,
Andrew Henry, Yvonne Kamdem, Barrett Marsh, and Caroline Nseir.

# Documentation Links

- [Developer Setup Instructions](docs/developer-setup-guide.md)

# Demo Instructions

Once all the necessary dependencies are installed, the following
procedure can be used to demonstrate the current state of the
AutoGrade project:

- Starting from the top-level repository directory (`capstone-ag`),
  change directory into `autograde`.

- Open a new termial (by using CTRL+SHIFT+N), and
  start the top-level script in the new terminal by
  running

      python3 autograde_toplevel.py

- Return to the original terminal and place a PFAS image sample directly
  in the autograde directory to
  kick off the entire AutoGrade process.  In particular, to use the primary
  demo PFAS as the input image, run

      cp samples/PFAS_demo_sample.PNG .

  You should see text output in the other terminal, ending with the final
  grade report.  Typical
  grade values are around 40%, but there is considerable variability in the
  accuracy, with values as low as 10% or (rarely) as high as 80%, although
  even values outside this range may be possible.
  You can repeat the process by copying the file again as many times as
  you like.

- To close the original terminal, press CTRL+D.  In the other terminal,
  first stop the top-level script by interrupting it with CTRL+C
  and then close that terminal with CTRL+D.
