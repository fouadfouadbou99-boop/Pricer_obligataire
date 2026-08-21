import pandas as pd
import numpy as np


class ZeroCurve:

    def __init__(self, fichier):

        self.df = pd.read_csv(fichier)

        self.tenors = self.df["tenor"].values
        self.rates = self.df["rate"].values


    def get_rate(self, maturity):

        return float(
            np.interp(
                maturity,
                self.tenors,
                self.rates
            )
        )
