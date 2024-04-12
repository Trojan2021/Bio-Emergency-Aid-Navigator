#######################
# Import libraries
import streamlit as st
import altair as alt
import threading
import time
import random
import folium
from streamlit_folium import folium_static
from Adafruit_IO import Client
from streamlit.runtime.scriptrunner import add_script_run_ctx

ADAFRUIT_IO_USERNAME = 'g_nerone'
ADAFRUIT_IO_KEY = 'API_KEY_HERE'
FEED_NAME = 'gps'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
stopThread = False
# intialValues = {
#     "Bandaids": 0,
#     "Gauzes": 0,
#     "Alcohol Wipes": 0,
#     "Ointment": 0,
#     "Gloves": 0
# }
# currentItem = 'Bandaids'
def initialize_session_state():
    if 'initialValues' not in st.session_state:
        st.session_state.initialValues = {"Bandaids": 0,"Gauzes": 0,"Alcohol Wipes": 0,"Ointment": 0,"Gloves": 0}
    if 'currentItem' not in st.session_state:
        st.session_state.currentItem = "Bandaids"
    if 'currentCord' not in st.session_state:
        st.session_state.currentCord = '$GPGGA,015025.00,0,N,0,W,1,05,2.24,0,M,-33.7,M,,*62'

def nemaToDD(cord, direction):
    ddmm = int(cord)
    dd = int(ddmm / 100)
    mPart = cord - dd * 100
    ddCord = dd + mPart/60 
    if(direction == 'S' or direction == 'W'):
        ddCord *= -1
    return ddCord

def getGPSValue():
    gpsOneLine = ''
    randNum = 0
    data = aio.receive(FEED_NAME)
    gpsOneLine = data.value
    if gpsOneLine.find('$GPGGA') != -1:
        st.session_state.currentCord = gpsOneLine
    randNum = random.randint(1,3)
    if(randNum == 1):
        gpsOneLine = '$GPGGA,015025.00,4000.27294,N,08300.46216,W,1,05,2.24,249.9,M,-33.7,M,,*62'
    elif(randNum == 2):
        gpsOneLine = '$GPGGA,015025.00,4000.27292,N,08300.46216,W,1,05,2.24,10.9,M,-33.7,M,,*62'
    else:
        gpsOneLine = '$GPGGA,015025.00,4000.26080,N,08300.46216,W,1,05,2.24,230.9,M,-33.7,M,,*62'
    #cords = data.value.split(',')
    #cords.append('100.4')
    #return cords if data else [0, 0]
    if(data is not None):
        cords = gpsOneLine[gpsOneLine.find("$GPGGA"):]
        nemaData = cords.split(',')
        lat = nemaToDD(float(nemaData[2]), nemaData[3])
        long = nemaToDD(float(nemaData[4]), nemaData[5])
        height = float(nemaData[9])
    else:
        lat = 0
        long = 0
        height = 0
        
    return (lat,long,height)

def getItemAmount(itemName):
    # amount = -1
    # with open('initialValues.txt', 'r') as file:
    #     file_contents = file.read()
    #     index = file_contents.find(':', file_contents.find(itemName)) + 2
    #     amount = int(file_contents[index:file_contents.find(';',index)]) 
    #st.write(st.session_state)
    return st.session_state.initialValues[itemName]

def resetAllItems():
    # file_contents = ''
    # with open('initialValues.txt', 'r') as file:
    #     file_contents = file.read()
    #     index = 0
    #     while(index < len(file_contents)):
    #         index = file_contents.find(':', index) + 2
    #         file_contents = file_contents[0:index] + '0' + file_contents[file_contents.find(';', index):len(file_contents)]
    #         index = file_contents.find(';', index) + 1
    # with open('initialValues.txt', 'w') as file:
    #     file.write(file_contents)
    for key in st.session_state.initialValues:
        if st.session_state.initialValues[key] != 0:
            st.session_state.initialValues[key] = 0
        
    
       
def incrementItemAmount(itemName):
    itemAmount = getItemAmount(itemName) + 1
    changeItemValueInFile(itemAmount, itemName)

def decrementItemAmount(itemName):
    itemAmount = getItemAmount(itemName)
    if(itemAmount > 0):
        itemAmount = getItemAmount(itemName) - 1
        changeItemValueInFile(itemAmount, itemName)
    
def changeItemValueInFile(itemAmount, itemName):
    # newFileValue = ""
    # with open('initialValues.txt', 'r') as file:
    #     file_contents = file.read()
    #     index = file_contents.find(':', file_contents.find(itemName)) + 2
    #     #Still need to add the value
    #     newFileValue = file_contents[0:index] + str(itemAmount) + file_contents[file_contents.find(';', index):len(file_contents)]
    # with open('initialValues.txt', 'w') as file:
    #     file.write(newFileValue)
    st.session_state.initialValues[itemName] = itemAmount
        
      
def currentItemSelected():
    # file_contents = ""
    # with open('currentItemSelected.txt', 'r') as file:
    #     file_contents = file.read()
    # return file_contents
    return st.session_state.currentItem

def DDCordsToDMSCords(latLong):
    latLong = [float(latLong[0]), float(latLong[1])]
    dmsLatLong = ['','']
    for i in range(2):
        if(i == 0):
            if(latLong[i] > 0):
                cardinal = 'N'
            else:
                cardinal = 'S'
                latLong[i] = -1 * latLong[i]
        elif(i == 1):
            if(latLong[i] > 0):
                cardinal = 'E'
            else:
                cardinal = 'W'
                latLong[i] = -1 * latLong[i]
        d = int(latLong[i])
        temp = (latLong[i] - d) * 60
        m = int(temp)
        s = round((temp - m) * 60, 6)
        dmsLatLong[i] = str(d) + '°' + str(m) + "'" + str(s) + '"' + cardinal
    return dmsLatLong

def displayCords(placeholder1, placeholder2):
    cnt = 0
    stop_event = True
    while(stop_event):
        #time.sleep(5)
        cords = getGPSValue()
        dmsCords = DDCordsToDMSCords([cords[0], cords[1]])
        cnt = cnt + 1
        st.write(f"Test{cnt}")
        placeholder1.markdown('#### Coordinate Location')
        placeholder2.markdown("""<div style="background-color: #1AA91A; color: white; border-radius: 5px; padding: 10px;">"""
                    f"""<strong>Latitude:</strong> {dmsCords[0]}<br><strong>Longitude:</strong> {dmsCords[1]}<br><strong>Height:</strong> {cords[2]} Meters above Sea Level"""
                    """</div>""", unsafe_allow_html=True)
        st.write(stop_event)
        time.sleep(3)
        st.write(stop_event)
        if(cnt == 10):
            stop_event = False
        if(stopThread):
            stop_event = False
            st.write("SOMETHING")
            #del st.session_state.thread1
        st.write(stop_event)
    #st.session_state.thread1.join()
def resetThreading():
    st.session_state.stopThread = False
    del st.session_state.thread1
        
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
initialize_session_state()

col1 = st.columns((4,6,2), gap='small')
blockCSS = """<div style="background-color: #333333; color: white; border-radius: 5px; padding: 10px;">"""
with col1[0]:
    cords = getGPSValue()
    dmsCords = DDCordsToDMSCords([cords[0], cords[1]])
    st.markdown('#### Coordinate Location')
    st.markdown("""<div style="background-color: #1AA91A; color: white; border-radius: 5px; padding: 10px;">"""
                f"""<strong>Latitude:</strong> {dmsCords[0]}<br><strong>Longitude:</strong> {dmsCords[1]}<br><strong>Height:</strong> {cords[2]} Meters above Sea Level"""
                """</div>""", unsafe_allow_html=True)
    # placeholder1 = st.empty()
    # placeholder2 = st.empty()
    # stopThread = False
    # st.write("TESTING")
    # thread1 = threading.Thread(target=displayCords, args=(placeholder1,placeholder2))
    # add_script_run_ctx(thread1)
    # thread1.start()
with col1[2]:
    itemsList = ['Bandaids', 'Gauzes', 'Alcohol Wipes', 'Ointment', 'Gloves']
    # with open('currentItemSelected.txt', 'w') as file:
    #     file.write(st.selectbox('Select Item', itemsList))
    st.session_state.currentItem = st.selectbox('Select Item', itemsList)
    # st.markdown(word)
    # ItemAmounts.updateCurrentItem(str(word))
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        if st.button("+1 Item"):
            # stopThread = True
            incrementItemAmount(currentItemSelected())
    with sub_col2:
        if st.button("-1 Item"):
            # stopThread = True
            decrementItemAmount(currentItemSelected())
    sub_col = st.columns((1,5,1), gap="small")
    with sub_col[1]:
        if(st.button("Reset Items")):
            # stopThread = True
            resetAllItems()
with col1[1]:  
    st.markdown('#### Amount of Items')
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.markdown("""<div style="background-color: #0F1CA9; color: white; border-radius: 5px; padding: 10px;">"""
                    f"""<strong>Bandaids:</strong> {getItemAmount("Bandaids")}<br><strong>Gauzes:</strong> {getItemAmount("Gauzes")}<br><strong>Alcohol Wipes:</strong> {getItemAmount("Alcohol Wipes")}"""
                    """</div>""", unsafe_allow_html=True)
    with sub_col2:
        st.markdown("""<div style="background-color: #0F1CA9; color: white; border-radius: 5px; padding: 10px;">"""
                    f"""<strong>Ointment:</strong> {getItemAmount("Ointment")}<br><strong>Gloves:</strong> {getItemAmount("Gloves")}"""
                    """</div>""", unsafe_allow_html=True)
        
    
col2 = st.columns((5,5), gap="medium")
with col2[0]:
    st.markdown('#### Location Of Drone')
    # if 'map' not in st.session_state:
    st.session_state.map = folium.Map(location=[float(cords[0]), float(cords[1])], zoom_start=17)
    st.session_state.marker = folium.Marker(location=[float(cords[0]), float(cords[1])], popup="Drone 1 Location").add_to(st.session_state.map)
    # st.session_state.mapCounter = 0
    # else:
    #     st.session_state.mapCounter = st.session_state.mapCounter + 1           
        
    # if 'marker' not in st.session_state:
    #     st.session_state.marker = folium.Marker(location=[float(cords[0]), float(cords[1])], popup="Drone 1 Location").add_to(st.session_state.map)
    # else:
    #     st.session_state.marker.remove(st.session_state.map)
    #     st.session_state.marker = folium.Marker(location=[float(cords[0]), float(cords[1])], popup="Drone 1 Location").add_to(st.session_state.map)
    #st.session_state.marker = folium.Marker(location=[float(cords[0]), float(cords[1])], popup="Drone 1 Location").add_to(st.session_state.map)
    
    folium_static(st.session_state.map, width=500, height=400)
    # if st.session_state.mapCounter >= 10:
    #     del st.session_state.map
with col2[1]:
    st.markdown('#### Live Drone Feed')
    video_url = "https://www.youtube.com/watch?v=6BIURPirIQ8&ab_channel=GoingDownGaming"  # Replace with your YouTube video URL
    st.video(video_url)
# if(not stopThread): 
#     thread1.join()
# else:
#     del st.session_state.stopThread
#     del st.session_state.thread1
# startTime = time.time()
# endTime = startTime
# while(endTime - startTime >= 10):
#     endTime = time.time()
#     st.write(time.time())
# for key in st.session_state.keys():
#     del st.session_state[key]
time.sleep(5)
st.rerun()
    
