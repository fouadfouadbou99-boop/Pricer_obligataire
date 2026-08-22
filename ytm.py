from scipy.optimize import brentq

from modules.cashflows import (
    generate_cashflows
)


def calculate_ytm(
        bond,
        market_price):

    times, cfs = generate_cashflows(
        bond
    )

    def objective(y):

        pv = 0

        for t, cf in zip(
                times,
                cfs):

            pv += (
                cf /
                ((1 + y) ** t)
            )

        return pv - market_price

    return brentq(
        objective,
        0.0001,
        0.30
    )
