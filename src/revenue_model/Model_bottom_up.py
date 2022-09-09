"""The bottom up model that computes the TAM and TSM."""


# pylint: disable=R0903
class Model_bottom_up:
    """Basic bottom up model model."""

    def __init__(self, bottom_up_market):
        self.company_cost_reduction = (
            bottom_up_market.nr_of_units
            * bottom_up_market.unit_costs
            * bottom_up_market.cost_reduction_per_unit_percentage
        )
        self.serviceable_cost_reduction = (
            self.company_cost_reduction
            * bottom_up_market.market_servicable_fraction
        )
        self.trucol_revenue = (
            self.serviceable_cost_reduction
            * bottom_up_market.cut_on_cost_reduction_for_trucol
        )

    def addTwo(self, x):
        """adds two to the incoming integer and returns the result of the
        computation."""
        return x + 2


# pylint: disable=R0903
class Bottom_up_logistics:
    """TODO: Ask expert advice on generating accurate estimates."""

    def __init__(self):
        self.nr_of_units = 5 * 10**6  # TODO: update nr.
        self.unit_costs = 2  # dollar
        self.cost_reduction_per_unit_percentage = 0.1
        self.market_servicable_fraction = 0.01
        self.units_impactable_by_trucol = (
            self.nr_of_units * self.market_servicable_fraction
        )
        # Assume 5 % of the cost reduction can be payed for TruCol services.
        self.cut_on_cost_reduction_for_trucol = 0.05
