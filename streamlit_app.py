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
  st.header('Input features')
  st.subheader('Adsorption', divider=True)
  flow_rate_a = st.slider("Flow Rate Adsorption (sccm)", min_value=1.00, max_value=500.00, value=111.00)
  start_time_a = st.slider("Start Time Adsorption (sec)", min_value=0, max_value=36000, value=0)
  end_time_a = st.slider("End Time Adsorption (sec)", min_value=0, max_value=36000, value=600)
  initial_conc_a = st.slider("Initial concentration Adsorption (%CO2)", min_value=1.00, max_value=15.00, value=0.01)
  

  st.subheader('Desorption', divider=True)
  flow_rate_d = st.slider("Flow Rate Desorption (sccm)", min_value=1.00, max_value=500.00, value=111.00)
  start_time_d = st.slider("Start Time Desorption (sec)", min_value=0, max_value=36000, value=0)
  end_time_d = st.slider("End Time Desorption (sec)", min_value=0, max_value=36000, value=600)
  initial_conc_d = st.slider("Initial concentration Desorption (%CO2)", min_value=1.00, max_value=15.00, value=0.01)



#Data frame for input features
input_data_a = {'flow_rate_ads':flow_rate_a,
              'start_time_ads':start_time_a,
              'end_time_ads':end_time_a,
             'initial_conc_ads':initial_conc_a}
input_data_d = {'flow_rate_des':flow_rate_d,
              'start_time_des':start_time_d,
              'end_time_des':end_time_d,
             'initial_conc_des':initial_conc_d}

with st.expander('Input parameters'):
  st.badge("Adsorption",icon=":material/check:", color="green")
  input_df_a = pd.DataFrame(input_data_a, index=[0])
  edited_df_a = st.data_editor(input_df_a)
  #edited_df_a
  st.badge("Desorption", icon=":material/check:", color="green")
  input_df_d = pd.DataFrame(input_data_d, index=[0])
  edited_df_d = st.data_editor(input_df_d)

mask_a = (x >= start_time_a) & (x <= end_time_a)
mask_d = (x >= start_time_d) & (x <= end_time_d)
x_filtered_a = x[mask_a]
x_filtered_d = x[mask_d]
y_filtered_a = y[mask_a]
y_filtered_d = y[mask_d]

y_diff_a = np.abs(y_filtered_a - initial_conc_a)
area_percentage_co2_sec_a = np.trapz(y_diff_a, x_filtered_a)
area_fractional_co2_sec_a = area_percentage_co2_sec_a / 100
volume_cm3_a = area_fractional_co2_sec_a * (flow_rate_a / 60)

y_diff_d = np.abs(y_filtered_d - initial_conc_d)
area_percentage_co2_sec_d = np.trapz(y_diff_d, x_filtered_d)
area_fractional_co2_sec_d = area_percentage_co2_sec_d / 100
volume_cm3_d = area_fractional_co2_sec_d * (flow_rate_d / 60)

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
    fig.add_trace(go.Scatter(x=x_filtered_a/60, y=y_filtered_a, mode='lines', name='CO2 concentration'))
    
    # Horizontal line for initial concentration
    fig.add_trace(go.Scatter(x=x_filtered_a/60, y=[initial_conc_a]*len(x_filtered_a/60), mode='lines', 
                             line=dict(color='red', dash='dash'), name=f'y = {initial_conc_a}'))
    
    # Shaded area above and below initial concentration
    fig.add_trace(go.Scatter(x=x_filtered_a/60, y=y_filtered_a, fill='tonexty', mode='none', 
                             fillcolor='rgba(0,100,200,0.3)', name='Above Initial Conc'))
    fig.add_trace(go.Scatter(x=x_filtered_a/60, y=[initial_conc_a]*len(x_filtered_a/60), fill='tonexty', mode='none', 
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
  volume_cm3_a

with st.expander('Visualization of desorbed volume'):
    fig = go.Figure()
    
    # Line plot for CO2 concentration
    fig.add_trace(go.Scatter(x=x_filtered_d/60, y=y_filtered_d, mode='lines', name='CO2 concentration'))
    
    # Horizontal line for initial concentration
    fig.add_trace(go.Scatter(x=x_filtered_d/60, y=[initial_conc_d]*len(x_filtered_d/60), mode='lines', 
                             line=dict(color='red', dash='dash'), name=f'y = {initial_conc_d}'))
    
    # Shaded area above and below initial concentration
    fig.add_trace(go.Scatter(x=x_filtered_d/60, y=y_filtered_d, fill='tonexty', mode='none', 
                             fillcolor='rgba(0,100,200,0.3)', name='Above Initial Conc'))
    fig.add_trace(go.Scatter(x=x_filtered_d/60, y=[initial_conc_d]*len(x_filtered_d/60), fill='tonexty', mode='none', 
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
  volume_cm3_d





    



