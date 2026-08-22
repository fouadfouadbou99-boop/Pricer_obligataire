import pandas as pd


def load_portfolio(file):

    return pd.read_excel(
        file,
        engine="openpyxl"
    )
