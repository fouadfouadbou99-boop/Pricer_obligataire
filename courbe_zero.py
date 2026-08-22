import pandas as pd
import numpy as np


class ZeroCurve:

    def __init__(self, file_path):

        df = pd.read_csv(file_path)

        self.tenors = df["tenor"].astype(float).values
        self.rates = df["rate"].astype(float).values

    def get_rate(self, maturity):

        return float(
            np.interp(
                maturity,
                self.tenors,
                self.rates
            )
        )
