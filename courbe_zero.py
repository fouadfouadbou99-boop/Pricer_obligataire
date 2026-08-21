import pandas as pd
import numpy as np

class ZeroCurve:

    def __init__(self, fichier_csv):

        df = pd.read_csv(fichier_csv)

        self.tenors = df["tenor"].values
        self.rates = df["rate"].values

    def get_rate(self, maturity):

        return np.interp(
            maturity,
            self.tenors,
            self.rates
        )
