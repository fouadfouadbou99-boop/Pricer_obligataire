import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys # Added for diagnostic code

# Assuming bond.py, courbe_zero.py, and risque.py are now discoverable via sys.path
from bond import Bond
from courbe_zero import ZeroCurve
from risque import macaulay_duration #, modified_duration, convexity, dv01

# Set page configuration
st.set_page_config(page_title="Pricer Obligataire Maroc", layout="wide")
st.title("Pricer Obligataire Maroc")

# Define the path to the CSV file
# Assuming courbe_taux.csv is in the same directory as app.py in the deployed environment
CSV_FILE_PATH = "courbe_taux.csv"

# --- Caching Data and Objects ---
# Cache the CSV data loading for performance
@st.cache_data
def load_curve_data(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Erreur : '{os.path.basename(path)}' introuvable. Veuillez vous assurer qu'il se trouve dans le bon répertoire.")
        return pd.DataFrame()

# Cache the ZeroCurve object creation
@st.cache_resource
def create_zero_curve(tenors, rates):
    return ZeroCurve(tenors, rates)

# Load curve data
curve_df = load_curve_data(CSV_FILE_PATH)

if not curve_df.empty:
    # Create ZeroCurve object
    curve = create_zero_curve(curve_df["tenor"], curve_df["rate"])

    # --- Streamlit Inputs ---
    st.sidebar.header("Paramètres de l'Obligation")
    nominal = st.sidebar.number_input("Nominal (MAD)", value=1000000, min_value=1000, step=10000)
    coupon_rate = st.sidebar.number_input("Taux de Coupon (%)", value=3.5, min_value=0.0, max_value=100.0, step=0.1) / 100
    maturity = st.sidebar.number_input("Maturité (années)", value=10, min_value=1, max_value=50, step=1)
    frequency = st.sidebar.selectbox("Fréquence des paiements annuels", [1, 2], index=1) # 1 for annual, 2 for semi-annual

    # Create Bond object
    bond = Bond(nominal, coupon_rate, maturity, frequency)

    # --- Calculations ---
    price = bond.price(curve)
    duration = macaulay_duration(bond, curve)
    # You can add more metrics here as needed, e.g., modified_duration, convexity, dv01

    # --- Display Results ---
    st.subheader("Résultats du Pricing")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Prix de l'Obligation", f"{price:,.2f} MAD")
    with col2:
        st.metric("Duration de Macaulay", f"{duration:.4f} ans")

    # --- Plotting Zero Curve ---
    st.subheader("Courbe de Taux Zéro")
    fig = px.line(curve_df, x="tenor", y="rate", markers=True, title="Courbe de Taux Zéro (Taux Annuel)")
    fig.update_layout(xaxis_title="Ténor (années)", yaxis_title="Taux Zéro (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("--- ")
    st.info("Note: Les taux sont affichés en pourcentage mais sont utilisés sous forme décimale dans les calculs.")

    # --- Diagnostic Code (Temporarily add to your app.py) ---
    st.subheader("Diagnostic de l'environnement de déploiement")
    st.write(f"Répertoire de travail actuel: {os.getcwd()}")
    st.write(f"Chemins Python (sys.path): {sys.path}")
    st.write("Contenu du répertoire courant:")
    for item in os.listdir('.'):
        st.write(f"- {item}")
    # --- Fin du code de diagnostic ---

else:
    st.warning("Impossible de charger les données de la courbe de taux. Veuillez vérifier le fichier 'courbe_taux.csv'.")

# Display the original content of the files for reference (optional, good for debugging/development)
# st.subheader("Contenu des fichiers (pour le débogage)")
# st.code(open('bond.py').read(), language='python')
# st.code(open('courbe_zero.py').read(), language='python')
# st.code(open('risque.py').read(), language='python')
