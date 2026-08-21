import pandas as pd


def build_scenarios(
    bond,
    curve,
    curve_df,
    ZeroCurve
):

    shocks = [
        -200,
        -100,
        -50,
        0,
        50,
        100,
        200
    ]

    rows = []

    for shock in shocks:

        shifted_curve = ZeroCurve(

            curve_df["tenor"],

            curve_df["rate"]
            + shock / 10000
        )

        rows.append(
            {
                "Choc (pb)"
                : shock,

                "Prix"
                : round(
                    bond.price(
                        shifted_curve
                    ),
                    2
                )
            }
        )

    return pd.DataFrame(rows)
