# The bottom up model that computes the TAM and TSM

from matplotlib import lines
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import numpy as np
import os
import random

from .Plot_to_tex import Plot_to_tex as plt_tex
from .Datapoints import Datapoints


class Model_top_down:
    def __init__(self, project_nr):
        self.project_nr = project_nr
        self.nr_simulations = 300
        self.dp = Datapoints()
        x_series, y_series = self.estimate_revenue()
        self.plot_data_series(x_series, y_series)
        # self. get normal dist ()
        y = self.sum_revenues(y_series)
        x = self.avg_randomness(x_series)

        self.plot_data(x, y)

    def sum_revenues(self, x_series):
        summed_series = []
        for i in range(0, len(x_series[0])):
            summed = 0
            for j in range(0, len(x_series)):
                summed = summed + x_series[j][i]

            summed_series.append(summed)
        return summed_series

    def avg_randomness(self, series):
        summed_series = []
        for i in range(0, len(series[0])):
            summed = 0
            for j in range(0, len(series)):
                summed = summed + series[j][i]
            summed_series.append(summed / len(series))
        return summed_series

    def estimate_revenue(self):
        revenue_logistics, randomness_logistics = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.logistics_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        # self.plot_data(randomness_logistics, revenue_logistics)

        # algo
        revenue_algo_trading, randomness_algo_trading = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.algo_trading_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        # self.plot_data(randomness_algo_trading, revenue_algo_trading)

        # material
        (
            revenue_material_sciences,
            randomness_material_sciences,
        ) = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.material_sciences_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        print(
            f"material_sciences_market_profit={self.dp.material_sciences_market_profit}"
        )
        # self.plot_data(randomness_material_sciences, material_sciences_market_profit)

        # pharma
        (
            revenue_pharmaceutics,
            randomness_pharmaceutics,
        ) = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.pharmaceutics_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        print(f"pharmaceutics_market_profit={self.dp.pharmaceutics_market_profit}")
        # self.plot_data(randomness_pharmaceutics, revenue_pharmaceutics)

        # tele
        (
            revenue_telecommunications,
            randomness_telecommunications,
        ) = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.telecommunications_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        print(
            f"telecommunications_market_profit={self.dp.telecommunications_market_profit}"
        )
        # self.plot_data(randomness_telecommunications, revenue_telecommunications)

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

    def estimate_logistics_revenue(
        self, N, gain, market_profit, shared_profit_fraction
    ):
        revenue_estimates = []
        randomness = []
        for i in range(0, N):
            # TODO: change to get the range as specified in datapoints per parameter
            rand_a = float(np.random.rand(1) * 2)
            rand_b = float(np.random.rand(1) * 2)
            rand_c = float(np.random.rand(1) * 2)
            randomness.append((1 - rand_a) ** 2 + (1 - rand_b) ** 2 + (1 - rand_c) ** 2)
            revenue_estimates.append(
                market_profit * rand_a * gain * rand_b * shared_profit_fraction * rand_c
            )

        return revenue_estimates, randomness

    def estimate_pharmaceutics_revenue(self):
        return 0

    def estimate_algo_trading_revenue(self):
        return 0

    def estimate_material_sciences_revenue(self):
        return 0

    def estimate_telecommunications_revenue(self):
        return 0

    def plot_data(self, x, y):
        N = self.nr_simulations

        # Random colour for points, vector of length N
        colors = np.ones(N)

        # Plot figure
        fig, ax = plt.subplots()

        # Set y-axis scale to millions
        scale_y = 1e6
        ticks_y = ticker.FuncFormatter(lambda x, pos: "{0:g}".format(x / scale_y))
        ax.yaxis.set_major_formatter(ticks_y)

        # Specify units of y-axis
        ax.set_ylabel("$ million")

        plt.scatter(x, y, c=colors, alpha=0.8)
        plt.xlabel("Summed Squared Average Randomness")
        plt.ylabel("Estimated revenue in $million/year")
        plt.title("Monte-carlo simulation\n estimated total revenue TruCol consultancy")

        # Export/save plot
        # plt.show()
        plt.savefig(
            os.path.dirname(__file__)
            + "/../../../latex/project"
            + str(self.project_nr)
            + "/Images/"
            + "revenue_sum"
            + ".png"
        )

    def plot_data_series(self, x_series, y_series):
        x = [item for sublist in x_series for item in sublist]
        y = [item for sublist in y_series for item in sublist]
        N = len(x)

        # random colour for points, vector of length N
        colors, legend_colors = self.get_colors(x_series, y_series)

        # Plot figure
        fig, ax = plt.subplots()

        # Set y-axis scale to millions
        scale_y = 1e6
        ticks_y = ticker.FuncFormatter(lambda x, pos: "{0:g}".format(x / scale_y))
        ax.yaxis.set_major_formatter(ticks_y)

        # Specify units of y-axis
        ax.set_ylabel("$ million")

        # Manually create the legend based on hardcoded colours
        logistics = mpatches.Patch(color="yellow", label="logistics")
        algo_trading = mpatches.Patch(color="green", label="algorithmic trading")
        material_sciences = mpatches.Patch(color="cyan", label="material sciences")
        pharmaceutics = mpatches.Patch(color="blue", label="pharmaceutics")
        telecommunications = mpatches.Patch(color="magenta", label="telecommunications")
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
            "Monte-carlo simulation\n estimated revenue TruCol consultancy per sector"
        )

        # Export/save plot
        # plt.show()
        plt.savefig(
            os.path.dirname(__file__)
            + "/../../../latex/project"
            + str(self.project_nr)
            + "/Images/"
            + "revenue_per_sector"
            + ".png"
        )

    def get_colors(self, x_series, y_series):

        # Create list to store colors
        color_arr = []

        # Hardcode the colours for the dataseries
        colors = ["yellow", "green", "cyan", "blue", "magenta"]

        # Flatten the lists per sector into a single list
        x = [item for sublist in x_series for item in sublist]

        # Give each datapoint of a sector the same colour
        for i in range(0, len(x_series)):
            for elem in range(0, len(x_series[i])):
                color_arr.append(colors[i])
        return color_arr, colors

    def get_normal_dist(self):
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
        prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
        return prob_density

    def addTwo(self, x):
        """adds two to the incoming integer and returns the result of the computation."""
        return x + 2
