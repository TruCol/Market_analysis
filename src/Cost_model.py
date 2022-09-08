"""List of cost model parameters."""

from src.export_data.export_params_to_latex import dict_to_latex_table

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

        # Writes the costs model parameters to latex table.
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
