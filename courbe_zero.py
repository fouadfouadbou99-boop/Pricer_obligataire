import pandas as pd
import numpy as np


class ZeroCurve:

    def __init__(self, csv_file):

        df = pd.read_csv(csv_file)

        self.tenors = np.array(df["tenor"], dtype=float)
        self.rates = np.array(df["rate"], dtype=float)

    def get_rate(self, maturity):

        return float(
            np.interp(
                maturity,
                self.tenors,
                self.rates
            )
        )
