import numpy as np

def prix_obligation(
        nominal,
        coupon,
        maturite,
        frequence,
        taux_zero):

    n = int(maturite * frequence)

    coupon_periodique = nominal * coupon / frequence

    prix = 0

    for i in range(1, n + 1):

        temps = i / frequence

        taux = taux_zero(temps)

        prix += coupon_periodique / (
            (1 + taux) ** temps
        )

    prix += nominal / (
        (1 + taux_zero(maturite)) ** maturite
    )

    return prix
