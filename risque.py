import numpy as np


def macaulay_duration(dates, flux, taux):

    prix = 0
    somme_ponderee = 0

    for t, cf in zip(dates, flux):

        va = cf / ((1 + taux) ** t)

        prix += va

        somme_ponderee += t * va

    return somme_ponderee / prix


def modified_duration(duration_macaulay, taux):

    return duration_macaulay / (1 + taux)


def dv01(prix, duration_modifiee):

    return prix * duration_modifiee * 0.0001


def convexity(dates, flux, taux):

    prix = 0
    conv = 0

    for t, cf in zip(dates, flux):

        va = cf / ((1 + taux) ** t)

        prix += va

        conv += t * (t + 1) * va

    return conv / (prix * (1 + taux) ** 2)
