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

        coupon = (
            self.nominal
            * self.coupon_rate
            / self.frequency
        )

        price = 0

        for i in range(1, n + 1):

            t = i / self.frequency

            rate = curve.get_rate(t)

            price += coupon / ((1 + rate) ** t)

        price += (
            self.nominal
            /
            ((1 + curve.get_rate(self.maturity))
             ** self.maturity)
        )

        return price
