import streamlit as st
import pandas as pd
import plotly.express as px

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
2
# CHARGEMENT DES DONNEES
3
# ==================================================
4
 
5
st.sidebar.header("📂 Chargement des données")
6
 
7
# ----------------------------------------
8
# PORTEFEUILLE
9
# ----------------------------------------
10
 
11
fichier_portefeuille = st.sidebar.file_uploader(
12
"📁 Charger le portefeuille",
13
type=["xlsx"]
14
)
15
 
16
try:
17
 
18
if fichier_portefeuille is not None:
19
 
20
portefeuille = pd.read_excel(
21
fichier_portefeuille,
22
engine="openpyxl"
23
)
24
 
25
st.sidebar.success(
26
"Portefeuille chargé"
27
)
28
 
29
else:
30
 
31
portefeuille = pd.read_excel(
32
"RPC_bonds_data_rpc.xlsx",
33
engine="openpyxl"
34
)
35
 
36
except Exception as e:
37
 
38
st.error(
39
f"Erreur chargement portefeuille : {e}"
40
)
41
 
42
st.stop()
43
 
44
# ----------------------------------------
45
# COURBE DES TAUX
46
# ----------------------------------------
47
 
48
fichier_courbe = st.sidebar.file_uploader(
49
"📈 Charger la courbe des taux",
50
type=["xlsx", "csv"]
51
)
52
 
53
try:
54
 
55
if fichier_courbe is not None:
56
 
57
if fichier_courbe.name.endswith(".csv"):
58
 
59
courbe = pd.read_csv(
60
fichier_courbe
61
)
62
 
63
else:
64
 
65
courbe = pd.read_excel(
66
fichier_courbe,
67
engine="openpyxl"
68
)
69
 
70
st.sidebar.success(
71
"Courbe chargée"
72
)
73
 
74
else:
75
 
76
courbe = pd.read_csv(
77
"courbe_taux.csv"
78
)
79
 
80
except Exception as e:
81
 
82
st.error(
83
f"Erreur chargement courbe : {e}"
84
)
85
 
86
st.stop()

# ==================================================
2
# COURBE DES TAUX
3
# ==================================================
4
 
5
st.subheader("📈 Courbe des Taux")
6
 
7
courbe.columns = [
8
str(col).strip()
9
for col in courbe.columns
10
]
11
 
12
if "Taux" in courbe.columns:
13
 
14
courbe.rename(
15
columns={
16
"Taux": "rate"
17
},
18
inplace=True
19
)
20
 
21
fig = px.line(
22
courbe,
23
x="tenor",
24
y="rate",
25
markers=True
26
)
27
 
28
fig.update_layout(
29
xaxis_title="Maturité",
30
yaxis_title="Taux"
31
)
32
 
33
st.plotly_chart(
34
fig,
35
use_container_width=True
36
)

# ==================================================
# PREPARATION
# ==================================================

portefeuille.columns = [
    str(col).strip()
    for col in portefeuille.columns
]

# ==================================================
# KPI
# ==================================================

nominal_total = 0

if "Nominal Global" in portefeuille.columns:

    nominal_total = pd.to_numeric(
        portefeuille["Nominal Global"],
        errors="coerce"
    ).fillna(0).sum()

nombre_positions = len(
    portefeuille
)

coupon_moyen = 0

if "Taux facial" in portefeuille.columns:

    coupon_moyen = (
        pd.to_numeric(
            portefeuille["Taux facial"],
            errors="coerce"
        ).fillna(0).mean()
    ) * 100

tra_moyen = 0

if "TRA" in portefeuille.columns:

    tra_moyen = (
        pd.to_numeric(
            portefeuille["TRA"],
            errors="coerce"
        ).fillna(0).mean()
    ) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Nominal Total",
        f"{nominal_total:,.0f} MAD"
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

with col4:

    st.metric(
        "TRA Moyen",
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
    c
    for c in colonnes
    if c in portefeuille.columns
]

st.dataframe(
    portefeuille[
        colonnes_existantes
    ],
    use_container_width=True
)

# ==================================================
# COURBE DES TAUX
# ==================================================

st.subheader(
    "📈 Courbe des Taux"
)

try:

    fig = px.line(
        courbe,
        x="tenor",
        y="rate",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Maturité",
        yaxis_title="Taux"
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
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Portefeuille Obligataire Maroc"
)
