import streamlit as st
from nav import navigation
import requests
import pandas as pd

#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")
    

#Page Config
st.set_page_config(
    layout = "wide",
    page_title="PIC Fatal Error Dashboard",
    page_icon = "./assets/favi.ico",
)

# Navigation Bar
with st.sidebar:
    navigation()

census_url = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"
parcel_url = "https://gis.dupageco.org/arcgis/rest/services/ParcelSearch/DuPageAssessmentParcelViewer/MapServer/4/query"

def fetch_api_data(url, params, fields):
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        result = {}
        for key, path in fields.items():
            value = data
            for step in path:
                value = value[step]
            result[key] = value
        return result, None
    except (KeyError, IndexError, TypeError):
        return None, f"No data found for {'Parcel Index Number' if 'parcel_owner' in fields else 'Applicant Address'}" 
    except Exception as e:
        return None, str(e)
   
def census_tract_check(census_tract):
    if census_tract not in dha_non_eligible_census:
        return f'Census Tract {census_tract} does not exist in the list of ineligible census tracts.'
    else:
        return f'Census Tract {census_tract} exists in the list of ineligible census tracts.'   


def township_check(township):
    if township not in dha_non_eligible_township:
        return f'Township {township} does not exist in the list of ineligible townships.'
    else:
        return f'Township {township} exists in the list of ineligible townships.'
    
    
def parcel_check(parcel_number):
    if parcel_number not in dha_non_eligible_parcels:
        return f'Parcel Index Number {parcel_number} does not exist in the list of ineligible Parcel Index Numbers.'
    else:
        return f'Parcel Index Number {parcel_number} exists in the list of Parcel Index Numbers.'
    

def street_check(street_name, parcel_number, parcel_address):
    if street_name.lower() in parcel_address.lower():
        return f'Street Address {street_name} Exists Under Parcel Index Number {parcel_number}'
    else:
        return f'Street Address {street_name} Does Not Exists Under Parcel Index Number {parcel_number}'
    

def check_application(township, census_tract, parcel_number, tenant_name, applicant):
    
    census_data = fetch_api_data(
        census_url,
        {
        "address": address,
        "benchmark": "4",
        "vintage": 4,
        "format": "json",
        },
        {
        "township_data": [
            'result', 'addressMatches', 0,
            'geographies', 'County Subdivisions', 0, 'NAME'
        ],
        "census_data": [
            "result", "addressMatches", 0,
            "geographies", "Census Tracts", 0, "NAME"
        ],
    }
    )
    
    parcel_data = fetch_api_data(
        parcel_url,
        {
            "where": f"PIN = '{parcel_number}'", 
            "outFields": "BILLNAME, PROPSTNAME", 
            "returnGeometry": "false", 
            "f": "json"
        },
        {
        "parcel_owner": [
            "features", 0 ,"attributes","BILLNAME"
        ],
        "parcel_address": [
            "features", 0 ,"attributes","PROPSTNAME"
        ],
    }
    )

    if parcel_data[1] or census_data[1]:
        warning_message = parcel_data[1] if parcel_data[1] else census_data[1]
        st.warning(f'Error fetching data: {warning_message}')
        return

    print(f'data: {parcel_data}, {census_data}')
    
    parcel_owner = parcel_data[0]['parcel_owner']
    parcel_address = parcel_data[0]['parcel_address']
    township_data = census_data[0]['township_data']
    census_data = census_data[0]['census_data']
    
    eligible = True
    
    if township in dha_non_eligible_township:
        eligible = False
    if census_tract in dha_non_eligible_census:
        eligible = False
    if township.lower() not in township_data.lower():
        eligible = False
    if census_tract.lower() not in census_data.lower():
        eligible = False
    if parcel_number in dha_non_eligible_parcels:
        eligible = False
    if street_name.lower() not in parcel_address.lower():
        eligible = False
    if int(unit_count) > 2 and (int(eligible_units)/int(unit_count) > 0.2):
        eligible = False
    
    if eligible:
        st.write("✅ APPLICATION IS ELIGIBLE")

        table_compare = {
            "Application": [
                township,
                census_tract,
                street_name,
                applicant,
            ],
            "API Checks":[
                township_data,
                census_data,
                parcel_address,
                parcel_owner
            ]
        }
        st.table(table_compare)
        st.write("Total Units:".ljust(30) + str(unit_count).ljust(30) + "| Eligible Units: " + str(eligible_units))
        st.write("Unit Ratio:".ljust(30) + f"{(int(eligible_units)/int(unit_count))*100:.2f}%")
        
        st.write("✅ OTHER CHECKS".center(90))
        
        st.write(census_tract_check(census_tract))
        st.write(township_check(township))
        st.write(parcel_check(parcel_number))
        st.write(street_check(street_name, parcel_number, parcel_address))

        st.write("UNIT & ADDRESS DETAILS".center(90))
        df = pd.DataFrame({
            "PIN": [parcel_number],
            "Unit Count": [unit_count],
            "Eligible Units": [eligible_units],
            "% Qualify": [f'{(int(eligible_units)/int(unit_count))*100:.2f}%'],
            "Street Address": [street_name],
            "City": [city_name],
            "State": [state_name],
            "Zip Code": [zip_code],
            "Tenant Name": [tenant_name]
        })
        st.table(df)
        return
    else:
        st.write("❌ APPLICATION NOT ELIGIBLE".center(90))

        table_compare = {
            "Application": [
                township,
                census_tract,
                street_name,
                applicant,
            ],
            "API Checks":[
                township_data,
                census_data,
                parcel_address,
                parcel_owner
            ]
        }
        st.table(table_compare)
        st.write("Total Units:".ljust(30) + str(unit_count).ljust(30) + "| Eligible Units: " + str(eligible_units))
        st.write("Unit Ratio:".ljust(30) + f"{(int(eligible_units)/int(unit_count))*100:.2f}%")
        
        st.write("✅ OTHER CHECKS".center(90))
        
        st.write(census_tract_check(census_tract))
        st.write(township_check(township))
        st.write(parcel_check(parcel_number))
        st.write(street_check(street_name, parcel_number))

dha_non_eligible_township = {
    "Wayne": False, 
    "Bloomingdale": False,
    "Winfield": False
}  

dha_non_eligible_census = {
    "8401.04": False, 
    "8403.03": False, 
    "8407.04": False, 
    "8408.02": False, 
    "8409.04": False, 
    "8411.02": False, 
    "8411.08": False, 
    "8412.08": False,
    "8412.1": False, 
    "8413.12": False, 
    "8413.13": False, 
    "8415.03": False,
    "8416.03": False, 
    "8416.04": False, 
    "8416.05": False, 
    "8416.07": False,
    "8417.05": False, 
    "8417.06": False, 
    "8417.08": False, 
    "8426.04": False,
    "8427.1": False, 
    "8436.01": False, 
    "8443.06": False, 
    "8443.08": False,
    "8443.09": False, 
    "8444.02": False, 
    "8449.02": False, 
    "8450": False,
    "8455.06": False, 
    "8458.03": False, 
    "8459.02": False, 
    "8461.02": False,
    "8463.12": False, 
    "8464.1": False, 
    "8465.04": False, 
    "8465.13": False,
    "8465.15": False, 
    "8466.03": False, 
    "8467.01": False 
}

dha_non_eligible_parcels = {
    "0309306018": False,
    "0315107011": False,
    "0315107024": False,
    "0316107016": False,
    "0316115001": False,
    "0316115003": False,
    "0316115015": False,
    "0316115020": False,
    "0318300002": False,
    "0320214004": False,
    "0320418008": False,
    "0325108010": False,
    "0325108025": False,
    "0328423008": False,
    "0329201004": False,
    "0335300047": False,
    "0335321011": False,
    "0336308018": False,
    "0502200017": False,
    "0503208006": False,
    "0503210017": False,
    "0510410035": False,
    "0511414006": False,
    "0514306017": False,
    "0514306018": False,
    "0514307078": False,
    "0517417060": False,
    "0520116006": False,
    "0522204016": False,
    "0522204020": False,
    "0523104020": False,
    "0527106119": False,
    "0527106131": False,
    "0603121005": False,
    "0603123007": False,
    "0603128003": False,
    "0603211011": False,
    "0603304001": False,
    "0604109010": False,
    "0604236021": False,
    "0605201138": False,
    "0606300028": False,
    "0606307005": False,
    "0607206033": False,
    "0608103005": False,
    "0608104004": False,
    "0608121009": False,
    "0610221011": False,
    "0611418022": False,
    "0612328014": False,
    "0613300022": False,
    "0617107014": False,
    "0619203065": False,
    "0621212115": False,
    "0621214098": False,
    "0629107038": False,
    "0702107005": False,
    "0704305030": False,
    "0704305063": False,
    "0704305069": False,
    "0709207012": False,
    "0709220069": False,
    "0710213016": False,
    "0710213034": False,
    "0710213097": False,
    "0710213163": False,
    "0710213284": False,
    "0710301034": False,
    "0710302032": False,
    "0710303040": False,
    "0710311172": False,
    "0710311211": False,
    "0711409025": False,
    "0711409064": False,
    "0713101014": False,
    "0713106005": False,
    "0713404012": False,
    "0714201012": False,
    "0714317009": False,
    "0714317010": False,
    "0715211035": False,
    "0716200030": False,
    "0716200031": False,
    "0716205004": False,
    "0719316135": False,
    "0722311102": False,
    "0723114072": False,
    "0725400035": False,
    "0725400043": False,
    "0725400044": False,
    "0725400047": False,
    "0725405035": False,
    "0725405038": False,
    "0725405050": False,
    "0726111091": False,
    "0726112037": False,
    "0728308087": False,
    "0729208055": False,
    "0729216156": False,
    "0731201039": False,
    "0731309012": False,
    "0732110040": False,
    "0732110056": False,
    "0732110072": False,
    "0732114044": False,
    "0732302077": False,
    "0732302084": False,
    "0732417057": False,
    "0803406020": False,
    "0808404006": False,
    "0809106008": False,
    "0809203004": False,
    "0814215034": False,
    "0816103038": False,
    "0817105013": False,
    "0817106050": False,
    "0817106054": False,
    "0817106055": False,
    "0817402012": False,
    "0817404016": False,
    "0828402079": False,
    "0828411032": False,
    "0828412028": False,
    "0829201013": False,
    "0829309041": False,
    "0832108010": False,
    "0832110003": False,
    "0832110049": False,
    "0832110083": False,
    "0832110085": False,
    "0832110086": False,
    "0832110102": False,
    "0832110179": False,
    "0832110182": False,
    "0832110200": False,
    "0832110206": False,
    "0832110216": False,
    "0832110218": False,
    "0832111013": False,
    "0832111102": False,
    "0832117016": False,
    "0835304032": False,
    "0836101030": False,
    "0836316041": False,
    "0903403006": False,
    "0905415015": False,
    "0908307005": False,
    "0908411042": False,
    "0909428025": False,
    "0910102002": False,
    "0910312035": False,
    "0911416006": False,
    "0914122104": False,
    "0915105009": False,
    "0916305008": False,
    "0916305015": False,
    "0916305020": False,
    "0916307005": False,
    "0919111109": False,
    "0919201031": False,
    "0920113003": False,
    "0921308004": False,
    "0929104018": False,
    "0929203001": False,
    "0929215060": False,
    "0929215075": False,
    "0929218039": False,
    "0929220012": False,
    "0929220106": False,
    "0929220115": False,
    "0930301022": False,
    "0934108019": False,
    "0935114001": False,
    "0935114116": False,
    "0935114117": False,
    "0935114148": False,
    "0935114180": False,
    "0935114196": False,
    "0935114204": False,
    "0935114227": False,
    "0935114229": False,
    "0935114349": False,
    "0935114361": False,
    "0935114364": False,
    "0935114389": False,
    "0719312068": False,
    "0720314009": False,
    "0726111056": False,
    "0823401106": False,
    "0832110073": False
}

st.header("Tax Abatement")
    
col1, col2, = st.columns([1.5, 5])

with col1:
    township = st.text_input("Township", width = 400)
    census_tract = st.text_input("Census Tract", width = 400)
    parcel_number = st.text_input("Parcel Index Number", width = 400)
    tenant_name = st.text_input("Tenant Name", width = 400)
    applicant = st.text_input("Applicant Name", width = 400)
    street_name = st.text_input("Street Name", width = 400)
    city_name = st.text_input("City Name", width = 400)
    state_name = st.text_input("State Name", "IL", width = 400, disabled = True)
    zip_code = st.text_input("Zip Code", width = 400)
    unit_count = st.text_input("Unit Count", width = 400)
    eligible_units = st.text_input("Eligible Units", width = 400)
    submit = st.button("Run Application Check")

#Applicant Full Address
address = f'{street_name} {city_name} {state_name} {zip_code}'

with col2:
    if submit:
        check_application(township, census_tract, parcel_number, tenant_name, applicant)








