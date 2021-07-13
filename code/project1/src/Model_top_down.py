# The bottom up model that computes the TAM and TSM
import random
from matplotlib import pyplot as plt
from matplotlib import lines
import matplotlib.pyplot as plt
import numpy as np

from .Plot_to_tex import Plot_to_tex as plt_tex
from .Datapoints import Datapoints


class Model_top_down:
    def __init__(self):
        self.nr_simulations = 100
        self.dp = Datapoints()
        x_series, y_series= self.estimate_revenue()
        self.plot_data_series(x_series, y_series)
        # self.get_normal_dist ()

    def estimate_revenue(self):
        revenue_logistics, randomness_logistics = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.logistics_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        #self.plot_data(randomness_logistics, revenue_logistics)
        
        # algo
        revenue_algo_trading, randomness_algo_trading = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.algo_trading_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        #self.plot_data(randomness_algo_trading, revenue_logistics)
        
        # material
        revenue_material_sciences, randomness_material_sciences = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.material_sciences_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        #self.plot_data(randomness_material_sciences, revenue_logistics)
        
        # pharma
        revenue_pharmaceutics, randomness_pharmaceutics = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.pharmaceutics_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        #self.plot_data(randomness_pharmaceutics, revenue_logistics)
       
        # tele
        revenue_telecommunications, randomness_telecommunications = self.estimate_logistics_revenue(
            self.nr_simulations,
            self.dp.profit_gain_by_trucol_protocol_consultancy,
            self.dp.telecommunications_market_profit,
            self.dp.fraction_of_profit_shared_with_trucol,
        )
        self.plot_data(randomness_telecommunications, revenue_telecommunications)
        x_series=[randomness_logistics,randomness_algo_trading,  randomness_material_sciences, randomness_pharmaceutics,randomness_telecommunications]
        y_series=[revenue_logistics,revenue_algo_trading,  revenue_material_sciences, revenue_pharmaceutics,revenue_telecommunications]
        # estimated_revenue=revenue_logistics+revenue_pharmaceutics+revenue_algo_trading+revenue_material_sciences+revenue_telecommunications
        estimated_revenue = 0
        return x_series, y_series

    def estimate_logistics_revenue(
        self, N, gain, market_profit, shared_profit_fraction
    ):
        revenue_estimates = []
        randomness = []
        for i in range(0, N):
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
        # x = np.random.rand(N)
        # y = np.random.rand(N)*10

        # random colour for points, vector of length N
        colors = np.random.rand(N)
        print(f"colors={colors}")
        print(f"x={x}")

        # area of the circle, vectoe of length N
        # area = (30 * np.random.rand(N))**2

        plt.figure()
        plt.scatter(x, y, c=colors, alpha=0.8)
        plt.xlabel("Randomness")
        plt.ylabel("Estimated revenue")
        plt.title("Monte-carlo simulation estimated\n yearly revenue TruCol consultancy")
        plt.show()
        plt.savefig("example.png")

    def plot_data_series(self, x_series, y_series):
        #x=concatenate_series(x_series)
        x = [item for sublist in x_series for item in sublist]
        y = [item for sublist in y_series for item in sublist]
        #y=concatenate_series(y_series)
        #N = self.nr_simulations
        N = len(x)
        
        # x = np.random.rand(N)
        # y = np.random.rand(N)*10

        # random colour for points, vector of length N
        #colors = np.random.rand(N)
        colors = self.get_colors(x_series,y_series)
        #print(f"colors={colors}")
        #print(f"x={x}")

        # area of the circle, vectoe of length N
        # area = (30 * np.random.rand(N))**2

        plt.figure()
        plt.scatter(x, y, c=colors, alpha=0.8)
        plt.xlabel("Randomness")
        plt.ylabel("Estimated revenue")
        plt.title("Monte-carlo simulation estimated\n yearly revenue TruCol consultancy")
        plt.show()
        plt.savefig("example.png")

    def get_colors(self, x_series,y_series):
        colors= np.random.rand(len(x_series))
        x = [item for sublist in x_series for item in sublist]
        color_arr=[]
        for i in range(0,len(x_series)):
            for elem in range(0,len(x_series[i])):
                color_arr.append(colors[i])
        return color_arr
            
    def get_normal_dist(self):
        # Creating a series of data of in range of 1-50.
        x = np.linspace(1, 50, 200)

        # Calculate mean and Standard deviation.
        mean = np.mean(x)
        sd = np.std(x)

        # Apply function to the data.
        pdf = self.normal_dist(x, mean, sd)
        # print(f'pdf={pdf}')
        # Plotting the Results
        plt.plot(x, pdf, color="red")
        plt.xlabel("Data points")
        plt.ylabel("Probability Density")
        plt.show()

    # Creating a Function.
    def normal_dist(self, x, mean, sd):
        prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
        return prob_density

    def addTwo(self, x):
        """adds two to the incoming integer and returns the result of the computation."""
        return x + 2
