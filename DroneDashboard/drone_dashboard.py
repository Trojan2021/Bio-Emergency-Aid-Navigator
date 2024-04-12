#######################
# Import libraries
import streamlit as st
import altair as alt
import folium
from streamlit_folium import folium_static
from Adafruit_IO import Client

ADAFRUIT_IO_USERNAME = 'g_nerone'
ADAFRUIT_IO_KEY = ''
FEED_NAME = 'gps'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def nemaToDD(cord, direction):
    ddmm = int(cord)
    dd = int(ddmm / 100)
    mPart = cord - dd * 100
    ddCord = dd + mPart/60 
    if(direction == 'S' or direction == 'W'):
        ddCord *= -1
    return ddCord

def getGPSValue():
    data = aio.receive(FEED_NAME)
    #cords = data.value.split(',')
    #cords.append('100.4')
    #return cords if data else [0, 0]
    if(data is not None):
        cords = data.value[data.value.find("$GPGGA"):]
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

@st.cache_data 
def createMap(lat, long):
    return folium.Map(location=[float(lat), float(long)], zoom_start=100)
        
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
    cords = getGPSValue()
    dmsCords = DDCordsToDMSCords([cords[0], cords[1]])
    st.markdown('#### Coordinate Location')
    st.markdown("""<div style="background-color: #1AA91A; color: white; border-radius: 5px; padding: 10px;">"""
                f"""<strong>Latitude:</strong> {dmsCords[0]}<br><strong>Longitude:</strong> {dmsCords[1]}<br><strong>Height:</strong> {cords[2]} Meters above Sea Level"""
                """</div>""", unsafe_allow_html=True)
with col1[2]:
    itemsList = ['Bandaids', 'Gauzes', 'Alcohol Wipes', 'Ointment', 'Gloves']
    with open('currentItemSelected.txt', 'w') as file:
        file.write(st.selectbox('Select Item', itemsList))
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        if st.button("+1 Item"):
            incrementItemAmount(currentItemSelected())
    with sub_col2:
        if st.button("-1 Item"):
            decrementItemAmount(currentItemSelected())
    sub_col = st.columns((1,5,1), gap="small")
    with sub_col[1]:
        if(st.button("Reset Items")):
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
    cords = getGPSValue()       
    m = createMap(cords[0], cords[1])
    folium.Marker(location=[float(cords[0]), float(cords[1])], popup="Drone 1 Location").add_to(m)
    st.markdown('#### Location Of Drone')
    folium_static(m, width=500, height=400)
with col2[1]:
    st.markdown('#### Live Drone Feed')
    video_url = "https://www.youtube.com/watch?v=6BIURPirIQ8&ab_channel=GoingDownGaming"  # Replace with your YouTube video URL
    st.video(video_url)
