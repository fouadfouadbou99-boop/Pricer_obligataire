def macaulay_duration(
        bond,
        curve):

    coupon_cf = (
        bond.nominal *
        bond.coupon /
        bond.frequency
    )

    n = int(
        bond.maturity *
        bond.frequency
    )

    prix = 0
    poids = 0

    for i in range(1, n + 1):

        t = i / bond.frequency

        taux = curve.get_rate(t)

        cf = coupon_cf

        if i == n:
            cf += bond.nominal

        va = cf / ((1 + taux) ** t)

        prix += va

        poids += t * va

    return poids / prix


def modified_duration(
        macaulay,
        taux):

    return (
        macaulay /
        (1 + taux)
    )


def dv01(
        prix,
        duration_mod):

    return (
        prix *
        duration_mod *
        0.0001
    )
