from scipy.optimize import newton


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

    def cashflows(self):

        flows = []

        n = int(
            self.maturity
            * self.frequency
        )

        coupon = (
            self.nominal
            * self.coupon_rate
            / self.frequency
        )

        for i in range(1, n + 1):

            t = i / self.frequency

            cf = coupon

            if i == n:
                cf += self.nominal

            flows.append(
                (t, cf)
            )

        return flows

    def price(
        self,
        curve
    ):

        value = 0

        for t, cf in self.cashflows():

            rate = curve.get_rate(t)

            value += (
                cf /
                ((1 + rate) ** t)
            )

        return value

    def ytm(
        self,
        market_price
    ):

        def objective(y):

            value = 0

            for t, cf in self.
