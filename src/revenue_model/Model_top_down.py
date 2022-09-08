"""The bottom up model that computes the TAM and TSM."""

import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

from src.export_data.export_params_to_latex import (
    export_params_to_latex_params_and_table,
)
from src.revenue_model.Datapoints import Datapoints


class Model_top_down:
    """Applies the assumptions of the accompanying market analysis pdf to
    generate the expected revenue in the form of a Monte-Carlo simulation."""

    def __init__(self):
        self.nr_simulations = 300
        self.dp = Datapoints()
        x_series, y_series = self.estimate_revenue()
        self.plot_data_series(x_series, y_series)
        # self. get normal dist ()
        y = self.sum_revenues(y_series)
        x = self.avg_randomness(x_series)

        self.plot_data(x, y)

        # Convert parameters to dictionary.
        model_params = {
            "nr_simulations": self.nr_simulations,
        }

        param_dict = model_params | self.dp.datapoints_dict
        export_params_to_latex_params_and_table(
            param_dict, "latex/Tables/top_down", "market_size_params"
        )

    def sum_revenues(self, x_series):
        """Computes the summed revenue.

        # TODO: improve comment.

        :param x_series:
        """
        summed_series = []
        for i, _ in enumerate(x_series[0]):
            summed = 0
            for j, _ in enumerate(x_series):
                # pylint: disable=R1736
                summed = summed + x_series[j][i]

            summed_series.append(summed)
        return summed_series

    def avg_randomness(self, series):
        """Returns the summed value of a series.
        TODO: make explicit why it is called avg_randomness.
        (See:sum_revenues)

        :param series:

        """
        summed_series = []
        for i, _ in enumerate(series[0]):
            summed = 0
            # pylint: disable=R1736
            for j, _ in enumerate(series):
                summed = summed + series[j][i]
            summed_series.append(summed / len(series))
        return summed_series

    def estimate_revenue(self):
        """Estimates the TruCol revenue based on the assumptions stated in the
        accompanying market analysis pdf."""
        (
            revenue_logistics,
            randomness_logistics,
        ) = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_company,
            self.dp.logistics_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
            self.dp.sam_factor,
            self.dp.tam_factor,
        )
        # self.plot_data(randomness_logistics, revenue_logistics)

        # algo
        (
            revenue_algo_trading,
            randomness_algo_trading,
        ) = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_company,
            self.dp.algo_trading_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
            self.dp.sam_factor,
            self.dp.tam_factor,
        )
        # self.plot_data(randomness_algo_trading,
        # revenue_algo_trading)

        # material
        (
            revenue_material_sciences,
            randomness_material_sciences,
        ) = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_company,
            self.dp.material_sciences_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
            self.dp.sam_factor,
            self.dp.tam_factor,
        )
        print(
            "material_sciences_market_profit="
            + f"{self.dp.material_sciences_market_profit}"
        )
        # self.plot_data(randomness_material_sciences,
        # material_sciences_market_profit)

        # pharma
        (
            revenue_pharmaceutics,
            randomness_pharmaceutics,
        ) = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_company,
            self.dp.pharmaceutics_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
            self.dp.sam_factor,
            self.dp.tam_factor,
        )
        print(
            "pharmaceutics_market_profit="
            + f"{self.dp.pharmaceutics_market_profit}"
        )
        # self.plot_data(randomness_pharmaceutics, revenue_pharmaceutics)

        # tele
        (
            revenue_telecommunications,
            randomness_telecommunications,
        ) = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_company,
            self.dp.telecommunications_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
            self.dp.sam_factor,
            self.dp.tam_factor,
        )
        print(
            "telecommunications_market_profit="
            + f"{self.dp.telecommunications_market_profit}"
        )
        # self.plot_data(randomness_telecommunications,
        # revenue_telecommunications)

        # Concatenate all datapoints
        x_series = [
            randomness_logistics,
            randomness_algo_trading,
            randomness_material_sciences,
            randomness_pharmaceutics,
            randomness_telecommunications,
        ]
        y_series = [
            revenue_logistics,
            revenue_algo_trading,
            revenue_material_sciences,
            revenue_pharmaceutics,
            revenue_telecommunications,
        ]
        return x_series, y_series

    # pylint: disable=R0913
    # pylint: disable=R0914
    def estimate_logistics_revenue(
        self,
        N,
        gain_range,
        market_profit_range,
        shared_profit_fraction_range,
        sam_factor,
        tam_factor,
    ):
        """Estimates the TruCol revenue within the logistics sector.

        :param N: param gain_range:
        :param market_profit_range: param shared_profit_fraction_range:
        :param sam_factor: param tam_factor:
        :param gain_range:
        :param shared_profit_fraction_range:
        :param tam_factor:
        """
        print(f"market_profit_range={market_profit_range}")
        print(f"shared_profit_fraction_range={shared_profit_fraction_range}")

        revenue_estimates = []
        randomness = []
        for _ in range(0, N):
            # TODO: change to get the range as specified in datapoints per
            # parameter
            rand_market_profit = float(
                np.random.rand(1) * 5
            )  # factor 0 to 5 as the computed profit margin of 0.0158 seems
            # slightly low
            rand_gain = float(
                np.random.rand(1) * 16
            )  # map gain to range of 0.1 to 16% based on McKinsey study
            # rand_c = float(np.random.rand(1) * 2)
            # map profit fraction from 0.1 to 10
            rand_tam = float(
                np.random.rand(1) * 2
            )  # map tam to factor 2 as it is a rough estimate
            rand_sam = float(
                np.random.rand(1) * 2
            )  # map samto factor 2 as it is a rough estimate
            rand_profit_fraction = float(
                np.random.rand(1) * 50
            )  # map profit fraction (shared with TruCol) from 1 to 50%
            randomness.append(
                (1 - rand_market_profit) ** 2
                + (1 - rand_gain) ** 2
                + (1 - rand_tam) ** 2
                + (1 - rand_sam) ** 2
            )
            rand_market_profit_range = market_profit_range * rand_market_profit
            rand_gain_rainge = gain_range * rand_gain
            rand_sam_range = sam_factor * rand_sam
            rand_tam_range = tam_factor * rand_tam

            # rand_shared_profit_fraction_range = (
            #    shared_profit_fraction_range * rand_profit_fraction
            # )

            revenue_estimates.append(
                rand_market_profit_range
                * rand_sam_range
                * rand_tam_range
                * rand_gain_rainge
                * rand_profit_fraction
            )
        return revenue_estimates, randomness

    def estimate_pharmaceutics_revenue(self):
        """Returns the pharmaceutics revenue as 0 to only focus on one
        sector."""
        return 0

    def estimate_algo_trading_revenue(self):
        """Returns the algorithmic trading revenue as 0 to only focus on one
        sector."""
        return 0

    def estimate_material_sciences_revenue(self):
        """Returns the material sciences revenue as 0 to only focus on one
        sector."""
        return 0

    def estimate_telecommunications_revenue(self):
        """Returns the telecomunications revenue as 0 to only focus on one
        sector."""
        return 0

    def plot_data(self, x, y):
        """Plots some x and y coordinates in scatterplot.

        :param x: param y:
        :param y:
        """
        N = self.nr_simulations

        # Random colour for points, vector of length N
        colors = np.ones(N)

        # Plot figure
        _, ax = plt.subplots()

        # Set y-axis scale to millions
        scale_y = 1e6
        ticks_y = ticker.FuncFormatter(lambda x, _: f"{x / scale_y:g}")
        ax.yaxis.set_major_formatter(ticks_y)

        # Specify units of y-axis
        ax.set_ylabel("$ million")

        plt.scatter(x, y, c=colors, alpha=0.8)
        plt.xlabel("Summed Squared Average Randomness")
        plt.ylabel("Estimated revenue in $million/year")
        plt.title(
            "Monte-carlo simulation\n estimated total revenue TruCol company"
        )

        # Export/save plot
        # plt.show()
        plt.savefig(
            os.path.dirname(__file__)
            + "/../../latex"
            + "/Images/"
            + "revenue_sum"
            + ".png"
        )

    def plot_data_series(self, x_series, y_series):
        """Creates a scatter plot based on the incoming x and y coordinate
        series. A series represents a datatype.

        :param x_series: param y_series:
        :param y_series:
        """
        x = [item for sublist in x_series for item in sublist]
        y = [item for sublist in y_series for item in sublist]
        len(x)

        # random colour for points, vector of length N
        colors, _ = self.get_colors(x_series)

        # Plot figure
        _, ax = plt.subplots()

        # Set y-axis scale to millions
        scale_y = 1e6
        ticks_y = ticker.FuncFormatter(lambda x, _: f"{x / scale_y:g}")
        ax.yaxis.set_major_formatter(ticks_y)

        # Specify units of y-axis
        ax.set_ylabel("$ million")

        # Manually create the legend based on hardcoded colours
        logistics = mpatches.Patch(color="yellow", label="logistics")
        algo_trading = mpatches.Patch(
            color="green", label="algorithmic trading"
        )
        material_sciences = mpatches.Patch(
            color="cyan", label="material sciences"
        )
        pharmaceutics = mpatches.Patch(color="blue", label="pharmaceutics")
        telecommunications = mpatches.Patch(
            color="magenta", label="telecommunications"
        )
        plt.legend(
            handles=[
                logistics,
                algo_trading,
                material_sciences,
                pharmaceutics,
                telecommunications,
            ]
        )

        # Generate the scatterplot
        plt.scatter(x, y, c=colors, alpha=0.8)
        plt.xlabel("Summed Squared Randomness")
        plt.ylabel("Estimated revenue in $million/year")
        plt.title(
            "Monte-carlo simulation\n estimated revenue TruCol company per"
            + " sector"
        )

        # Export/save plot
        # plt.show()
        plt.savefig(
            os.path.dirname(__file__)
            + "/../../latex"
            + "/Images/"
            + "revenue_per_sector"
            + ".png"
        )

    def get_colors(self, x_series):
        """Returns the colours for the different data series that are being
        plotted.

        :param x_series: param y_series:
        :param y_series:
        """

        # Create list to store colors
        color_arr = []

        # Hardcode the colours for the dataseries
        colors = ["yellow", "green", "cyan", "blue", "magenta"]

        # Flatten the lists per sector into a single list
        # [item for sublist in x_series for item in sublist]

        # Give each datapoint of a sector the same colour
        for i, _ in enumerate(x_series):
            # pylint: disable=R1736
            for _ in range(0, len(x_series[i])):
                # pylint: disable=R1736
                color_arr.append(colors[i])
        return color_arr, colors

    def get_normal_dist(self):
        """Gets a normal distribution and plots it."""
        # Creating a series of data of in range of 1-50.
        x = np.linspace(1, 50, 200)

        # Calculate mean and Standard deviation.
        mean = np.mean(x)
        sd = np.std(x)

        # Apply function to the data.
        pdf = self.normal_dist(x, mean, sd)

        # Plotting the Results
        plt.plot(x, pdf, color="red")
        plt.xlabel("Data points")
        plt.ylabel("Probability Density")

    def normal_dist(self, x, mean, sd):
        """Generates a normal distribution.

        :param x: param mean:
        :param sd:
        :param mean:
        """
        prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
        return prob_density

    def addTwo(self, x):
        """adds two to the incoming integer and returns the result of the
        computation.

        :param x:
        """
        return x + 2
