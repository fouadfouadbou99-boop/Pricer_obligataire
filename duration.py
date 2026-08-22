from modules.cashflows import generate_cashflows


def macaulay_duration(
        bond,
        curve):

    times, cfs = generate_cashflows(
        bond
    )

    pv_total = 0
    weighted = 0

    for t, cf in zip(
            times,
            cfs):

        r = curve.get_rate(t)

        pv = cf / ((1 + r) ** t)

        pv_total += pv

        weighted += t * pv

    return weighted / pv_total
