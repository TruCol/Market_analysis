"""File used to export data to latex."""
from pprint import pprint

from src.Cost_model import dict_to_latex_table
from src.export_data.create_dynamic_diagrams import create_dynamic_diagrams
from src.export_data.create_static_diagrams import create_static_diagrams
from src.export_data.Hardcoded_data import Hardcoded_data
from src.export_data.helper_dir_file_edit import overwrite_file
from src.export_data.latex_compile import compile_latex
from src.export_data.latex_export_code import export_code_to_latex


def export_data(args, params):
    """Parses the Python arguments that specify what should be compiled.

    :param args:
    """

    hd = Hardcoded_data()

    param_lines = export_latex_params(params)
    print(f"param_lines={param_lines}")

    # Export parameters to file.
    overwrite_file("latex/Tables/params.tex", param_lines)

    # Export model parameters to Latex table:
    dict_to_latex_table(
        "latex/Tables/params_table.tex",
        params,
        "Parameter",
        "Value",
        (
            r"Cost Model Parameters in \euro (/hr or absolute, unless"
            + "specified otherwise)"
        ),
    )

    # Generating PlantUML diagrams
    create_dynamic_diagrams(args, hd)
    create_static_diagrams(args, hd)

    # Plotting graphs using Python code, and export them to latex.
    # Generate plots.
    # Export plots to LaTex.

    # Export code to LaTex.
    if args.c2l:
        # TODO: verify whether the latex/{project_name}/Appendices folder
        # exists before exporting.
        # TODO: verify whether the latex/{project_name}/Images folder exists
        # before exporting.
        export_code_to_latex(hd, False)
    elif args.ec2l:
        # TODO: verify whether the latex/{project_name}/Appendices folder
        # exists before exporting.
        # TODO: verify whether the latex/{project_name}/Images folder exists
        # before exporting.
        export_code_to_latex(hd, True)

    # Compile the accompanying LaTex report.
    if args.l:
        compile_latex(True, True)
        print("")
    print("\n\nDone exporting data.")


def export_latex_params(params):
    """Exports the model parameters and computed values to LaTex variables."""
    # Export model parameters to .tex file with LaTex variables.
    param_lines = []
    # TODO: flatten dict
    # print(f'params={params}')
    pprint(params)

    for key, value in params.items():
        if key == "wages":
            for wages_key, wages_value in params[key].items():
                param_lines.append(
                    "\\newcommand"
                    + chr(92)
                    + str(wages_key.replace("_", ""))
                    + "{"
                    + str(wages_value)
                    + "}"
                )
        else:
            param_lines.append(
                "\\newcommand"
                + chr(92)
                + str(key.replace("_", "").replace("-", ""))
                + "{"
                + str(value)
                + "}"
            )
    return param_lines
