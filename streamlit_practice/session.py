import streamlit as st
import pandas as pd

st.header("Session State Mekanizması: Pratik Kullanım")

if "satir_sayisi" not in st.session_state:
    st.session_state.satir_sayisi = 10

dataframe = pd.read_csv("data.csv", sep=",")

st.table(dataframe.head(st.session_state.satir_sayisi))

def artir():
    st.session_state.satir_sayisi += 1

def dusur():
    st.session_state.satir_sayisi -= 1

artir_btn = st.button(label="Artır 👆", on_click=artir)
dusur_btn = st.button(label="Düşür 👇", on_click=dusur)

st.divider()
st.header(st.session_state.satir_sayisi)
