import streamlit as st
import pandas as pd
import plotly.express as px
from bond import Bond
from courbe_zero import ZeroCurve
from risque import macaulay_duration, modified_duration, convexity, dv01

st.set_page_config(page_title="Pricer Obligataire Maroc",layout="wide")
st.title("Pricer Obligataire Maroc")
curve_df=pd.read_csv("courbe_taux.csv")
curve=ZeroCurve(curve_df["tenor"],curve_df["rate"])
nominal=st.number_input("Nominal",value=1000000)
coupon=st.number_input("Coupon %",value=3.5)/100
maturity=st.number_input("Maturite",value=10)
frequency=st.selectbox("Frequence",[1,2])
bond=Bond(nominal,coupon,maturity,frequency)
price=bond.price(curve)
st.metric("Prix",f"{price:,.2f} MAD")
st.metric("Duration",f"{macaulay_duration(bond,curve):.4f}")
fig=px.line(curve_df,x="tenor",y="rate",markers=True)
st.plotly_chart(fig,use_container_width=True)

