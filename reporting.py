import pandas as pd


def executive_summary(
    price,
    ytm,
    duration,
    mod_duration,
    convexity,
    dv01
):

    return pd.DataFrame({

        "Indicateur":[
            "Prix",
            "YTM",
            "Duration",
            "Duration Modifiee",
            "Convexite",
            "DV01"
        ],

        "Valeur":[

            round(price,2),

 
