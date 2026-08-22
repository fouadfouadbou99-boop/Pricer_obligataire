from modules.cashflows import (
    generate_cashflows
)


def convexity(
        bond,
        curve):

    times, cfs = generate_cashflows(
        bond
    )

    num = 0
    den = 0

    for t, cf in zip(
            times,
            cfs):

        r = curve.get_rate(t)

        pv = cf / ((1+r)**t)

        den += pv

        num += (
            t *
            (t+1) *
            pv
        )

    return (
        num /
        (den * ((1+r)**2))
    )
