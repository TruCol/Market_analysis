import os
from .Main import Main

print(f"Hi, I'll be running the main code, and I'll let you know when I'm done.")
project_nr = 1
main = Main()

# export the code to latex
main.export_code_to_latex(project_nr)

# compile the latex report
main.compile_latex_report(project_nr)

print(f"Done.")
