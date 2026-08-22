def macaulay_duration(
    bond,
    curve
):

    price = bond.price(curve)

    weighted_pv = 0

    for t, cf in bond.cashflows():

        rate = curve.get_rate(t)

        pv = cf / (
            (1 + rate) ** t
        )

        weighted_pv += (
            t * pv
        )

    return weighted_pv / price


def modified_duration(
    bond,
    curve
):

    md = macaulay_duration(
        bond,
        curve
    )

    y = curve.get_rate(
        bond.maturity
    )

    return md / (
        1 + y /
        bond.frequency
    )


def convexity(
    bond,
    curve
):

    price = bond.price(curve)

    total = 0

    for t, cf in bond.cashflows():

        rate = curve.get_rate(t)

        total += (
            cf *
            t *
            (t + 1)
            /
            ((1 + rate) ** (t + 2))
        )

    return total / price


def dv01(
    bond,
    curve
):

    price = bond.price(curve)

    mod_duration = modified_duration(
        bond,
        curve
    )

    return (
        price *
        mod_duration *
        0.0001
    )
