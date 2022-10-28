import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

@st.cache()
def load_data():
    df = pd.read_csv('cneos_fireball_data.csv')
    
    df['Peak Brightness Date/Time (UT)']= pd.to_datetime(df['Peak Brightness Date/Time (UT)'])
    df['date'] = df['Peak Brightness Date/Time (UT)'].dt.date
    df['year'] = df['Peak Brightness Date/Time (UT)'].dt.year
    df['quarter'] = df['Peak Brightness Date/Time (UT)'].dt.quarter
    df['month'] = df['Peak Brightness Date/Time (UT)'].dt.month
    df['day'] = df['Peak Brightness Date/Time (UT)'].dt.day
    df['weekday'] = df['Peak Brightness Date/Time (UT)'].dt.weekday
    df['time'] = df['Peak Brightness Date/Time (UT)'].dt.time
    df['hour'] = df['Peak Brightness Date/Time (UT)'].dt.hour
    df['minute'] = df['Peak Brightness Date/Time (UT)'].dt.minute
    df['second'] = df['Peak Brightness Date/Time (UT)'].dt.second
    
    df['Lat'] = df.apply(lambda row: lat(row), axis=1)
    df['Long'] = df.apply(lambda row: long(row), axis=1)
    df.drop(['Latitude (deg.)', 'Longitude (deg.)'], axis=1)
    return df

def lat(row):
    if row['Latitude (deg.)'] == row['Latitude (deg.)']:
        if row['Latitude (deg.)'][-1] == 'N':
            return float(row['Latitude (deg.)'][:-1])
        elif row['Latitude (deg.)'][-1] == 'S':
            return float('-'+(row['Latitude (deg.)'][:-1]))
    return np.nan

def long(row):
    if row['Longitude (deg.)'] == row['Longitude (deg.)']:
        if row['Longitude (deg.)'][-1] == 'E':
            return float(row['Longitude (deg.)'][:-1])
        elif row['Longitude (deg.)'][-1] == 'W':
            return float('-'+(row['Longitude (deg.)'][:-1]))
    return np.nan



fireballs_df = load_data()

st.title("FireBuddy")

selection = alt.selection(type='interval', encodings=['x'])

if st.sidebar.checkbox('Data'):
    st.write(fireballs_df)

if st.sidebar.checkbox('Frequency Charts'):
    col = ['year', 'quarter', 'month', 'day', 'weekday', 'hour', 'minute', 'second']
    option = st.selectbox('Pick one', col)
    
    freq = alt.Chart(fireballs_df).mark_bar().encode(
        alt.X(col),
        alt.Y(aggregate='count', type='quantitative')
    ).properties(
        title='Frequency Of Fireballs',
        width=600,
        height=400
    ).interactive()
    
    st.write(freq)