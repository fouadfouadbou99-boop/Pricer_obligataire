import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Portefeuille Obligataire Maroc",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Portefeuille Obligataire Maroc")

# =====================================================
# CHARGEMENT DES DONNEES
# =====================================================

try:

    portefeuille = pd.read_excel(
        "RPC_bonds_data_rpc.xlsx",
        engine="openpyxl"
    )

except Exception as e:

    st.error(
        f"Erreur lors du chargement du portefeuille : {e}"
    )

    st.stop()

try:

    courbe = pd.read_csv(
        "courbe_taux.csv"
    )

except Exception as e:

    st.error(
        f"Erreur lors du chargement de la courbe : {e}"
    )

    st.stop()

# =====================================================
# NETTOYAGE DES DONNEES
# =====================================================

portefeuille.columns = [
    str(col).strip()
    for col in portefeuille.columns
]

for colonne in [
    "Nominal Global",
    "Taux facial",
    "TRA"
]:

    if colonne in portefeuille.columns:

        portefeuille[colonne] = pd.to_numeric(
            portefeuille[colonne],
            errors="coerce"
        )

# =====================================================
# INDICATEURS CLES
# =====================================================

nominal_total = 0
coupon_moyen = 0
tra_moyen = 0

if "Nominal Global" in portefeuille.columns:

    nominal_total = portefeuille[
        "Nominal Global"
    ].fillna(0).sum()

if "Taux facial" in portefeuille.columns:

    coupon_moyen = (
        portefeuille["Taux facial"]
        .fillna(0)
        .mean()
        * 100
    )

if "TRA" in portefeuille.columns:

    tra_moyen = (
        portefeuille["TRA"]
        .fillna(0)
        .mean()
        * 100
    )

nombre_positions = len(portefeuille)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Nominal Total",
        f"{nominal_total:,.0f} MAD"
    )

with col2:

    st.metric(
        "Nombre Positions",
        nombre_positions
    )

with col3:

    st.metric(
        "Coupon Moyen",
        f"{coupon_moyen:.2f}%"
    )

with col4:

    st.metric(
        "TRA Moyen",
        f"{tra_moyen:.2f}%"
    )

# =====================================================
# TABLEAU PORTEFEUILLE
# =====================================================

st.subheader("Portefeuille Obligataire")

colonnes = [
    "Code",
    "Description Titres",
    "Date Echéance",
    "Taux facial",
    "Nominal Global",
    "TRA"
]

colonnes_existantes = [
    c
    for c in colonnes
    if c in portefeuille.columns
]

st.dataframe(
    portefeuille[colonnes_existantes],
    use_container_width=True
)

# =====================================================
# TOP POSITIONS
# =====================================================

if (
    "Nominal Global" in portefeuille.columns
    and
    "Description Titres" in portefeuille.columns
):

    st.subheader("Top 10 Positions")

    top10 = portefeuille.nlargest(
        10,
        "Nominal Global"
    )

    fig_top = px.bar(
        top10,
        x="Description Titres",
        y="Nominal Global",
        title="Top 10 des positions"
    )

    st.plotly_chart(
        fig_top,
        use_container_width=True
    )

# =====================================================
# REPARTITION DES ENCOURS
# =====================================================

if (
    "Nominal Global" in portefeuille.columns
    and
    "Description Titres" in portefeuille.columns
):

    st.subheader("Répartition des Encours")

    top15 = portefeuille.nlargest(
        15,
        "Nominal Global"
    )

    fig_pie = px.pie(
        top15,
        values="Nominal Global",
        names="Description Titres"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# =====================================================
# COURBE DES TAUX
# =====================================================

st.subheader("Courbe des Taux")

fig_curve = px.line(
    courbe,
    x="tenor",
    y="rate",
    markers=True
)

fig_curve.update_layout(
    xaxis_title="Maturité",
    yaxis_title="Taux"
)

st.plotly_chart(
    fig_curve,
    use_container_width=True
)

# =====================================================
# DONNEES COURBE
# =====================================================

with st.expander(
    "Afficher les données de la courbe"
):

    st.dataframe(
        courbe,
        use_container_width=True
    )

# =====================================================
# DISTRIBUTION TRA
# =====================================================

if "TRA" in portefeuille.columns:

    st.subheader("Distribution des TRA")

    fig_tra = px.histogram(
        portefeuille,
        x="TRA",
        nbins=20
    )

    st.plotly_chart(
        fig_tra,
        use_container_width=True
    )

# =====================================================
# DISTRIBUTION COUPONS
# =====================================================

if "Taux facial" in portefeuille.columns:

    st.subheader(
        "Distribution des Coupons"
    )

    fig_coupon = px.histogram(
        portefeuille,
        x="Taux facial",
        nbins=20
    )

    st.plotly_chart(
        fig_coupon,
        use_container_width=True
    )

# =====================================================
# EXPORT
# =====================================================

@st.cache_data
def exporter_excel(df):

    from io import BytesIO

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False
        )

    return buffer.getvalue()


st.download_button(
    label="📥 Télécharger le portefeuille",
    data=exporter_excel(portefeuille),
    file_name="portefeuille.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =====================================================
# PIED DE PAGE
# =====================================================

st.markdown("---")

st.caption(
    "Dashboard Obligataire Maroc - Version Portefeuille"
)
