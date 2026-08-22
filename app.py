import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

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
# FONCTIONS UTILES
# ==================================================

def format_montant(x):
    if pd.isna(x):
        return "0 MAD"

    if x >= 1_000_000_000:
        return f"{x/1_000_000_000:.2f} MMDH"

    if x >= 1_000_000:
        return f"{x/1_000_000:.2f} MDH"

    return f"{x:,.0f} MAD"


def telecharger_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    return output.getvalue()


# ==================================================
# CHARGEMENT DES DONNEES
# ==================================================

st.sidebar.header("📂 Chargement des données")

# -----------------------------
# Portefeuille
# -----------------------------

fichier_portefeuille = st.sidebar.file_uploader(
    "📁 Charger le portefeuille",
    type=["xlsx"]
)

try:

    if fichier_portefeuille is not None:

        portefeuille = pd.read_excel(
            fichier_portefeuille,
            engine="openpyxl"
        )

        st.sidebar.success("✅ Portefeuille chargé")

    else:

        portefeuille = pd.read_excel(
            "RPC_bonds_data_rpc.xlsx",
            engine="openpyxl"
        )

except Exception as e:

    st.error(f"Erreur portefeuille : {e}")
    st.stop()

# -----------------------------
# Courbe
# -----------------------------

fichier_courbe = st.sidebar.file_uploader(
    "📈 Charger la courbe des taux",
    type=["csv", "xlsx"]
)

try:

    if fichier_courbe is not None:

        if fichier_courbe.name.endswith(".csv"):
            courbe = pd.read_csv(fichier_courbe)

        else:
            courbe = pd.read_excel(
                fichier_courbe,
                engine="openpyxl"
            )

        st.sidebar.success("✅ Courbe chargée")

    else:

        courbe = pd.read_csv(
            "courbe_taux.csv"
        )

except Exception as e:

    st.error(f"Erreur courbe : {e}")
    st.stop()

# ==================================================
# NETTOYAGE
# ==================================================

portefeuille.columns = portefeuille.columns.astype(str).str.strip()
courbe.columns = courbe.columns.astype(str).str.strip()

if "Taux" in courbe.columns:
    courbe.rename(
        columns={"Taux": "rate"},
        inplace=True
    )

# ==================================================
# CONVERSIONS
# ==================================================

colonnes_numeriques = [
    "Taux facial",
    "TRA",
    "Nominal Global",
    "Quantité",
    "Spread"
]

for col in colonnes_numeriques:

    if col in portefeuille.columns:

        portefeuille[col] = pd.to_numeric(
            portefeuille[col],
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

coupon_moyen = 0

if {
    "Taux facial",
    "Nominal Global"
}.issubset(portefeuille.columns):

    coupon_moyen = (
        portefeuille["Taux facial"]
        * portefeuille["Nominal Global"]
    ).sum() / portefeuille["Nominal Global"].sum()

coupon_moyen *= 100

tra_moyen = 0

if {
    "TRA",
    "Nominal Global"
}.issubset(portefeuille.columns):

    tra_moyen = (
        portefeuille["TRA"]
        * portefeuille["Nominal Global"]
    ).sum() / portefeuille["Nominal Global"].sum()

tra_moyen *= 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nominal Total",
        format_montant(nominal_total)
    )

with col2:
    st.metric(
        "Nombre de lignes",
        nombre_positions
    )

with col3:
    st.metric(
        "Coupon Moyen Pondéré",
        f"{coupon_moyen:.2f}%"
    )

with col4:
    st.metric(
        "TRA Moyen Pondéré",
        f"{tra_moyen:.2f}%"
    )

# ==================================================
# TABLEAU PORTEFEUILLE
# ==================================================

st.subheader("📁 Portefeuille")

colonnes = [
    "Code",
    "Description Titres",
    "Date Echéance",
    "Taux facial",
    "Quantité",
    "Nominal Global",
    "Spread",
    "TRA"
]

colonnes_existantes = [
    c for c in colonnes
    if c in portefeuille.columns
]

st.dataframe(
    portefeuille[colonnes_existantes],
    use_container_width=True,
    height=500
)

# ==================================================
# EXPORT EXCEL
# ==================================================

fichier_excel = telecharger_excel(portefeuille)

st.download_button(
    label="📥 Télécharger le portefeuille",
    data=fichier_excel,
    file_name="portefeuille_obligataire.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ==================================================
# GRAPHIQUES
# ==================================================

st.subheader("📊 Analyse du portefeuille")

colg1, colg2 = st.columns(2)

# -----------------------------
# Top titres
# -----------------------------

with colg1:

    if {
        "Description Titres",
        "Nominal Global"
    }.issubset(portefeuille.columns):

        top = portefeuille.sort_values(
            "Nominal Global",
            ascending=False
        ).head(10)

        fig = px.bar(
            top,
            x="Nominal Global",
            y="Description Titres",
            orientation="h",
            title="Top 10 Encours"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# -----------------------------
# Répartition TRA
# -----------------------------

with colg2:

    if "TRA" in portefeuille.columns:

        fig = px.histogram(
            portefeuille,
            x="TRA",
            nbins=20,
            title="Distribution des TRA"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==================================================
# REPARTITION PAR ECHEANCE
# ==================================================

if "Date Echéance" in portefeuille.columns:

    st.subheader("📅 Répartition des échéances")

    portefeuille["Date Echéance"] = pd.to_datetime(
        portefeuille["Date Echéance"],
        errors="coerce"
    )

    fig = px.histogram(
        portefeuille,
        x="Date Echéance",
        title="Répartition des maturités"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# COURBE DES TAUX
# ==================================================

st.subheader("📈 Courbe des Taux")

try:

    fig = px.line(
        courbe,
        x="tenor",
        y="rate",
        markers=True,
        title="Courbe des taux"
    )

    fig.update_layout(
        xaxis_title="Maturité (années)",
        yaxis_title="Taux",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Erreur graphique : {e}"
    )

# ==================================================
# DONNEES COURBE
# ==================================================

with st.expander(
    "Afficher les données de la courbe"
):

    st.dataframe(
        courbe,
        use_container_width=True
    )

# ==================================================
# STATISTIQUES
# ==================================================

st.subheader("📋 Statistiques")

st.write(portefeuille.describe())

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Dashboard Obligataire Maroc - Version Améliorée"
)
