"""Exports the parameters to a latex table, and to latex variables."""
from pprint import pprint

from src.export_data.helper_dir_file_edit import overwrite_file


def export_params_to_latex_params_and_table(params: dict, subpath, label):
    """Exports the parameters to latex parameters."""
    apply_scientific_notation(params)
    param_lines = get_latex_param_lines(params)
    print(f"param_lines={param_lines}")

    # Export parameters to file.
    overwrite_file(f"{subpath}_params.tex", param_lines)

    # Export the incoming parameters to Latex table:
    dict_to_latex_table(
        f"{subpath}_params_table.tex",
        params,
        "Parameter",
        "Value",
        (
            r"Cost Model Parameters in \euro (/hr or absolute, unless"
            + "specified otherwise)"
        ),
        label=label,
    )


def apply_scientific_notation(some_dict):
    """Makes numbers more readable by applying e notation for too small and too
    large numbers.

    Also rounds to 6 decimals.
    """
    for key, value in some_dict.items():
        some_dict[key] = truncate(value, 6)
        # some_dict[key]=format_number(value)
        if value < 0.00001 or value > 10000:
            some_dict[key] = f"{value:e}"
    return some_dict


def truncate(n, decimals=0):
    """Rounds to 6 decimals."""
    multiplier = 10**decimals
    return int(n * multiplier) / multiplier


def get_latex_param_lines(params):
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


# pylint: disable=R0913
def dict_to_latex_table(
    filepath: str,
    the_params: dict,
    key_header: str,
    value_header: str,
    caption: str,
    label: str,
):
    """Writes a dict to a latex file.

    :param the_params: dict:
    :param key_header: str:
    :param value_header: str:
    :param caption: str:
    """
    tuples = dict_to_latex_tuples(the_params)

    with open(filepath, "w", encoding="utf-8") as f:
        backreturn = "\\\\\n" + " " * 4

        content = backreturn.join(
            [f"{_tuple[0]} & {_tuple[1]}" for _tuple in tuples]
        )

        f.write(
            f"""
\\begin{{longtable}}{{@{{}}cp{{.7\\textwidth}}@{{}}}}
    \\caption{{{caption}}}\\label{{tab:{label}}}\\\\
    \\toprule
    {{\\bfseries {key_header}}} & {{\\bfseries {value_header}}} \\\\ \\midrule
    \\endfirsthead
    \\caption{{{caption} (continued)}}\\\\
    \\toprule
    \\multicolumn{{2}}{{l}}{{\\scriptsize\\emph{{\\ldots{{}} continued}}}}\\\\
    {{\\bfseries {key_header}}} & {{\\bfseries {value_header}}} \\\\ \\midrule
    \\endhead
    \\multicolumn{{2}}{{r}}{{\\scriptsize\\emph{{to be continued\\ldots}}}}\\\\
    \\bottomrule
    \\endfoot
    \\bottomrule
    \\endlastfoot
    {content}\\\\
\\end{{longtable}}
    """.strip()
        )


def flatten_dict(some_dict: dict):
    """Flattens a dict that contains values and dicts.

    :param some_dict: dict:
    """
    flat_dict = {}
    # Flatten dict
    for key, value in some_dict.items():
        if isinstance(value, dict):
            for newKey, newValue in value.items():
                flat_dict[newKey] = newValue
        else:
            flat_dict[key] = value
    return flat_dict


def dict_to_latex_tuples(some_dict: dict):
    """Converts a dict to a list of key,value tuples without underscores.

    :param some_dict: dict:
    """
    flat_dict = flatten_dict(some_dict)
    tuples = []
    for key, value in flat_dict.items():
        if isinstance(key, str):
            key = key.replace("_", " ")
            key = key.replace("&", r"\&")
        if isinstance(value, str):
            value = value.replace("_", " ")
            value = value.replace("&", r"\&")
        tuples.append((key, value))
    return tuples
