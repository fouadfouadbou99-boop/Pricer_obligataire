def macaulay_duration(bond, curve):

    price = bond.price(curve)

    weighted_pv = 0

    n = int(
        bond.maturity
        * bond.frequency
    )

    coupon = (
        bond.nominal
        * bond.coupon_rate
        / bond.frequency
    )

    for i in range(1, n + 1):

        t = i / bond.frequency

        rate = curve.get_rate(t)

        cashflow = coupon

        if i == n:
            cashflow += bond.nominal

        pv = cashflow / ((1 + rate) ** t)

        weighted_pv += t * pv

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
        1 + y / bond.frequency
    )


def convexity(
    bond,
    curve
):

    price = bond.price(curve)

    total = 0

    n = int(
        bond.maturity
        * bond.frequency
    )

    coupon = (
        bond.nominal
        * bond.coupon_rate
        / bond.frequency
    )

    for i in range(1, n + 1):

        t = i / bond.frequency

        rate = curve.get_rate(t)

        cashflow = coupon

        if i == n:
            cashflow += bond.nominal

        total += (
            cashflow
            * t
            * (t + 1)
            /
            ((1 + rate) ** (t + 2))
        )

    return total / price


def dv01(
    bond,
    curve
):

    price = bond.price(curve)

    mod_dur = modified_duration(
        bond,
        curve
    )

    return (
        price
        * mod_dur
        * 0.0001
    )
