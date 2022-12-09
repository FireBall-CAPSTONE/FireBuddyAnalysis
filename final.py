import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import datetime

df = pd.read_csv('cneos_fireball_data.csv')
df['Peak Brightness Date/Time (UT)']= pd.to_datetime(df['Peak Brightness Date/Time (UT)'])
df['date'] = pd.to_datetime(df['Peak Brightness Date/Time (UT)'].dt.date)
df['year'] = df['Peak Brightness Date/Time (UT)'].dt.year
df['quarter'] = df['Peak Brightness Date/Time (UT)'].dt.quarter
df['month'] = df['Peak Brightness Date/Time (UT)'].dt.month
df['day'] = df['Peak Brightness Date/Time (UT)'].dt.day
df['weekday'] = df['Peak Brightness Date/Time (UT)'].dt.weekday
df['hour'] = df['Peak Brightness Date/Time (UT)'].dt.hour
df['minute'] = df['Peak Brightness Date/Time (UT)'].dt.minute
df['second'] = df['Peak Brightness Date/Time (UT)'].dt.second
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

df['Lat'] = df.apply(lambda row: lat(row), axis=1)
df['Long'] = df.apply(lambda row: long(row), axis=1)

df['vx2'] = df['vx']**2
df['vy2'] = df['vy']**2
df['vz2'] = df['vz']**2
df['vel2'] = df['Velocity (km/s)']**2

df = df.drop(['Latitude (deg.)', 'Longitude (deg.)'], axis=1)

df.corr().style.background_gradient(cmap='coolwarm', axis=None)



plt.scatter(np.log(df['Total Radiated Energy (J)']), np.log(df['Calculated Total Impact Energy (kt)']))



selection = alt.selection(type='interval', encodings=['x'])

base = alt.Chart().mark_bar().encode(
    x=alt.X(alt.repeat('column'), type='quantitative'),
    y=alt.Y(aggregate='count', type='quantitative')
).properties(
    width=225,
    height=130
)
    
# gray background with selection
background = base.encode(
    color=alt.value('#ddd')
).add_selection(selection)

# blue highlights on the transformed data
highlight = base.transform_filter(selection)

line = alt.Chart().mark_rule(color='firebrick').encode(
    x=alt.X(alt.repeat('column'), aggregate='mean', type='quantitative'),
    size=alt.SizeValue(3)
).transform_filter(selection)

# layer the three charts & repeat
group_chrt = alt.layer(
    background,
    highlight,
    line,
    data=df
)

alt.vconcat(
    group_chrt.repeat(column=["year", "quarter", "month"]),
    group_chrt.repeat(column=["day", "weekday"]),
    group_chrt.repeat(column=["hour", "minute", "second"])
)
