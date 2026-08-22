import streamlit as st
import pandas as pd
import plotly.express as px
import io

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

    st.error(
        f"Erreur courbe : {e}"
    )

    st.stop()

# ==================================================
# NORMALISATION
# ==================================================

portefeuille.columns = (
    portefeuille.columns
    .astype(str)
    .str.strip()
)

courbe.columns = (
    courbe.columns
    .astype(str)
    .str.strip()
)

if "Taux" in courbe.columns:
    courbe.rename(
        columns={"Taux": "rate"},
        inplace=True
    )

# ==================================================
# PREPARATION
# ==================================================

if "Date Echéance" in portefeuille.columns:

    portefeuille["Date Echéance"] = pd.to_datetime(
        portefeuille["Date Echéance"],
        errors="coerce"
    )

if "Taux facial" in portefeuille.columns:

    portefeuille["Taux facial"] = pd.to_numeric(
        portefeuille["Taux facial"],
        errors="coerce"
    )

if "Nominal Global" in portefeuille.columns:

    portefeuille["Nominal Global"] = pd.to_numeric(
        portefeuille["Nominal Global"],
        errors="coerce"
    )

# ==================================================
# KPI
# ==================================================

nominal_total = portefeuille.get(
    "Nominal Global",
    pd.Series(dtype=float)
).fillna(0).sum()

nombre_positions = len(portefeuille)

coupon_moyen = portefeuille.get(
    "Taux facial",
    pd.Series(dtype=float)
).fillna(0).mean()

if coupon_moyen < 1:
    coupon_moyen *= 100

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Nominal Total",
        f"{nominal_total:,.0f}".replace(",", " ")
        + " MAD"
    )

with col2:

    st.metric(
        "Nombre de lignes",
        nombre_positions
    )

with col3:

    st.metric(
        "Coupon Moyen",
        f"{coupon_moyen:.2f}%"
    )

# ==================================================
# VALORISATION
# ==================================================

st.subheader("💰 Valorisation approximative")

try:

    today = pd.Timestamp.today()

    portefeuille["Maturite"] = (
        portefeuille["Date Echéance"]
        - today
    ).dt.days / 365.25

    portefeuille["Maturite"] = (
        portefeuille["Maturite"]
        .clip(lower=0)
    )

    portefeuille["Valeur Marche"] = (
        portefeuille["Nominal Global"]
        /
        (
            (1 + portefeuille["Taux facial"])
            ** portefeuille["Maturite"]
        )
    )

    vm = portefeuille[
        "Valeur Marche"
    ].sum()

    pnl = vm - nominal_total

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Valeur de Marché",
            f"{vm:,.0f}".replace(",", " ")
            + " MAD"
        )

    with c2:

        st.metric(
            "Plus / Moins Value",
            f"{pnl:,.0f}".replace(",", " ")
            + " MAD"
        )

except:

    st.info(
        "Valorisation non disponible."
    )

# ==================================================
# ONGLETS
# ==================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📁 Portefeuille",
    "📈 Courbe",
    "🥧 Analyse",
    "⬇ Export"
])

# ==================================================
# PORTEFEUILLE
# ==================================================

with tab1:

    st.dataframe(
        portefeuille,
        use_container_width=True
    )

# ==================================================
# COURBE DES TAUX
# ==================================================

with tab2:

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
