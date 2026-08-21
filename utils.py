def bond_status(
    price,
    nominal
):

    if price > nominal:

        return "Premium"

    elif price < nominal:

        return "Discount"

    return "Pair"
