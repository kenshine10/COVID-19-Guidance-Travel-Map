from os import name
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
from ipyleaflet.leaflet import ZoomControl
from pandas.core import indexing
from pandas.core.indexes.base import Index
from pandas.io.formats.style_render import Tooltips
import streamlit as st
from streamlit.elements.map import _ZOOM_LEVELS
from streamlit_folium import folium_static
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import folium
import datetime
from folium.plugins import Fullscreen
import folium.features
from datetime import date, datetime
import pytz
from datetime import datetime
import leafmap.foliumap as leafmap
import branca
import branca.colormap as cm
from branca.colormap import linear

MAGE_EMOJI_URL = "https://cdn-icons-png.flaticon.com/512/2913/2913584.png"
plane_icon = "https://cdn-icons-png.flaticon.com/512/476/476505.png"

st.set_page_config(
    page_title="COVID-19 Travel Map",
    page_icon=MAGE_EMOJI_URL,
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
    """
            <style>
            .header-style {
                font-size:25px;
            }
            </style>
            """,
    unsafe_allow_html=True
)
st.markdown(
    """
            <style>
            .font-style {
                font-size:20px;
            }
            </style>
            """,
    unsafe_allow_html=True
)
st.markdown(
    """
            <style>
            .font-allow {
                font-size:50px;
                color:#a6d96a;
            }
            </style>
            """,
    unsafe_allow_html=True
)
st.markdown(
    """
            <style>
            .font-restrict {
                font-size:50px;
                color:#fdae61;
            }
            </style>
            """,
    unsafe_allow_html=True
)
st.markdown(
    """
            <style>
            .font-close {
                font-size:50px;
                color:#d7191c;
            }
            </style>
            """,
    unsafe_allow_html=True
)
st.markdown(
    """
            <style>
            .font-unknown {
                font-size:50px;
                color:grey;
            }
            </style>
            """,
    unsafe_allow_html=True
)

st.title("Welcome to COVID-19 Guidance Travel Map")
st.subheader("This is an interactive map for travelers guidance")
st.markdown('***')
MAGE_EMOJI_URL = 'sidebae icon.png'
st.sidebar.image(MAGE_EMOJI_URL)


# Country list
countries_and_codes = [
    ['Afghanistan', 'AF'], ['Albania', 'AL'], [
        'Algeria', 'DZ'], ['Andorra', 'AD'], ['Angola', 'AO'],
    ['Åland Islands', 'ALA'], ['Antigua and Barbuda', 'AG'], ['Anguilla', 'AIA'], ['American Samoa', 'ASM'], ['Argentina', 'AR'], ['Aruba', 'ABW'], [
        'Armenia', 'AM'], ['Australia', 'AU'], ['Austria', 'AT'],
    ['Azerbaijan', 'AZ'], ['The Bahamas', 'BHS'], ['Bahrain', 'BH'], [
        'Bangladesh', 'BD'], ['Barbados', 'BB'],
    ['Belarus', 'BY'], ['Belgium', 'BE'], ['Belize', 'BZ'], [
        'Benin', 'BJ'], ['Bhutan', 'BT'], ['Bolivia', 'BO'],
    ['Bosnia and Herzegovina', 'BA'], ['Botswana', 'BW'], [
        'Brazil', 'BR'], ['Brunei', 'BN'], ['Bulgaria', 'BG'],
    ['Burkina Faso', 'BF'], ['Burma', 'MM'], ['Burundi', 'BI'], [
        'Cabo Verde', 'CV'], ['Cambodia', 'KH'],
    ['Cameroon', 'CM'], ['Canada', 'CA'], ['Cape Verde', 'CPV'], [
        'Central African Republic', 'CF'], ['Chad', 'TD'], ['Chile', 'CL'],
    ['China', 'CN'], ['Colombia', 'CO'], ['Republic of the Congo', 'CG'], [
        'Congo (Kinshasa)', 'CD'],
    ['Costa Rica', 'CR'], ["Cote d'Ivoire", 'CI'], [
        'Croatia', 'HR'], ['Cuba', 'CU'], ['Cyprus', 'CY'],
    ['Czechia', 'CZ'], ['Denmark', 'DK'], [
        'Djibouti', 'DJ'], ['Dominica', 'DM'],
    ['Dominican Republic', 'DO'], ['Ecuador', 'EC'], [
        'Egypt', 'EG'], ['El Salvador', 'SV'],
    ['Equatorial Guinea', 'GQ'], ['Eritrea', 'ER'], [
        'Estonia', 'EE'], ['Ethiopia', 'ET'],
    ['Fiji', 'FJ'], ['Finland', 'FI'], ['France', 'FR'], [
        'Gabon', 'GA'], ['The Gambia', 'GM'], ['Georgia', 'GE'],
    ['Germany', 'DE'], ['Ghana', 'GH'], ['Greece', 'GR'], [
        'Grenada', 'GD'], ['Guatemala', 'GT'], ['Guinea', 'GN'],
    ['Guinea-Bissau', 'GW'], ['Guyana', 'GY'], ['Haiti',
                                                'HT'], ['Hong Konge', 'HKG'], ['Honduras', 'HN'],
    ['Hungary', 'HU'], ['Iceland', 'IS'], ['India', 'IN'], [
        'Indonesia', 'ID'], ['Iran', 'IR'], ['Iraq', 'IQ'],
    ['Ireland', 'IE'], ['Jersey', 'JE'], ['Italy', 'IT'], [
        'Jamaica', 'JM'], ['Japan', 'JP'], ['Jordan', 'JO'],
    ['Kazakhstan', 'KZ'], ['Kenya', 'KE'], [
        'Korea, South', 'KR'], ['Kosovo', 'XK'], ['Kuwait', 'KW'],
    ['Kyrgyzstan', 'KG'], ['Laos', 'LA'], ['Latvia', 'LV'], [
        'Lebanon', 'LB'], ['Liberia', 'LR'], ['Libya', 'LY'],
    ['Lesotho', 'LSO'], ['Lithuania', 'LT'], [
        'Luxembourg', 'LU'], ['Macedonia', 'MAC'], ['Madagascar', 'MG'],
    ['Malawi', 'MW'], ['Malaysia', 'MY'], ['Maldives', 'MV'], [
        'Mali', 'ML'], ['Malta', 'MT'], ['Mauritania', 'MR'],
    ['Mauritius', 'MU'], ['Mexico', 'MX'], ['Moldova', 'MD'], [
        'Monaco', 'MC'], ['Mongolia', 'MN'], ['Montenegro', 'ME'],
    ['Morocco', 'MA'], ['Mozambique', 'MZ'], ['Namibia', 'NA'], [
        'Nepal', 'NP'], ['Netherlands', 'NL'], ['New Zealand', 'NZ'],
    ['Nicaragua', 'NI'], ['Niger', 'NE'], ['Nigeria', 'NG'], [
        'Palestine', 'PSE'], ['Norway', 'NO'], ['Oman', 'OM'],
    ['Pakistan', 'PK'], ['Panama', 'PA'], ['Papua New Guinea', 'PG'], [
        'Paraguay', 'PY'], ['Peru', 'PE'], ['Philippines', 'PH'],
    ['Poland', 'PL'], ['Portugal', 'PT'], ['Qatar', 'QA'], [
        'Romania', 'RO'], ['Russia', 'RU'], ['Rwanda', 'RW'],
    ['Saint Kitts and Nevis', 'KN'], ['Saint Lucia', 'LC'], [
        'Saint Vincent and the Grenadines', 'VC'], ['San Marino', 'SM'],
    ['Saudi Arabia', 'SA'], ['Senegal', 'SN'], ['Serbia', 'RS'], [
        'Seychelles', 'SC'], ['Sierra Leone', 'SL'],
    ['Singapore', 'SG'], ['Slovakia', 'SK'], ['Slovenia', 'SI'], [
        'Somalia', 'SO'], ['South Africa', 'ZA'], ['Spain', 'ES'],
    ['Sri Lanka', 'LK'], ['Sudan', 'SD'], ['Suriname', 'SR'], [
        'Sweden', 'SE'], ['Switzerland', 'CH'], ['Syria', 'SY'],
    ['Taiwan', 'TW'], ['Tanzania', 'TZ'], ['Thailand',
                                           'TH'], ['Turkmenistan', 'TKM'], ['Togo', 'TG'],
    ['Tuvalu', 'TUV'], ['Tunisia', 'TN'], ['Turkey', 'TR'], [
        'United States of America', 'US'], ['Uganda', 'UG'], ['Ukraine', 'UA'],
    ['United Arab Emirates', 'AE'], ['United Kingdom', 'GB'], [
        'Uruguay', 'UY'], ['Uzbekistan', 'UZ'], ['Venezuela', 'VE'],
    ['Vietnam', 'VN'], ['Yemen', 'YEM'], ['Zambia', 'ZM'], ['Zimbabwe', 'ZW']]

################## Get Data ##########################

country_geo = f'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'

#country_geo2 = pd.read_csv("world-administrative-boundaries.xls.csv")

travel_dataset_country = pd.read_csv("CovidProject.csv")
travel_dataset = pd.read_csv("countries_data_last.csv")

Vaccination_data = pd.read_csv("vaccination-data.csv")

Covid_cases_url = f'https://covid19.who.int/WHO-COVID-19-global-table-data.csv'

Covid_cases_df = pd.read_csv(Covid_cases_url, index_col=False) 


st.sidebar.header("Travel Profile:")
travel_profile = st.sidebar.radio(
    "Select Travelling Profile:",
    ('Tourism', 'Education', 'Medical'))

mf = folium.Map(location=[42, 0],
                zoom_start=2.1, tiles='OpenStreetMap', name = "Light mode")

if travel_profile == 'Tourism':
    selectData_tourism = st.sidebar.multiselect("Select preferred Infromation to be present in the map:", [
                                                "Shops", "Public Transport", "Public Events", "Internal Movements"])

    if 'Shops' in selectData_tourism:
        shops_map = folium.Choropleth(geo_data=country_geo, name="Shops", data=travel_dataset, columns=["id", "SC"], nan_fill_color="grey", nan_fill_opacity=0.5, key_on="feature.id", bins=[
            0, 1, 2, 3, 4], fill_color='RdYlGn', fill_opacity=0.8, line_opacity=0.5, line_weight=1.5, line_color='black', range_color=[0, 2], highlight=True, ).add_to(mf)
    if 'Public Transport' in selectData_tourism:
        transport_map = folium.Choropleth(geo_data=country_geo, name="Public Transport", data=travel_dataset, columns=["id", "TC"], nan_fill_color="grey", nan_fill_opacity=0.5, key_on="feature.id", bins=[
            0, 1, 2, 3, 4], fill_color='RdYlGn', fill_opacity=0.8, line_opacity=0.5, line_weight=1.5, line_color='black', range_color=[0, 2], highlight=True,).add_to(mf)

    if 'Public Events' in selectData_tourism:
        events_map = folium.Choropleth(geo_data=country_geo, name="Public Events", data=travel_dataset, columns=["id", "PEC"], nan_fill_color="grey", nan_fill_opacity=0.5, key_on="feature.id", bins=[
            0, 1, 2, 3, 4], fill_color='RdYlGn', fill_opacity=0.8, line_opacity=0.5, line_weight=1.5, line_color='black', range_color=[0, 2], highlight=True,).add_to(mf)

    if 'Internal Movements' in selectData_tourism:
        movement_map = folium.Choropleth(geo_data=country_geo, name="Internal Movements", data=travel_dataset, columns=["id", "IMC"], nan_fill_color="grey", nan_fill_opacity=0.5, key_on="feature.id", bins=[
            0, 1, 2, 3, 4], fill_color='RdYlGn', fill_opacity=0.8, line_opacity=0.5, line_weight=1.5, line_color='black', range_color=[0, 2], highlight=True,).add_to(mf)

elif travel_profile == 'Education':
    selectData_education = st.sidebar.multiselect(
        "Select preferred Infromation to be present in the map:", ["Schools", "Public Transport"])

    if 'Schools' in selectData_education:
        shops_map = folium.Choropleth(geo_data=country_geo, name="School closures", data=travel_dataset, columns=["id", "ET"], nan_fill_color="grey", nan_fill_opacity=0.5, key_on="feature.id", bins=[
            0, 1, 2, 3, 4], fill_color='RdYlGn', fill_opacity=0.8, line_opacity=0.5, line_weight=1.5, line_color='black', range_color=[0, 2], highlight=True,).add_to(mf)

    if 'Public Transport' in selectData_education:
        transport_map = folium.Choropleth(geo_data=country_geo, name="Public Transport", data=travel_dataset, columns=["id", "TC"], nan_fill_color="grey", nan_fill_opacity=0.5, key_on="feature.id", bins=[
            0, 1, 2, 3, 4], fill_color='RdYlGn', fill_opacity=0.8, line_opacity=0.5, line_weight=1.5, line_color='black', range_color=[0, 2], highlight=True,).add_to(mf)


else:
    selectData_medical = st.sidebar.multiselect(
        "Select preferred Infromation to be present in the map:", ["Hospitals", "Public Transport"])

    ################# medical Profile Map - Shops  ##########################
    if 'Hospitals' in selectData_medical:
        shops_map = folium.Choropleth(geo_data=country_geo, name="Hospitals", data=travel_dataset, columns=["id", "HC"], nan_fill_color="grey", nan_fill_opacity=0.5, key_on="feature.id", bins=[
            0, 1, 2, 3, 4], fill_color='RdYlGn', fill_opacity=0.8, line_opacity=0.5, line_weight=1.5, line_color='black', range_color=[0, 2], highlight=True,).add_to(mf)

    if 'Public Transport' in selectData_medical:
        transport_map = folium.Choropleth(geo_data=country_geo, name="Public Transport", data=travel_dataset, columns=["id", "TC"], nan_fill_color="grey", nan_fill_opacity=0.5, key_on="feature.id", bins=[
            0, 1, 2, 3, 4], fill_color='RdYlGn', fill_opacity=0.8, line_opacity=0.5, line_weight=1.5, line_color='black', range_color=[0, 2], highlight=True,).add_to(mf)


st.sidebar.header("Select Country:")

############ Return seclected country #################


def getFromCon(countries_travelFrom):
    return countries_travelFrom


def getToCon(countries_travelTo):
    return countries_travelTo


countries_travelFrom = st.sidebar.selectbox(
    "🛫 Travel from:", [item[0] for item in countries_and_codes], format_func=getFromCon)
countries_travelTo = st.sidebar.selectbox(
    "🛬 Travel to:", [item[0] for item in countries_and_codes], format_func=getToCon)


today = datetime.now()

# Last update info
dt_string = today.strftime("%B %d, %Y %I:%M:%S %p")

############ Display country count ######################
def get_total_open_country (countries_travelFrom):
    try:
        openCountry = travel_dataset_country.loc[(
            travel_dataset_country['Country'] == countries_travelFrom), 'Total Open Country '].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return openCountry

def get_total_rest_country (countries_travelFrom):
    try:
        restCountry = travel_dataset_country.loc[(
            travel_dataset_country['Country'] == countries_travelFrom), 'Total Restricted Country'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return restCountry

def get_total_close_country (countries_travelFrom):
    try:
        closeCountry = travel_dataset_country.loc[(
            travel_dataset_country['Country'] == countries_travelFrom), 'Total Closed Country'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return closeCountry

def get_total_unknown_country (countries_travelFrom):
    try:
        unknownCountry = travel_dataset_country.loc[(
            travel_dataset_country['Country'] == countries_travelFrom), 'Total Unknown Country'].iloc[0]
        
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return unknownCountry

col1, col2, col3, col4 = st.columns(4)

col1.metric("Open Country", "")
col1.markdown(
    f'<p class="font-allow" >{get_total_open_country (countries_travelFrom)}</p>',
    unsafe_allow_html=True
)
col2.metric("Restricted Country", "")
col2.markdown(
    f'<p class="font-restrict" >{get_total_rest_country (countries_travelFrom)}</p>',
    unsafe_allow_html=True
)
col3.metric("Closed Country", "")
col3.markdown(
    f'<p class="font-close" >{get_total_close_country (countries_travelFrom)}</p>',
    unsafe_allow_html=True
)
col4.metric("Unkonwn Country", "")
col4.markdown(
    f'<p class="font-unknown" >{get_total_unknown_country (countries_travelFrom)}</p>',
    unsafe_allow_html=True
)

################## Map ##########################

frame = folium.Figure(width=2050, height=550)

#################Tooltip #############################
#travel_df = pd.DataFrame(travel_dataset)
#country_df = pd.DataFrame(country_geo2)

#df_outer = pd.merge(country_df, travel_df, how='inner', left_on=[
#                    'English Name'], right_on=['Country']).dropna()

#######################################################
################## Travel Allowance Map ##########################

allTravel_df = pd.DataFrame(travel_dataset_country, columns=['Country', 'id' , 'OCS','Country Name'])
travel_df = pd.DataFrame(travel_dataset,columns=['Country', 'id' ,'TEC' ])

selectedCountry = pd.merge(allTravel_df, travel_df, how='inner', left_on=[
                    'Country Name'], right_on=['Country'])
result = selectedCountry.loc[selectedCountry['Country_x']==countries_travelFrom]

map = folium.Choropleth(geo_data=country_geo, name="Travel From  Entry", data=result, columns=["id_y", "OCS"], nan_fill_color="grey", nan_fill_opacity=0.5, key_on="feature.id", bins=[
                        0, 1, 2, 3, 4], fill_color='RdYlGn', fill_opacity=0.8, line_opacity=0.5, line_weight=1.5, line_color='black', range_color=[0, 2], highlight=True, legend=False).add_to(mf)


folium.TileLayer('cartodbdark_matter', name="Dark mode",
                 control=True).add_to(mf)
folium.LayerControl().add_to(mf)
Fullscreen().add_to(mf)


##################  Map Tooltip ##########################


map.geojson.add_child(folium.features.GeoJsonTooltip
                      (fields=['name'],
                       aliases=['Country:'],
                       labels=True))


                       
folium_static(mf, width=1545, height=680)

st.sidebar.info("Last Updated at: **{}**".format(dt_string))

#########Display Information ################
st.markdown("***")
st.subheader("Travel Restrictions")

# travel entry


def get_country_travel_to(countries_travelTo):
    travelStatus = travel_dataset.loc[(
        travel_dataset['Country'] == countries_travelTo), 'Traveller Entry'].iloc[0]
    if travelStatus == 'Allowed':
        try:
            return "✅", travelStatus
        except:
            st.warning("No data available")
            st.stop()
    elif travelStatus == 'Partially Allowed':
        try:
            return "⚠️", travelStatus
        except:
            st.warning("No data available")
            st.stop()
    elif travelStatus == 'Banned':
        try:
            return "⛔", travelStatus
        except:
            st.warning("No data available")
            st.stop()
    else:
        return st.warning("No data available"), st.stop()
        

def get_country_travel_from(countries_travelFrom, countries_travelTo):
    try: 
        if (countries_travelFrom != countries_travelTo):
            travelStatus = travel_dataset_country.loc[(
                travel_dataset_country['Country'] == countries_travelFrom) & (travel_dataset_country['Country Name'] == countries_travelTo), 'Other Country status'].iloc[0]
            if travelStatus == 'Open Country ':
                try:
                    return "✅",travelStatus
                except:
                    st.warning("No data available")
                    st.stop()
            elif travelStatus == 'Restricted Country':
                try:
                    return "⚠️", travelStatus
                except:
                    st.warning("No data available")
                    st.stop()
            elif travelStatus == 'Closed Country':
                try:
                    return "⛔", travelStatus
                except:
                    st.warning("No data available")
                    st.stop()
        else:
            return st.warning("No data available, you have selected travel from and travel to same country"), st.stop()
    except:
        if (countries_travelFrom != countries_travelTo):
            return st.warning("No data available"), st.stop()   


st.write("✈️** Entry For Travelers: **", get_country_travel_from(countries_travelFrom, countries_travelTo))

# covid test


def get_country_test_as_dict(countries_travelTo):
    try:
        covidTest = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Covid-19 Test'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return covidTest


st.write("🧪** Testing: **", get_country_test_as_dict(countries_travelTo))
# quarantine


def get_country_quarantine_as_dict(countries_travelTo):
    try:
        quarantine = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Quarantine'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return quarantine


st.write("🏠** Quarantine Details: **",
         get_country_quarantine_as_dict(countries_travelTo))
# masks


def get_country_masks_as_dict(countries_travelTo):
    try:
        masks = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Masks'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return masks


st.write("😷** The mask information is: **",
         get_country_masks_as_dict(countries_travelTo))

############ Profile Details ####################
st.markdown("***")
st.subheader("Local Restrictions")

# travel entry


def get_profile_as_dict(travel_profile):
    if travel_profile == 'Tourism':
        shoppingProfile = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Shopping'].iloc[0]
        TransportationProfile = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Transportation'].iloc[0]
        PublicEventProfile = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Public events'].iloc[0]
        MovementProfile = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Internal movement'].iloc[0]

        return shoppingProfile, TransportationProfile, PublicEventProfile, MovementProfile
    elif travel_profile == 'Education':
        SchoolsProfile = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Education'].iloc[0]
        TransportationProfile = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Transportation'].iloc[0]
        return SchoolsProfile, TransportationProfile
    elif travel_profile == 'Medical':
        hospitalProfile = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Healthcare'].iloc[0]
        TransportationProfile = travel_dataset.loc[(
            travel_dataset['Country'] == countries_travelTo), 'Transportation'].iloc[0]
        return hospitalProfile, TransportationProfile
    else:
        return st.error("No data available"), st.stop()
        


st.write("🧳 ** Profile Selected is: **", travel_profile)
st.write("🗺️ ** Profile Details: **", get_profile_as_dict(travel_profile))


############ Country Statistics ####################
st.markdown("***")
st.subheader("Country Statistics")


def get_total_cases(countries_travelTo):
    try:
        total_cases_country = Covid_cases_df.loc[(
            Covid_cases_df['Name'] == countries_travelTo), 'Cases - cumulative total'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return total_cases_country


def get_total_deaths(countries_travelTo):
    try:
        total_deaths_country = Covid_cases_df.loc[(
            Covid_cases_df['Name'] == countries_travelTo), 'Deaths - cumulative total'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return total_deaths_country


def get_weekcases(countries_travelTo):
    try:
        total_weekcases = Covid_cases_df.loc[(Covid_cases_df['Name'] == countries_travelTo),
                                             'Cases - newly reported in last 7 days per 100000 population'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return total_weekcases

##################### Cases ################################
col1, col2, col3, col4, col5 = st.columns(5)

df_data_cases = pd.DataFrame(Covid_cases_df, columns=["Name", "Cases - cumulative total", "Cases - newly reported in last 24 hours",
                             "Deaths - cumulative total", "Deaths - newly reported in last 24 hours", "Cases - newly reported in last 7 days per 100000 population"])
cases_value = df_data_cases.loc[df_data_cases['Name']
                                == countries_travelTo, 'Cases - cumulative total']
col1.metric("The total cases: ", cases_value.to_csv(header=False, index=False))

new_cases_value = df_data_cases.loc[df_data_cases['Name'] ==
                                    countries_travelTo, 'Cases - newly reported in last 24 hours']
col2.metric("The total cases in last 24 hours: ",
            new_cases_value.to_csv(header=False, index=False))

deaths_value = df_data_cases.loc[df_data_cases['Name']
                                 == countries_travelTo, 'Deaths - cumulative total']
col3.metric("The total deaths: ", deaths_value.to_csv(
    header=False, index=False))

new_deaths_value = df_data_cases.loc[df_data_cases['Name'] ==
                                     countries_travelTo, 'Deaths - newly reported in last 24 hours']
col4.metric("The total deaths in last 24 hours: ",
            new_deaths_value.to_csv(header=False, index=False))

cum_value = df_data_cases.loc[df_data_cases['Name'] == countries_travelTo,
                              'Cases - newly reported in last 7 days per 100000 population']
col5.metric("New cases last 7 days out of 100,000 people:",
            cum_value.to_csv(header=False, index=False))


############ Vaccination ####################
st.markdown("***")
st.subheader("Vaccination")


coutryCode = travel_dataset.loc[(
    travel_dataset['Country'] == countries_travelTo), 'id'].iloc[0]



def get_vaccine_as_dict(countries_travelTo):
    try:
        Vaccine_name = Vaccination_data.loc[(
            Vaccination_data['Country'] == countries_travelTo), 'VACCINES_USED'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return Vaccine_name


def get_vaccineNum_as_dict(countries_travelTo):
    try:
        Vaccine_num = Vaccination_data.loc[(
            Vaccination_data['Country'] == countries_travelTo), 'NUMBER_VACCINES_TYPES_USED'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return Vaccine_num


def get_vaccinePer_as_dict(countries_travelTo):
    try:
        Vaccine_per = Vaccination_data.loc[(
            Vaccination_data['Country'] == countries_travelTo), 'PERSONS_FULLY_VACCINATED_PER100'].iloc[0]
    except:
        st.warning("No information is available for the selected date")
        st.stop()
    return Vaccine_per


st.write("🛡️ **Approved Vaccine :** ", get_vaccine_as_dict(countries_travelTo))
st.write("✔️ **Total Number of Approved Vaccine :**")
st.subheader(get_vaccineNum_as_dict(countries_travelTo))
st.write("💉 **Percentage of Population Fully Vaccinated :**")
st.subheader(get_vaccinePer_as_dict(countries_travelTo))
