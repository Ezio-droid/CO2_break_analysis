import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from threading import RLock
import numpy as np

st.title('💨 CO2 BCA App')

st.info('This app help in analyzing CO2 breakthrough curves')

with st.expander('Data'):
  st.write('**Raw data**')
  df = pd.read_csv('https://raw.githubusercontent.com/Ezio-droid/data/refs/heads/main/combine_data_r10.dat', delim_whitespace=True, header=None)
  df['time (sec)'] = df[0] - df.iloc[0,0]
  df
  
with st.expander('Data visualization'):
  _lock = RLock()
  x = df['time (sec)'].values
  y = df.iloc[:,5].values
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
  flow_rate = st.slider("Flow Rate (sccm)", min_value=1.00, max_value=500.00, value=111.00)
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
  edited_df = st.data_editor(input_df)
  edited_df

mask = (x >= start_time) & (x <= end_time)
x_filtered = x[mask]
y_filtered = y[mask]

y_diff = np.abs(y_filtered - initial_conc)
area_percentage_co2_sec = np.trapz(y_diff, x_filtered)
area_fractional_co2_sec = area_percentage_co2_sec / 100
volume_cm3 = area_fractional_co2_sec * (flow_rate / 60)

with st.expander('Visualization od adsorbed volume'):
  _lock = RLock()
  x = df['time (sec)'].values
  y = df.iloc[:,5].values
  with _lock:
    fig, ax = plt.subplots()
    plt.plot(x_filtered, y_filtered, s=1, label= 'CO2 concentration')
    plt.axhline(y=initial_conc, color= 'r', linestyle='--', label= f'y = {initial_conc}')
    plt.fill_between(x_filtered, y_filtered, initial_conc, where=(y_filtered > initial_conc), interpolate=True, alpha=0.3)
    plt.fill_between(x_filtered, y_filtered, initial_conc, where=(y_filtered < initial_conc), interpolate=True, alpha=0.3)
    plt.xlabel('Time (sec)')
    plt.ylabel('CO2 concentration (%)')
    plt.grid(True)
    plt.legend()
    plt.title('CO2 Concentration vs Time within the specified range')
    st.pyplot(fig)

with st.expander('CO2 adsorbed volume (cm3)'):
  volume_cm3


    



