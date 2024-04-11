#######################
# Import libraries
import streamlit as st
import altair as alt
import folium
from streamlit_folium import folium_static
from Adafruit_IO import Client

ADAFRUIT_IO_USERNAME = 'gnerone'
ADAFRUIT_IO_KEY = ''
FEED_NAME = 'gps'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def getGPSValue():
    data = aio.receive(FEED_NAME)
    return (data.value) if data else None

def getItemAmount(itemName):
    amount = -1
    with open('initialValues.txt', 'r') as file:
        file_contents = file.read()
        index = file_contents.find(':', file_contents.find(itemName)) + 2
        amount = int(file_contents[index:file_contents.find(';',index)])
    return amount

def resetAllItems():
    file_contents = ''
    with open('initialValues.txt', 'r') as file:
        file_contents = file.read()
        index = 0
        while(index < len(file_contents)):
            index = file_contents.find(':', index) + 2
            file_contents = file_contents[0:index] + '0' + file_contents[file_contents.find(';', index):len(file_contents)]
            index = file_contents.find(';', index) + 1
    with open('initialValues.txt', 'w') as file:
        file.write(file_contents)
        
def incrementItemAmount(itemName):
    itemAmount = getItemAmount(itemName) + 1
    changeItemValueInFile(itemAmount, itemName)

def decrementItemAmount(itemName):
    itemAmount = getItemAmount(itemName)
    if(itemAmount > 0):
        itemAmount = getItemAmount(itemName) - 1
        changeItemValueInFile(itemAmount, itemName)
    
def changeItemValueInFile(itemAmount, itemName):
    newFileValue = ""
    with open('initialValues.txt', 'r') as file:
        file_contents = file.read()
        index = file_contents.find(':', file_contents.find(itemName)) + 2
        #Still need to add the value
        newFileValue = file_contents[0:index] + str(itemAmount) + file_contents[file_contents.find(';', index):len(file_contents)]
    with open('initialValues.txt', 'w') as file:
        file.write(newFileValue)
        
def currentItemSelected():
    file_contents = ""
    with open('currentItemSelected.txt', 'r') as file:
        file_contents = file.read()
    return file_contents

def getGPSInfo():
    return
        
#######################
# Page configuration
st.set_page_config(
    page_title="Bio-Emergency-Aid-Navigator",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# Sidebar
with st.sidebar:
    st.title('Bio-Emergency-Aid-Navigator')

    drone_list = ['Drone 1']
    current_drone = st.selectbox('Select active drone', drone_list)

#######################
# Dashboard Main Panel

col1 = st.columns((4,6,2), gap='small')
blockCSS = """<div style="background-color: #333333; color: white; border-radius: 5px; padding: 10px;">"""
with col1[0]:
    z_number = 12
    st.markdown('#### Coordinate Location')
    st.markdown("""<div style="background-color: #1AA91A; color: white; border-radius: 5px; padding: 10px;">"""
                f"""<strong>Latitude:</strong> 40°00'45.4"N<br><strong>Longitude:</strong> 83°00'56.5"W<br><strong>Height:</strong> {z_number} meters"""
                """</div>""", unsafe_allow_html=True)
with col1[2]:
    itemsList = ['Bandaids', 'Gauzes', 'Alcohol Wipes', 'Ointment', 'Gloves']
    with open('currentItemSelected.txt', 'w') as file:
        file.write(st.selectbox('Select Item', itemsList))
    if(st.button("Reset Items")):
        resetAllItems()
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        if st.button("+1 Item"):
            incrementItemAmount(currentItemSelected())
    with sub_col2:
        if st.button("-1 Item"):
            decrementItemAmount(currentItemSelected())
with col1[1]:  
    st.markdown('#### Amount of Items')
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.markdown("""<div style="background-color: #0F1CA9; color: white; border-radius: 5px; padding: 10px;">"""
                    f"""<strong> {getItemAmount("Bandaids")}<br><strong>Gauzes:</strong> {getItemAmount("Gauzes")}<br><strong>Alcohol Wipes:</strong> {getItemAmount("Alcohol Wipes")}"""
                    """</div>""", unsafe_allow_html=True)
    with sub_col2:
        st.markdown("""<div style="background-color: #0F1CA9; color: white; border-radius: 5px; padding: 10px;">"""
                    f"""<strong>Ointment:</strong> {getItemAmount("Ointment")}<br><strong>Gloves:</strong> {getItemAmount("Gloves")}"""
                    """</div>""", unsafe_allow_html=True)
        
    
col2 = st.columns((5,5), gap="medium")
with col2[0]:
    cords = getGPSValue().split(',')
    m = folium.Map(location=[cords[0], cords[1]], zoom_start=100)
    folium.Marker(location=[cords[0], cords[1]], popup="San Francisco").add_to(m)
    st.markdown('#### Location Of Drone')
    folium_static(m, width=500, height=400)
with col2[1]:
    st.markdown('#### Live Drone Feed')
    video_url = "https://www.youtube.com/watch?v=6BIURPirIQ8&ab_channel=GoingDownGaming"  # Replace with your YouTube video URL
    st.video(video_url)
