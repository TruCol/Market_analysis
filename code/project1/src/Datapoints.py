# The bottom up model that computes the TAM and TSM
import random
from matplotlib import pyplot as plt
from matplotlib import lines
import matplotlib.pyplot as plt
import numpy as np

from .Plot_to_tex import Plot_to_tex as plt_tex


class Datapoints:
    def __init__(self):
        self.profit_dhl = 4.1 * 10 ** 9  # dollar
        self.profit_fedex = 1.29 * 10 ** 9  # dollar
        self.profit_ups = 7.7 * 10 ** 9  # dollar
        self.profit_dhl_fedex_ups = (
            self.profit_dhl + self.profit_fedex + self.profit_ups
        )

        self.logistics_market_share_dhl_fedex_ups = 0.15
        self.logistics_market_share_remaining = (
            1 - self.logistics_market_share_dhl_fedex_ups
        )
        self.logistics_market_profit = self.get_logistics_market_profit()

        self.profit_gain_by_trucol_protocol = 0.04
        self.profit_gain_by_trucol_protocol_consultancy = 0.001
        self.fraction_of_profit_shared_with_trucol = 0.01

        self.logistics_market_size = 5.5 * 10 ** 12
        self.algo_trading_market_size = 11.1 * 10 ** 9
        self.material_sciences_market_size = 1 * 10 ** 9
        self.pharmaceutics_market_size = 1.27 * 10 ** 12
        self.telecommunications_market_size = 1.7 * 10 ** 12

        # assume profit margins
        self.logistics_market_profit_margin = self.get_market_profit_margin(
            self.logistics_market_size, self.logistics_market_profit
        )
        self.algo_trading_market_profit_margin = self.logistics_market_profit_margin
        self.material_sciences_market_profit_margin = (
            self.logistics_market_profit_margin
        )
        self.pharmaceutics_market_profit_margin = self.logistics_market_profit_margin
        self.telecommunications_market_profit_margin = (
            self.logistics_market_profit_margin
        )

    def get_logistics_market_profit(self):
        net_profit_remainder = (
            self.profit_dhl_fedex_ups
            * self.logistics_market_share_remaining
            / self.logistics_market_share_dhl_fedex_ups
        )
        net_profit_logistics_market = net_profit_remainder + self.profit_dhl_fedex_ups
        print(f"net_profit_logistics_market={net_profit_logistics_market}")
        return net_profit_logistics_market

    def get_market_profit_margin(self, market_size, net_profit):
        print(f"profit_margin={net_profit/market_size}")
        return net_profit / market_size
