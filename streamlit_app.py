import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from threading import RLock

st.title('💨 CO2 BCA App')

st.info('This app help in analyzing CO2 breakthrough curves')

with st.expander('Data'):
  st.write('**Raw data**')
  df = pd.read_csv('https://raw.githubusercontent.com/Ezio-droid/data/refs/heads/main/combine_data_blank_processed_cp.dat')
  df


_lock = RLock()

x = df.iloc[:,0]
y = df.iloc[:,1]

with _lock:
  fig, ax = plt.subplots()
  ax.scatter(x,y)
  st.pyplot(fig)

#plt.scatter(data_pei_silica_powder_black_lid_light_run8['time (sec)'], data_pei_silica_powder_black_lid_light_run8.iloc[:, 5], s=1)  # s controls marker size
#plt.xlim(6000, 15000)

#plt.xlabel('Time (sec)')
#plt.xlim(150000, 350000)
#plt.ylabel('% CO2')
##plt.title('Scatter Plot')
#plt.grid(True)
#plt.show()


