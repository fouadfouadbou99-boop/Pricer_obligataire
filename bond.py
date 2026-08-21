import numpy as np

class Bond:

    def __init__(
        self,
        nominal,
        coupon_rate,
        maturity,
        frequency=2
    ):
        self.nominal = nominal
        self.coupon_rate = coupon_rate
        self.maturity = maturity
        self.frequency = frequency

    def price(self, curve):

        n = int(self.maturity * self.frequency)

        coupon_periodique = (
            self.nominal
            * self.coupon_rate
            / self.frequency
        )

        prix = 0

        for i in range(1, n + 1):

            temps = i / self.frequency

            taux = curve.get_rate(temps)

            prix += (
                coupon_periodique
                /
                ((1 + taux) ** temps)
            )

        prix += (
            self.nominal
            /
            (
                (1 + curve.get_rate(self.maturity))
                ** self.maturity
            )
        )

        return prix
