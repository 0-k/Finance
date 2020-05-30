import pandas as pd
import yfinance as yt
import numpy as np


class FinancialSeries:

    def __init__(self):
        self.values = None
        self.name = None
        self.ticker = None

    def fetch(self):
        raise NotImplementedError()

    def cache(self):
        raise NotImplementedError()

