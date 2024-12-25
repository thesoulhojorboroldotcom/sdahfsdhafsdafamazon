import streamlit as st
import requests
import json
from io import BytesIO
from PIL import Image





# Set the title of the app
st.set_page_config(page_title="The BattleGround")

################## Menu Hide #################
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>

            """
st.markdown(hide_st_style, unsafe_allow_html=True)

########## END #############

# Define the API endpoint URL (replace with your actual API URL)

url = "https://idp.federate.amazon.com/api/oauth2/v2/token"

payload = 'refresh_token=5dc3a908-f6dc-44fa-961c-f48bffa9efa9&grant_type=refresh_token&client_id=atoz.mobile.pkce.prod'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'Content-Length': '107',
  'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; ONEPLUS A6003 Build/RKQ1.201217.002)',
  'Host': 'idp.federate.amazon.com',
  'Connection': 'Keep-Alive',
  'Accept-Encoding': 'gzip'
}

response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)

token = json.loads(response.text)
access_token = token['access_token']
# print(access_token)



def get_data_from_api(name):
    url = "https://atoz-api.amazon.work/graphql?employeeId=201763573"

    payload = json.dumps({
      "query": "query getRelevancy{getRelevancy(employeeId:\"201763573\",searchText:\""+name+"\",searchType:MIXED){circleMembers{employeeId employeeName matchType type alias}}}"
    })
    headers = {
      'Host': 'atoz-api.amazon.work',
      'cookie': 'atoz-mobile-features=mobile_bottom_nav_v3; mobile_hq_homepage_v3=; atoz-mobile-app-info=EmployeeSelfServiceMobile/4.0.55677.0/20556772/4.0.548 Android/11 prod; atoz-oauth-token='+access_token+'',
      'x-atoz-client-id': 'ATOZ_MYCIRCLE_RELEVANCY_SEARCH',
      'content-type': 'application/json',
      'accept-encoding': 'gzip',
      'user-agent': 'okhttp/4.9.1'
    }
    with st.spinner("Fetching data from Server..........."):
      response = requests.request("POST", url, headers=headers, data=payload)

      # print(response.text)
      return response.text


def showPhoto(employeeId,employeeName):
      url = "https://atoz-badge-photo.amazon.work/"+employeeId+""

      payload = {}
      headers = {
        'Host': 'atoz-badge-photo.amazon.work',
        'accept-encoding': 'gzip',
        'cookie': 'atoz-mobile-features=mobile_bottom_nav_v3; mobile_hq_homepage_v3=; atoz-mobile-app-info=EmployeeSelfServiceMobile/4.0.55677.0/20556772/4.0.548 Android/11 prod; atoz-oauth-token='+access_token+'',
        'user-agent': 'okhttp/4.9.1'
      }

      response = requests.request("GET", url, headers=headers, data=payload)

      img = Image.open(BytesIO(response.content))
      st.image(img, caption=employeeName, use_container_width =False)

# Display a header
st.header("The System")

# Get user input
name = st.text_input("Enter Login ID or Name: ")

# Button to trigger API call
if st.button("Search"):
  # Call the API and get data
  data = get_data_from_api(name)
  data = json.loads(data)

  if data:
      circle_members = data['data']['getRelevancy']['circleMembers']
      for member in circle_members:
          showPhoto(member['employeeId'],member['employeeName'])
      

st.stop()
