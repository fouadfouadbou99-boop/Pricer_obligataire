import numpy as np
import pandas as pd


def generate_cashflows(bond):

    n = int(
        bond.maturity *
        bond.frequency
    )

    coupon_cf = (
        bond.nominal *
        bond.coupon_rate /
        bond.frequency
    )

    times = np.arange(
        1,
        n + 1
    ) / bond.frequency

    cashflows = [coupon_cf] * n

    cashflows[-1] += bond.nominal

    return pd.DataFrame(
        {
            "Maturite": times,
            "Flux": cashflows
        }
    )
