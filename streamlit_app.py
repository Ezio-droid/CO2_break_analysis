import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from threading import RLock
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

st.title('💨 CO2 BCA App')

st.info('This app help in analyzing CO2 breakthrough curves')

with st.expander('Data'):
  st.write('**Raw data**')
  df = pd.read_csv('https://raw.githubusercontent.com/Ezio-droid/data/refs/heads/main/combine_data_r10.dat', delim_whitespace=True, header=None)
  df['time (sec)'] = df[0] - df.iloc[0,0]
  df
  
#with st.expander('Data visualization'):
#  _lock = RLock()
#  x = df['time (sec)'].values
#  y = df.iloc[:,5].values
#  with _lock:
#    fig, ax = plt.subplots()
#    ax.scatter(x,y, s=1)
#    plt.xlabel('Time (sec)')
#    plt.ylabel('CO2 concentration (%)')
#    plt.grid(True)
#    st.pyplot(fig)
with st.expander('Data visualization'):
  x = df['time (sec)'].values
  y = df.iloc[:,5].values
  fig = px.scatter(x= df['time (sec)'].values,y= df.iloc[:,5].values, 
    labels={'x': 'Time (sec)', 'y': '% CO2'}, 
    title='Scatter Plot')
  fig.update_traces(marker=dict(size=2))  # Adjust marker size
  fig.update_layout(
    template='plotly_white',
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    #width=900,
    #height=400
  )

  st.plotly_chart(fig, theme="streamlit", use_container_width=True)



#Parameters
with st.sidebar:
  st.header('Input features for adsorption')
  flow_rate_a = st.slider("Flow Rate (sccm)", min_value=1.00, max_value=500.00, value=111.00)
  start_time_a = st.slider("Start Time (sec)", min_value=0, max_value=36000, value=0)
  end_time_a = st.slider("End Time (sec)", min_value=0, max_value=36000, value=600)
  initial_conc_a = st.slider("Initial concentration (%CO2)", min_value=1.00, max_value=15.00, value=0.01)

with st.sidebar:
  st.header('Input features for desorption')
  flow_rate_d = st.slider("Flow Rate (sccm)", min_value=1.00, max_value=500.00, value=111.00)
  start_time_d = st.slider("Start Time (sec)", min_value=0, max_value=36000, value=0)
  end_time_d = st.slider("End Time (sec)", min_value=0, max_value=36000, value=600)
  initial_conc_d = st.slider("Initial concentration (%CO2)", min_value=1.00, max_value=15.00, value=0.01)

#Data frame for input features
input_data = {'flow_rate':flow_rate_a,
              'start_time':start_time_a,
              'end_time':end_time_a,
             'initial_conc':initial_conc_a}
with st.expander('Input parameters'):
  input_df = pd.DataFrame(input_data, index=[0])
  edited_df = st.data_editor(input_df)
  edited_df

mask = (x >= start_time_a) & (x <= end_time_a)
x_filtered = x[mask]
y_filtered = y[mask]

y_diff = np.abs(y_filtered - initial_conc_a)
area_percentage_co2_sec = np.trapz(y_diff, x_filtered)
area_fractional_co2_sec = area_percentage_co2_sec / 100
volume_cm3 = area_fractional_co2_sec * (flow_rate_a / 60)

#with st.expander('Visualization od adsorbed volume'):
#  _lock = RLock()
#  with _lock:
#    fig, ax = plt.subplots()
#    plt.plot(x_filtered, y_filtered, label= 'CO2 concentration')
#    plt.axhline(y=initial_conc, color= 'r', linestyle='--', label= f'y = {initial_conc}')
#    plt.fill_between(x_filtered, y_filtered, initial_conc, where=(y_filtered > initial_conc), interpolate=True, alpha=0.3)
#    plt.fill_between(x_filtered, y_filtered, initial_conc, where=(y_filtered < initial_conc), interpolate=True, alpha=0.3)
#    plt.xlabel('Time (sec)')
#    plt.ylabel('CO2 concentration (%)')
#    plt.grid(True)
#    plt.legend()
#    plt.title('CO2 Concentration vs Time within the specified range')
#    st.pyplot(fig)

with st.expander('Visualization of adsorbed volume'):
    fig = go.Figure()
    
    # Line plot for CO2 concentration
    fig.add_trace(go.Scatter(x=x_filtered/60, y=y_filtered, mode='lines', name='CO2 concentration'))
    
    # Horizontal line for initial concentration
    fig.add_trace(go.Scatter(x=x_filtered/60, y=[initial_conc_a]*len(x_filtered/60), mode='lines', 
                             line=dict(color='red', dash='dash'), name=f'y = {initial_conc_a}'))
    
    # Shaded area above and below initial concentration
    fig.add_trace(go.Scatter(x=x_filtered/60, y=y_filtered, fill='tonexty', mode='none', 
                             fillcolor='rgba(0,100,200,0.3)', name='Above Initial Conc'))
    fig.add_trace(go.Scatter(x=x_filtered/60, y=[initial_conc_a]*len(x_filtered/60), fill='tonexty', mode='none', 
                             fillcolor='rgba(200,100,0,0.3)', name='Below Initial Conc'))
    
    fig.update_layout(
        title='CO2 Concentration vs Time within the specified range',
        xaxis_title='Time (min)',
        yaxis_title='CO2 concentration (%)',
        template='plotly_white',
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with st.expander('CO2 adsorbed volume (cm3)'):
  volume_cm3




    



