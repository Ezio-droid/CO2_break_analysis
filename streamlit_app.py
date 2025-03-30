import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from threading import RLock

st.title('💨 CO2 BCA App')

st.info('This app help in analyzing CO2 breakthrough curves')

with st.expander('Data'):
  st.write('**Raw data**')
  df = pd.read_csv('https://raw.githubusercontent.com/Ezio-droid/data/refs/heads/main/combine_data_blank_processed_cp.dat')
  df.columns = ['Time', 'CO2']
  df


#_lock = RLock()

#x = df.iloc[:,0]
#y = df.iloc[:,1]

#with _lock:
#  fig, ax = plt.subplots()
#  ax.scatter(x,y)
#  st.pyplot(fig)
with st.expander('Data visualization'):
  _lock = RLock()
  x = df.iloc[:,0]
  y = df.iloc[:,1]
  with _lock:
    fig, ax = plt.subplots()
    ax.scatter(x,y)
    st.pyplot(fig)
    



