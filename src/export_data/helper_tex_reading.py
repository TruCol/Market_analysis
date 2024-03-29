"""Helper script to parse Latex files, to support including LaTex
appendices."""
from src.export_data.helper_dir_file_edit import file_contains


def verify_latex_supports_auto_generated_appendices(path_to_main_latex_file):
    """Ensures the Latex file supports including automatically appending code
    as appendices.

    :param path_to_main_latex_file:
    """
    # TODO: change verification to complete tex block(s) for appendices.
    # TODO: Also verify related boolean and if statement creations.
    determining_overleaf_home_line = (
        r"\def\overleafhome{/tmp}% change as appropriate"
    )
    begin_apendices_line = "\\begin{appendices}"
    print(f"determining_overleaf_home_line={determining_overleaf_home_line}")
    print(f"begin_apendices_line={begin_apendices_line}")

    if not file_contains(
        path_to_main_latex_file, determining_overleaf_home_line
    ):
        raise Exception(
            f"Error, {path_to_main_latex_file} does not contain:\n\n"
            + f"{determining_overleaf_home_line}\n\n so this Python code "
            + "cannot export the code as latex appendices."
        )
    if not file_contains(
        path_to_main_latex_file, determining_overleaf_home_line
    ):
        raise Exception(
            f"Error, {path_to_main_latex_file} does not contain:\n\n"
            + f"{begin_apendices_line}\n\n so this Python code cannot export"
            "the code as latex appendices."
        )
