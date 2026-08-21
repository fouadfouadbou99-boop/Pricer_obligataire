import numpy as np

def duration_modifiee(duration_macaulay, ytm):

    return duration_macaulay / (1 + ytm)


def dv01(prix, duration_mod, delta=0.0001):

    return prix * duration_mod * delta


def convexite(dates, flux, taux):

    numerateur = 0

    denominateur = 0

    for t, cf in zip(dates, flux):

        facteur = (1 + taux) ** t

        numerateur += cf * t * (t + 1) / facteur

        denominateur += cf / facteur

    return numerateur / denominateur
