import streamlit as st
from nav import navigation
import requests
import pandas as pd
import json

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

INELIGIBILITIES_PATH = './data/tax_abatement/ineligibilities.json'

census_url = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"
parcel_url = "https://gis.dupageco.org/arcgis/rest/services/ParcelSearch/DuPageAssessmentParcelViewer/MapServer/4/query"

dha_non_eligible_census = json.load(open(INELIGIBILITIES_PATH))['dha_non_eligible_census']
dha_non_eligible_township = json.load(open(INELIGIBILITIES_PATH))['dha_non_eligible_township']
dha_non_eligible_parcels = json.load(open(INELIGIBILITIES_PATH))['dha_non_eligible_parcels']

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
    
    if not isinstance(unit_count, int) and not isinstance(eligible_units, int) :
        print(type(unit_count))
        st.warning("Please Enter Numeric Values for Unit Count and Eligible Units")
        return
        
    
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
    
    if not isinstance(unit_count, int) and not isinstance(eligible_units, int) :
        print(type(unit_count))
        st.warning("Please Enter Numeric Values for Unit Count and Eligible Units")
        return
        
    
    if eligible:
        st.success(":material/award_star: **Application is Eligible**")

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
        st.markdown(f"""
        **Total Units:** {str(unit_count)}  
        **Eligible Units:** {str(eligible_units)}  
        **Unit Ratio:** {(int(eligible_units)/int(unit_count))*100:.2f}%  
        """)
        st.divider()
        
        st.markdown("""
        ### :material/done_outline: **Other Eligibility Checks**

        """)

        st.markdown(f"""
        **Census Tract:** {census_tract_check(census_tract)}  
        **Township:** {township_check(township)}  
        **Parcel Number:** {parcel_check(parcel_number)}  
        **Street Address Match:** {street_check(street_name, parcel_number, parcel_address)}
        """)
        st.divider()

        st.success("UNIT & ADDRESS DETAILS".center(90))
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
        st.error(":material/report: APPLICATION NOT ELIGIBLE".center(90))

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
        st.markdown(f"""
        **Total Units:** {str(unit_count)}  
        **Eligible Units:** {str(eligible_units)}  
        **Unit Ratio:** {(int(eligible_units)/int(unit_count))*100:.2f}%  
        """)
        st.divider()
        
        st.markdown("""
        ### :material/done_outline: **Other Eligibility Checks**

        """)

        st.markdown(f"""
        **Census Tract:** {census_tract_check(census_tract)}  
        **Township:** {township_check(township)}  
        **Parcel Number:** {parcel_check(parcel_number)}  
        **Street Address Match:** {street_check(street_name, parcel_number, parcel_address)}
        """)
        st.divider()

st.header("Tax Abatement")
    
left_col1, right_col2, = st.columns([1.5, 5])

with left_col1:
    township = st.text_input("Township")
    census_tract = st.text_input("Census Tract")
    parcel_number = st.text_input("Parcel Index Number")
    tenant_name = st.text_input("Tenant Name")
    applicant = st.text_input("Applicant Name")
    street_name = st.text_input("Street Name")
    col1, col2, col3 = st.columns([0.6,0.4,0.5])
    with col1:
        city_name = st.text_input("City Name")
    with col2:
        state_name = st.text_input("State Name", "IL", disabled = True)
    with col3:
        zip_code = st.text_input("Zip Code")
    col1, col2 = st.columns(2)
    with col1:
        unit_count = st.number_input("Unit Count", min_value = 0, value = 0)
    with col2:
        eligible_units = st.number_input("Eligible Units", min_value = 0, value = 0)
    submit = st.button("Run Application Check")

#Applicant Full Address
address = f'{street_name} {city_name} {state_name} {zip_code}'

with right_col2:
    if submit:
        check_application(township, census_tract, parcel_number, tenant_name, applicant)