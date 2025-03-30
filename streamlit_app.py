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
  
with st.expander('Data visualization'):
  _lock = RLock()
  x = df.iloc[:,0]
  y = df.iloc[:,1]
  with _lock:
    fig, ax = plt.subplots()
    ax.scatter(x,y)
    st.pyplot(fig)

#Parameters
with st.sidebar:
  st.header('Input features')
  flow_rate = st.slider("Flow Rate (sccm)", min_value=1, max_value=500, value=100)
  start_time = st.slider("Start Time (sec)", min_value=0, max_value=36000, value=0)
  end_time = st.slider("End Time (sec)", min_value=0, max_value=36000, value=600)

#Data frame for input features
input_data = {'flow_rate':flow_rate,
              'start_time':start_time,
              'end_time':end_time}
with st.expander('Input parameters'):
  input_df = pd.DataFrame(input_data, index=[0])
  input_df
    



