def shocked_price(
        price,
        mod_duration,
        shock_bp):

    shock = (
        shock_bp / 10000
    )

    return (
        price *
        (
            1 -
            mod_
