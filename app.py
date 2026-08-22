import pandas as pd
import plotly.express as px
import io

# Assuming these modules exist and contain relevant classes/functions
# You might need to adjust these imports based on the actual content of your files
import bond
import portfolio
import pricing
import duration
import dv01
import convexity
import rendement
import risque
import market
import cashflows
import courbe_zero
import scenario
import stress_test
import reporting
import spread

# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Portefeuille Obligataire Maroc",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Portefeuille Obligataire Maroc")

# ==================================================
# FONCTIONS
# ==================================================

@st.cache_data
def charger_portefeuille(fichier):
    return pd.read_excel(fichier, engine="openpyxl")

@st.cache_data
def charger_courbe_excel(fichier):
    return pd.read_excel(fichier, engine="openpyxl")

@st.cache_data
def charger_courbe_csv(fichier):
    return pd.read_csv(fichier)

# Helper function to create a Bond object from a DataFrame row
# Assumes 'bond' module has a Bond class with a constructor that takes relevant bond parameters
# and that column names match expected arguments.
# This is a placeholder and might need adjustment based on the actual 'bond.py' implementation.
def create_bond_object(row):
    try:
        # Assuming column names map directly to Bond constructor arguments or properties
        # Adjust these column names and parameters based on your actual data and bond.py
        return bond.Bond(
            id_titre=row.get('ISIN', 'N/A'),
            nominal=row.get('Nominal Global', 0.0),
            coupon_rate=row.get('Taux Facial', 0.0),
            issue_date=row.get('Date Emission', pd.Timestamp.now()),
            maturity_date=row.get('Date Echéance', pd.Timestamp.now()),
            frequency=row.get('Fréquence Coupon', 2) # Assuming 2 for semi-annual, adjust as needed
        )
    except Exception as e:
        st.error(f"Error creating bond object: {e}. Row data: {row.to_dict()}")
        return None


# ==================================================
# CHARGEMENT PORTFEUILLE
# ==================================================

st.sidebar.header("📂 Chargement des données")

fichier_portefeuille = st.sidebar.file_uploader(
    "📁 Charger le portefeuille",
    type=["xlsx"]
)

try:

    if fichier_portefeuille is not None:
        portefeuille = charger_portefeuille(
            fichier_portefeuille
        )
    else:
        portefeuille = charger_portefeuille(
            "RPC_bonds_data_rpc.xlsx"
        )

    st.sidebar.success("✅ Portefeuille chargé")

except Exception as e:
    st.error(f"Erreur portefeuille : {e}")
    st.stop()

# ==================================================
# CHARGEMENT COURBE
# ==================================================

fichier_courbe = st.sidebar.file_uploader(
    "📈 Charger la courbe des taux",
    type=["csv", "xlsx"]
)

try:

    if fichier_courbe is not None:

        if fichier_courbe.name.endswith(".csv"):

            courbe = charger_courbe_csv(
                fichier_courbe
            )

        else:

            courbe = charger_courbe_excel(
                fichier_courbe
            )

    else:

        courbe = pd.read_csv(
            "courbe_taux.csv"
        )

    st.sidebar.success("✅ Courbe chargée")

except Exception as e:
    st.error(f"Erreur courbe des taux : {e}")
    st.stop()

# Ensure 'courbe' DataFrame has 'tenor' and 'rate' columns
if 'tenor' not in courbe.columns or 'rate' not in courbe.columns:
    st.error("La courbe des taux doit contenir les colonnes 'tenor' et 'rate'.")
    st.stop()

# Convert curve to dictionary or appropriate format for pricing functions
yield_curve_dict = dict(zip(courbe['tenor'], courbe['rate']))

# ==================================================
# NOUVELLE SECTION: CALCULS & KPIs
# ==================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Synthèse Portefeuille",
    "Courbe des taux",
    "Analyse",
    "Export",
    "Calculs & KPIs" # New Tab
])

with tab1:

    st.header("Vue d'ensemble du portefeuille")
    st.dataframe(portefeuille)

with tab2:

    st.header("Courbe des taux actuelle")

    try:

        fig = px.line(
            courbe,
            x="tenor",
            y="rate",
            markers=True,
            title="Courbe des taux"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(e)

# ==================================================
# ANALYSE
# ==================================================

with tab3:

    if (
        "Description Titres"
        in portefeuille.columns
    ):

        fig_pie = px.pie(
            portefeuille,
            names="Description Titres",
            values="Nominal Global",
            title="Répartition du portefeuille"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    if (
        "Date Echéance"
        in portefeuille.columns
    ):

        fig_hist = px.histogram(
            portefeuille,
            x="Date Echéance",
            y="Nominal Global",
            title="Echéancier des maturités"
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

with tab5: # New tab for Calculations and KPIs
    st.header("Calcul du Prix et des KPIs du Portefeuille")

    if portefeuille is not None and not portefeuille.empty:
        st.subheader("Calcul par ligne de portefeuille")

        results = []
        for index, row in portefeuille.iterrows():
            bond_obj = create_bond_object(row)
            if bond_obj:
                try:
                    # Assuming pricing.price_bond and other modules have functions
                    # that accept a bond object and the yield curve.
                    # These function calls are placeholders and need to match your actual module APIs.
                    price = pricing.price_bond(bond_obj, yield_curve_dict)
                    yield_to_maturity = rendement.calculate_yield(bond_obj, price)
                    mod_duration = duration.modified_duration(bond_obj, yield_to_maturity)
                    conv = convexity.convexity(bond_obj, yield_to_maturity)
                    dv01_val = dv01.calculate_dv01(bond_obj, yield_to_maturity)

                    results.append({
                        'ISIN': bond_obj.id_titre,
                        'Prix': price,
                        'Rendement à Maturité': yield_to_maturity,
                        'Duration Modifiée': mod_duration,
                        'Convexité': conv,
                        'DV01': dv01_val
                    })
                except Exception as e:
                    st.warning(f"Could not calculate for ISIN {bond_obj.id_titre}: {e}")
                    results.append({
                        'ISIN': bond_obj.id_titre,
                        'Prix': 'N/A',
                        'Rendement à Maturité': 'N/A',
                        'Duration Modifiée': 'N/A',
                        'Convexité': 'N/A',
                        'DV01': 'N/A'
                    })
            else:
                st.warning(f"Could not create bond object for row {index}.")

        if results:
            df_results = pd.DataFrame(results)
            st.dataframe(df_results)

            st.subheader("KPIs agrégés du Portefeuille")
            # Assuming 'portfolio' module has a Portfolio class that can take a list of bond objects
            # and functions to calculate aggregated KPIs.
            all_bond_objects = [create_bond_object(row) for index, row in portefeuille.iterrows() if create_bond_object(row) is not None]
            if all_bond_objects:
                try:
                    bond_portfolio = portfolio.Portfolio(all_bond_objects)
                    total_value = bond_portfolio.get_total_market_value(yield_curve_dict) # Placeholder for portfolio valuation
                    portfolio_duration = bond_portfolio.calculate_portfolio_duration(yield_curve_dict) # Placeholder
                    portfolio_convexity = bond_portfolio.calculate_portfolio_convexity(yield_curve_dict) # Placeholder

                    st.write(f"**Valeur Marchande Totale du Portefeuille:** {total_value:,.2f}")
                    st.write(f"**Duration Modifiée du Portefeuille:** {portfolio_duration:,.2f}")
                    st.write(f"**Convexité du Portefeuille:** {portfolio_convexity:,.2f}")
                    # Add other aggregated KPIs as needed
                except Exception as e:
                    st.error(f"Error calculating aggregated portfolio KPIs: {e}")
            else:
                st.info("No valid bond objects to aggregate portfolio KPIs.")

        else:
            st.info("No pricing or KPI results available. Please check your portfolio data and module implementations.")
    else:
        st.info("Veuillez charger un portefeuille pour effectuer les calculs.")


# ==================================================
# EXPORT
# ==================================================

with tab4:

    buffer = io.BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        portefeuille.to_excel(
            writer,
            index=False,
            sheet_name="Portefeuille"
        )

    st.download_button(
        label="📥 Télécharger le portefeuille",
        data=buffer.getvalue(),
        file_name="portefeuille_export.xlsx",
        mime="application/vnd.ms-excel"
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Portefeuille Obligataire Maroc | Version Professionnelle"
)

with open('app.py', 'w') as f:
    f.write(app_py_content)

print("Fichier 'app.py' créé dans l'environnement Colab.")
)
