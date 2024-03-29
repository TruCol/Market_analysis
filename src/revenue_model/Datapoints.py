"""The bottom up model that computes the TAM and TSM."""


# pylint: disable=R0902


class Datapoints:
    """Initialise the datapoints and compute basic datapoints that can be
    derived from the datapoints and/or assumptions."""

    def __init__(self):
        # Source: https://www.dpdhl.com/content/dam/dpdhl/en/media-center/
        # investors/documents/annual-reports/DPDHL-2019-Annual-Report.pdf
        self.profit_dhl_billion = 4.1  # billion dollar
        self.profit_dhl = self.profit_dhl_billion * 10**9  # dollar

        # Source:
        self.profit_fedex_billion = 1.29  # billion dollar
        self.profit_fedex = self.profit_fedex_billion * 10**9  # dollar
        # Source: https://investors.ups.com/_assets/
        # _67e21ed5c7d1164af5b2ef48cec32803/ups/db/1110/9465/annual_report/
        # UPS_2021_Proxy_Statement_and_2020_Annual_Report%3B_Form_10-K.pdf
        self.profit_ups_billion = 7.7  # billion dollar
        self.profit_ups = self.profit_ups_billion * 10**9  # dollar
        # Sum the profit of these three companies

        self.profit_dhl_fedex_ups_billion = (
            self.profit_dhl_billion
            + self.profit_fedex_billion
            + self.profit_ups_billion
        )
        self.profit_dhl_fedex_ups = (
            self.profit_dhl_fedex_ups_billion * 10**9
        )  # dollar

        # Assumption 7:McKinsey study showed 16% gain in profit in logistics
        # company through algo optimisation. It is assumed 0.1% is on average
        # an obtainable profit increase by means of algo optimisation.
        self.avg_algo_optimisation_profit_percentage = 0.1
        self.avg_algo_optimisation_profit = (
            self.avg_algo_optimisation_profit_percentage / 100
        )

        # TruCol Cut
        self.TruCol_cut_on_profit_percentage = 1
        self.TruCol_cut_on_profit = self.TruCol_cut_on_profit_percentage / 100

        # sam and tam factors
        self.sam_factor = 0.003
        self.tam_factor = 0.004
        print(f"self.profit_dhl_fedex_ups={self.profit_dhl_fedex_ups}")

        # Source: https://www.cips.org/supply-management/news/2016/november/
        # logistics-industry-forecast-to-be-worth-155tn-by-2023/
        # NOTE: this article seems an unreliable source and is outdated,
        # hence the 0.15 should possibly be changed/updated.
        self.logistics_market_share_dhl_fedex_ups_percentage = 15
        self.logistics_market_share_dhl_fedex_ups = (
            self.logistics_market_share_dhl_fedex_ups_percentage / 100
        )

        self.datapoints_dict = {
            "profit_dhl_billion": self.profit_dhl_billion,
            "profit_dhl": self.profit_dhl,
            "profit_fedex_billion": self.profit_fedex_billion,
            "profit_fedex": self.profit_fedex,
            "profit_ups_billion": self.profit_ups_billion,
            "profit_ups": self.profit_ups,
            "profit_dhl_fedex_ups": self.profit_dhl_fedex_ups,
            "sam_factor": self.sam_factor,
            "tam_factor": self.tam_factor,
            "logistics_market_share_dhl_fedex_ups": (
                self.logistics_market_share_dhl_fedex_ups
            ),
            "logistics_market_share_dhl_fedex_ups_percentage": (
                self.logistics_market_share_dhl_fedex_ups_percentage
            ),
            "avg_algo_optimisation_profit_percentage": (
                self.avg_algo_optimisation_profit_percentage),
            "avg_algo_optimisation_profit": self.avg_algo_optimisation_profit,
            "TruCol_cut_on_profit_percentage": (
                self.TruCol_cut_on_profit_percentage),
            "TruCol_cut_on_profit": self.TruCol_cut_on_profit,
        }

        # Compute the remaining market share.
        self.logistics_market_share_remaining = (
            1 - self.logistics_market_share_dhl_fedex_ups
        )

        # Assume avg market profit per dollar market share is uniform.
        self.logistics_market_profit = self.get_logistics_market_profit()
        # print(f'logistics_market_profit={logistics_market_profit}')

        # Conservative estimate based on 0.16 demonstrated by McKinsey &
        # Company study.
        # Source: https://www.mckinsey.com/business-functions/
        # mckinsey-analytics/how-we-help-clients/algorithmic-route-optimization
        # -improves-revenue-for-a-logistics-company#
        self.profit_gain_by_trucol_protocol = 0.04

        # Estimate based on analogy where a good constraint modeller
        # can reach significant gains in algorithmic efficiency of solution.
        self.profit_gain_by_trucol_protocol_company = 0.002
        # Conservative estimate based on a max of 1.00, for companies
        # that intend to improve algorithmic efficiency without increasing
        # profit.
        self.fraction_of_profit_shared_with_trucol = 0.01

        # Source: Statistica.com or marketsandmarkets.com
        # TODO: re-find exact link
        self.logistics_market_size = 5.5 * 10**12
        # Source: Statistica.com or marketsandmarkets.com
        # TODO: re-find exact link
        self.algo_trading_market_size = 11.1 * 10**9
        # Source: Statistica.com or marketsandmarkets.com
        # TODO: re-find exact link
        self.material_sciences_market_size = 1 * 10**9
        # Source: Statistica.com or marketsandmarkets.com
        # TODO: re-find exact link
        self.pharmaceutics_market_size = 1.27 * 10**12
        # Source: Statistica.com or marketsandmarkets.com
        # TODO: re-find exact link
        self.telecommunications_market_size = 1.7 * 10**12

        logistics_profit_fraction = (
            self.logistics_market_profit / self.logistics_market_size
        )
        print(f"self.profit_dhl_fedex_ups={self.profit_dhl_fedex_ups}")
        print(f"self.logistics_market_size={self.logistics_market_size}")
        print(f"logistics_profit_fraction={logistics_profit_fraction}")

        # Compute and assume profit margins
        self.compute_profit_margins()  # for logistics sector the data is known
        self.assume_profit_margins()  # for other sectors the data is assumed.

        # Compute profit per market
        self.compute_market_profit()

    def get_logistics_market_profit(self):
        """The basic computation that is done here is a cross multiplication of
        (see pdf):

        0.15/0.85=profit-three-companies/profit-remainder.
        """
        net_profit_remainder = (
            self.profit_dhl_fedex_ups
            * self.logistics_market_share_remaining
            / self.logistics_market_share_dhl_fedex_ups
        )
        net_profit_logistics_market = (
            net_profit_remainder + self.profit_dhl_fedex_ups
        )
        return net_profit_logistics_market

    def get_market_profit(self, market_size, profit_margin):
        """Computes the total market profit."""
        return market_size * profit_margin

    def get_market_profit_margin(self, market_size, net_profit):
        """Computes the profit margin, presumably based on data points."""
        return net_profit / market_size

    def compute_profit_margins(self):
        """Computes the projected profit margin for the TruCol company for the
        logistics market."""
        # Compute the profit margin based on market size and profit.
        self.logistics_market_profit_margin = self.get_market_profit_margin(
            self.logistics_market_size, self.logistics_market_profit
        )

    def assume_profit_margins(self):
        """Assumes the profit margins for all sectors based on the assumptions
        in the accompanying market analysis pdf."""

        # Assume the profit margin in the algorithmic trading market equals
        # that of the logistics market "
        self.algo_trading_market_profit_margin = (
            self.logistics_market_profit_margin
        )

        # Assume the profit margin in the material sciences market equals that
        # of the logistics market
        self.material_sciences_market_profit_margin = (
            self.logistics_market_profit_margin
        )

        # Assume the profit margin in the pharmaceutics market equals that of
        # the logistics market
        self.pharmaceutics_market_profit_margin = (
            self.logistics_market_profit_margin
        )

        # Assume the profit margin in the telecommunications market equals that
        # of the logistics market
        self.telecommunications_market_profit_margin = (
            self.logistics_market_profit_margin
        )

    def compute_market_profit(self):
        """Computes the profit per market sector based on the assumption that
        the profit margin in each sector equals that of the logistics
        market."""
        self.algo_trading_market_profit = self.get_market_profit(
            self.algo_trading_market_size,
            self.algo_trading_market_profit_margin,
        )
        self.material_sciences_market_profit = self.get_market_profit(
            self.material_sciences_market_size,
            self.material_sciences_market_profit_margin,
        )
        self.pharmaceutics_market_profit = self.get_market_profit(
            self.pharmaceutics_market_size,
            self.pharmaceutics_market_profit_margin,
        )
        self.telecommunications_market_profit = self.get_market_profit(
            self.telecommunications_market_size,
            self.telecommunications_market_profit_margin,
        )
