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
import requests
from datetime import datetime , timedelta
import pandas as pd
import matplotlib.pyplot as plt
import time 

# INSERT YOUR API  KEY WHICH YOU PASTED IN YOUR secrets.toml file 
api_key =  "728a5f3a4e637ee1dd42aa3ec2e6f618"

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
url_1 = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}'

# Function for LATEST WEATHER DATA
def getweather(city):
    result = requests.get(url.format(city, api_key))     
    if result:
        json = result.json()
        #st.write(json)
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp,1),round(temp_feels,1),
                humid,lon,lat,icon,des]
        return res , json
    else:
        print("error in search !")

# Function for HISTORICAL DATA
def get_hist_data(lat,lon,start):
    res = requests.get(url_1.format(lat,lon,start,api_key))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)     
    return data , temp

# Let's write the Application

st.header('Winter Weather Report')   




col1, col2 = st.beta_columns(2)

with col1:
    city_name = st.text_input("Enter a city name")
    #show_hist = st.checkbox('Show me history')
    
with col2: 

		if city_name:
		        res , json = getweather(city_name)
		        #st.write(res)
		        st.write('Current: ' , (round(res[1],2)))
		        st.write('Feels Like: ' , (round(res[2],2)))
		        #st.info('Humidity: ' + str(round(res[3],2)))
		        st.subheader('Status: ' + res[7])
		        
if city_name:        
    show_hist = st.beta_expander(label = 'Last 5 Days History')
    with show_hist:
            start_date_string = st.date_input('Current Date')
            #start_date_string = str('2021-06-26')
            date_df = []
            max_temp_df = []
            for i in range(5):
                        date_Str = start_date_string - timedelta(i)
                        
                        start_date = datetime.strptime('2021-12-03',"%Y-%m-%d")
                        timestamp_1 = datetime.timestamp(start_date)
                        #res , json = getweather(city_name)
                        his , temp = get_hist_data(res[5],res[4],int(timestamp_1))
                        date_df.append(date_Str)
                        max_temp_df.append(max(temp) - 273.5)
                
            df = pd.DataFrame()
            df['Date'] = date_df
            df['Max temp'] = max_temp_df
            st.table(df)
if city_name:
    st.map(pd.DataFrame({'lat' : [res[5]] , 'lon' : [res[4]]},columns=['lat','lon']))
st.header('Road Visibility test against fog')   
uploaded_file = st.file_uploader("upload here")
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
if uploaded_file:
    
  image = Image.open(uploaded_file)
  st.image(image, caption='Uploaded Image.')
  

# Load the model
  model = load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# Replace this with the path to your image

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
  image_array = np.asarray(image)
# Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
# Load the image into the array
  data[0] = normalized_image_array

# run the inference
  prediction = model.predict(data)
  print(prediction)
  if prediction.any()==0:
      
    st.header("Visible")
  else:
      st.header("Nope not visible")
      


