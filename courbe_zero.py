import numpy as np


class ZeroCurve:

    def __init__(self, tenors, rates):

        self.tenors = np.array(tenors)
        self.rates = np.array(rates)

    def get_rate(self, maturity):

        return float(
            np.interp(
                maturity,
                self.tenors,
                self.rates
            )
        )
