import numpy as np


class ZeroCurve:

    def __init__(
        self,
        tenors,
        rates
    ):

        self.tenors = np.array(
            tenors,
            dtype=float
        )

        self.rates = np.array(
            rates,
            dtype=float
        )

    def get_rate(
        self,
        maturity
    ):

        return float(
            np.interp(
                maturity,
                self.tenors,
                self.rates
            )
        )

    def parallel_shift(
        self,
        shift
    ):

        return ZeroCurve(
            self.tenors,
            self.rates + shift
        )
