import pandas as pd


def build_summary(
        portfolio_value,
        duration,
        dv01_total):

    return pd.DataFrame({

        "Indicateur": [

            "Valeur Marché",
            "Duration",
            "DV01"

        ],

        "Valeur": [

            portfolio_value,
            duration,
            dv01_total

        ]
    })
