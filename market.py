import pandas as pd

def tableau_flux(dates, flux):

    return pd.DataFrame({

        "Echéance": dates,
        "Flux": flux

    })
