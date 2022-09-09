"""The bottom up model that computes the TAM and TSM."""


# pylint: disable=R0903
class Model_bottum_up:
    """Placeholder for model."""

    def __init__(self,bottom_up_market):
        yearly_revenue=(
            bottom_up_market.nr_of_units*bottom_up_market.unit_costs*bottum_up_market.cost_reduction_per_unit_percentage

    def addTwo(self, x):
        """adds two to the incoming integer and returns the result of the
        computation."""
        return x + 2


# pylint: disable=R0903
class Bottum_up_logistics:
    """Placeholder for model."""

    def __init__(self):
        self.nr_of_units=5*10**6 # TODO: update nr.
        self.unit_costs=2 # dollar
        self.cost_reduction_per_unit_percentage=0.1
        self.market_servicable_fraction=0.01
        self.units_impactable_by_trucol=self.nr_of_units*self.market_servicable_fraction
        self.cut_on_cost_reduction_for_trucol=0.05 # Assume 5 % of the cost reduction can be payed for TruCol services.
        

    def addTwo(self, x):
        """adds two to the incoming integer and returns the result of the
        computation."""
        return x + 2