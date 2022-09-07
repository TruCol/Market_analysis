from .Main import Main
from .Model_top_down import Model_top_down

print(
    f"Hi, I'll be running the main code, and I'll let you know when I'm done."
)
project_nr = 1
main = Main()

# run monte-carlo for revenue estimation
model = Model_top_down(project_nr)


# export the code to latex
main.export_code_to_latex(project_nr)

# compile the latex report
main.compile_latex_report(project_nr)

print(f"Done.")
