import streamlit as st
import requests, json

import pandas as pd
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://img.freepik.com/free-vector/hand-drawn-winter-background_23-2148716428.jpg?size=626&ext=jpg")
        

    }
    .sidebar .sidebar-content {
        background: url("https://www.thespruce.com/thmb/usPkZyVKiegcU2PjScTktd0Vwp4=/1887x1415/smart/filters:no_upscale()/157497239-56a570855f9b58b7d0dceaa5.jpg")
    }
   
   
    </style>
    """,
    unsafe_allow_html=True
)

original_title = '<p style="font-family:Courier; color:Blue; font-size: 40px;"><b>winter weather live forecasting and foggy roads visibility prediction </b></p>'
st.markdown(original_title, unsafe_allow_html=True)
original_title1 = '<p style="font-family:Courier; color:Green; font-size: 20px;"><strong>Vehicles should be driven with extreme care during winter. Due to fog, visibility becomes low and so should the speed of vehicles, be it two-wheelers, four wheelers or transport vehicles. Get vehicles regularly serviced to avoid breakdown in fog. One should also be aware of and equipped with safety measures required at the time of breakdown of vehicles in fog, especially at night. Commuters should keep to pedestrian path while walking in fog and check on both sides before crossing the road.</strong></p>'
st.markdown(original_title1, unsafe_allow_html=True)
original_title2 = '<p style="font-family:Courier; color:Black; font-size: 20px;"><strong>Driving in winter becomes tricky and difficult owing to dense fog, especially during the night time. There are some major precautionary measures that ought to be adopted while driving. The first and foremost is drive slowly to maintain control over the vehicle to prevent accidents and loss in the case of applying sudden brakes. Stray cattle menace is also a major issue in the city. Thus, one has to be extra careful while driving on roads at night.</strong></p>'
st.markdown(original_title2, unsafe_allow_html=True)

import requests
from bs4 import BeautifulSoup


st.sidebar.title("Live weather ")
city = st.sidebar.text_input("Enter city name ")

# creating url and requests instance
url = "https://www.google.com/search?q="+"weather"+city
html = requests.get(url).content
 
# getting raw data
soup = BeautifulSoup(html, 'html.parser')
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
 
# formatting data
data = str.split('\n')
time = data[0]
sky = data[1]
 
# getting all div tag
listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
strd = listdiv[5].text
 
# getting other required data
pos = strd.find('Wind')
other_data = strd[pos:]
if st.sidebar.button('enter '):
     st.sidebar.write("Temperature is", temp)
     st.sidebar.write("Time: ", time)
     st.sidebar.write("Sky Description: ", sky)
     st.sidebar.write(other_data)

