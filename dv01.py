def modified_duration(
        macaulay,
        ytm):

    return (
        macaulay /
        (1 + ytm)
    )


def dv01(
        price,
        modified_dur):

    return (
        price *
        modified_dur *
        0.0001
    )
