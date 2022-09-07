"""List of cost model parameters."""

params = {
    "wages": {
        "blockchain_dev": 75 + 1,
        "front_end_dev": 40 + 1,
        "human_resources": 35 + 1,
    },
    # Bounties used to attract initial protocol users.
    "bounty_subsidising": 100000,
    "buffer": 100000,  # Buffer to take unknown costs into account.
    "daily_operational_costs": 200,
    "days_to_operational_break-even": 270,
}


# pylint: disable=R0902
class Cost_model:
    """Computes the total costs."""

    # pylint: disable=R0913
    def __init__(
        self,
        parent_costs: dict,
        the_params: dict,
    ):

        self.parent_costs = parent_costs
        self.operational_costs: int = (
            the_params["daily_operational_costs"]
            * the_params["days_to_operational_break-even"]
        )
        (
            self.total_costs,
            the_params["labour_costs"],
        ) = self.total_costs_to_dict(the_params)

        the_params["total_cost"] = self.compute_total_cost()
        the_params["non_labour_costs"] = (
            the_params["total_cost"] - the_params["labour_costs"]
        )

        dict_to_latex_table(
            "latex/Tables/total_costs_table.tex",
            self.total_costs,
            "Description",
            r"Cost [\euro]",
            "Total Expected Investment Costs",
        )

    def total_costs_to_dict(self, the_params):
        """Generates a dictionary including all expected project costs."""
        total_costs = {}
        labour_costs = 0

        # Get the order of the parent actities.
        order = []
        for key in self.parent_costs.keys():
            order.append(key)
        # The stored total costs are cumulative costs, so subtract the costs of
        # the previous parent to get the actual costs of the parent.
        for i, key in enumerate(order):
            if i == 0:
                total_costs[key.description] = self.parent_costs[key]
            else:
                total_costs[key.description] = (
                    self.parent_costs[key] - self.parent_costs[order[i - 1]]
                )
            labour_costs = labour_costs + total_costs[key.description]

        total_costs["Bounty Subsidising"] = the_params["bounty_subsidising"]
        total_costs["Buffer"] = the_params["buffer"]
        total_costs["Operational Costs"] = self.operational_costs
        return total_costs, labour_costs

    def compute_total_cost(self):
        """Generates the expected summed total costs."""
        total_cost = 0
        for value in self.total_costs.values():
            if isinstance(value, tuple):
                total_cost = total_cost + int(value[0])
            else:
                total_cost = total_cost + int(value)
        return total_cost


def dict_to_latex_table(
    filepath: str,
    the_params: dict,
    key_header: str,
    value_header: str,
    caption: str,
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
    \\caption{{{caption}\\label{{table:nonlin}}}}\\\\
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
