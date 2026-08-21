import numpy as np

def generer_flux(nominal, coupon, maturite, frequence):
    """
    Génère les flux futurs de l'obligation.
    """

    n = int(maturite * frequence)

    coupon_periodique = nominal * coupon / frequence

    dates = np.arange(1, n + 1) / frequence

    flux = [coupon_periodique] * n

    flux[-1] += nominal

    return dates, flux
