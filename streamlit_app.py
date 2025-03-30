import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from threading import RLock

st.title('💨 CO2 BCA App')

st.info('This app help in analyzing CO2 breakthrough curves')

with st.expander('Data'):
  st.write('**Raw data**')
  df = pd.read_csv('https://raw.githubusercontent.com/Ezio-droid/data/refs/heads/main/combine_data_r10.dat', delim_whitespace=True, header=None)
  df['time (sec)'] = df[0] - df.iloc[0,0]
  df
  
with st.expander('Data visualization'):
  _lock = RLock()
  x = df['time (sec)']
  y = df.iloc[:,5]
  with _lock:
    fig, ax = plt.subplots()
    ax.scatter(x,y, s=1)
    plt.xlabel('Time (sec)')
    plt.ylabel('CO2 concentration (%)')
    plt.grid(True)
    st.pyplot(fig)

#Parameters
with st.sidebar:
  st.header('Input features')
  flow_rate = st.slider("Flow Rate (sccm)", min_value=1, max_value=500, value=100)
  start_time = st.slider("Start Time (sec)", min_value=0, max_value=36000, value=0)
  end_time = st.slider("End Time (sec)", min_value=0, max_value=36000, value=600)
  initial_conc = st.slider("Initial concentration (%CO2)", min_value=1.00, max_value=15.00, value=0.01)

#Data frame for input features
input_data = {'flow_rate':flow_rate,
              'start_time':start_time,
              'end_time':end_time,
             'initial_conc':initial_conc}
with st.expander('Input parameters'):
  input_df = pd.DataFrame(input_data, index=[0])
  input_df

#with st.expander('Filtered data'):
#  mask = (x >=input_df['start_time']) & (x <= input_df['end_time'])
##  x_filtered = x[mask]
#  y_filtered = y[mask]
    



