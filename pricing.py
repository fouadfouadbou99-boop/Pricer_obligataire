from cashflows import generate_cashflows


def price_bond(
        bond,
        curve):

    times, cfs = generate_cashflows(
        bond
    )

    price = 0

    for t, cf in zip(
            times,
            cfs):

        r = curve.get_rate(t)

        price += (
            cf /
            ((1 + r) ** t)
        )

    return price
