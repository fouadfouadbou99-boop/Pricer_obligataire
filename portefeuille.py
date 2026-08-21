from bond import Bond


def portfolio_value(
    obligations,
    curve
):

    total = 0

    for ligne in obligations:

        bond = Bond(

            ligne["nominal"],

            ligne["coupon"],

            ligne["maturity"],

            ligne["frequency"]

        )

        total += bond.price(
            curve
        )

    return total
