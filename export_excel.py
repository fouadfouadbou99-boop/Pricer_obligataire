from io import BytesIO
import pandas as pd


def generate_excel_report(
    curve_df,
    sens_df,
    cashflows_df
):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        curve_df.to_excel(
            writer,
            sheet_name="Courbe",
            index=False
        )

        sens_df.to_excel(
            writer,
            sheet_name="Sensibilite",
            index=False
        )

        cashflows_df.to_excel(
            writer,
            sheet_name="Cashflows",
            index=False
        )

    return output.getvalue()
