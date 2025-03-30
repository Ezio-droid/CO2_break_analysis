import streamlit as st
import pandas as pd

st.title('💨 CO2 BCA App')

st.info('This app help in analyzing CO2 breakthrough curves')

df = pd.read_csv('https://raw.githubusercontent.com/Ezio-droid/data/refs/heads/main/combine_data_blank_processed_cp.dat')
df
