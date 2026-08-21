def spread_bp(
    ytm,
    sovereign_rate
):

    return (
        ytm
        - sovereign_rate
    ) * 10000
