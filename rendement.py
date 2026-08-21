from scipy.optimize import brentq

def calcul_ytm(prix, nominal, coupon, maturite, frequence):

    def fonction(y):

        prix_modele = 0

        n = int(maturite * frequence)

        coupon_periodique = nominal * coupon / frequence

        for i in range(1, n + 1):

            prix_modele += coupon_periodique / (
                (1 + y / frequence) ** i
            )

        prix_modele += nominal / (
            (1 + y / frequence) ** n
        )

        return prix_modele - prix

    return brentq(fonction, 0.0001, 0.20)
