import streamlit as st
import pandas as pd
import numpy as np
from time import sleep
from bs4 import BeautifulSoup 
import requests as r
import datetime
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
st.title('WRLDC Real Time Grid Frequency Analysis')
st.header('INFO')
st.write('This webapp fetches information from WRLDC website to get realtime data')
st.write('The final data is automatically downloaded as .csv file at the end of runtime')
f = []
dem = []
dev = []
dat = []
ref = 0
progress = st.progress(0)
rer = 0

def main():
    url = 'https://www.wrldc.in/'
    page = r.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    freq = soup.find(id = 'dataFrequency').text
    freq = float(freq)
    demand = soup.find(id = 'dataDemand').text
    demand = int(demand)
    dev_rate = soup.find(id = 'dataDeviationRate').text
    dev_rate = float(dev_rate)
    date_time = soup.find(id = 'dataDateTime').text
    #date_time = datetime.datetime.strptime(date_time, '%d-%b-%Y %H:%M:')
    #print(freq,demand,dev_rate,date_time)
    return freq,demand,dev_rate,date_time

def show_plot(f,dem,dev):
    st.write('Frequency Plot Complete')
    st.write(st.line_chart(f))
    st.write('Demand Plot Complete')
    st.write(st.line_chart(dem))
    st.write('Deviation Plot Complete')
    st.write(st.line_chart(dev))
    
    

def set_parmm():
    st.write('Set parameters')
    st.write('Run Time (Default = 1 hour)')
    runtime = st.slider('Runtime (hours)',min_value = 1, max_value = 24, value = 1,step = 1)
    st.write('Set data frequency (No. of data per minute, DEFAULT = 1)')
    datafreq = st.slider('Data Freq',min_value = 0.01, max_value = 2.0, value = 1.0,step = 0.005)
    return runtime, datafreq
        


def execute(i):
    x = main()
    f.append(x[0])
    dem.append(x[1])
    dev.append(x[2])
    dat.append(x[3])
    sleep(60 / par[1])
    df = pd.DataFrame(data={'date':dat,'frequency':f,'demand':dem,'Deviation rs/unit':dev})
    st.write(df.loc[[len(df)-1]])
    global data
    data = df
    animate(i)
    #ref = ref + 1
    #st.write('Progress: ')
    #progress.progress(ref/(par[0]*2))
    
        
    #if ref == 1440:
    #    st.write('24 hour data')
    #    st.write(df)
    #    progress24.empty()
    #    progress24 = st.progress(0)
    #    del f[:]
    #    del dem[:]
    #    del dev[:]
    #    del dat[:]
    #    ref = 0
    #if rer == 4320:
    #    st.caching.clear_cache()
    #    from streamlit.ScriptRunner import RerunException
    #    raise RerunException

    
    #show_plot(f,dem,dev,df,ref)
#if st.button('Show Plots and Data',key = 'show'):
    
par = set_parmm()

def animate(i):
    line.set_ydata(data.frequency[len(data)-1])
    the_plot.pyplot(plt)
    
    

st.write('Click here to run program:')
if st.button('RUN'):
    st.write('Instantaneous frequency Plot')
    st.write('Fetching Real Time Data')
    fig,ax = plt.subplots()
    max_x = 20
    max_rand = 20
    x = np.arange(0,max_rand)
    ax.set_ylim(49.85,50.15)
    line, = ax.plot(x,np.random.randint(0,max_rand,max_x))
    the_plot = st.pyplot(plt)
    line.set_ydata([np.nan]*len(x))
                    
    for i in range(0,par[0]*60):
        execute(i)
    
    show_plot(f,dem,dev)
    st.write(data)
    st.write('Downloading Data')
    data.to_csv('Result.csv', index = False)
    del f[:]
    del dem[:]
    del dev[:]
    del dat[:]
    ref = 0
    #progress.empty()
    #progress = st.progress(0)
    #result()
    

    
