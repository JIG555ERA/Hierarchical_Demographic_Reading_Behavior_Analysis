import streamlit as st
import pandas as pd
import altair as alt

# ======= Config ======
st.set_page_config(page_title="Dashboard | H.D.R.B.A.", layout="wide")

# Logout utility for convenience
def logout():
    st.session_state.update({
        "otp_sent": False,
        "authenticated": False,
        "email": "",
        "otp": None,
        "otp_attempts": 0,
        "otp_timestamp": 0
    })
    st.switch_page("Auth.py")

if not st.session_state.get("authenticated", False):
    # st.switch_page('Auth.py')
    st.warning('**⚠️ :red[Unauthorised Access]**')
    st.switch_page('Auth.py')
    st.stop()

# ====== SIDEBAR CONTEXT ======
# LogIN status
st.sidebar.success(f"✅ Logged in as: {st.session_state.get('email', 'Unknown')}")
# Logout button
st.sidebar.button("🔓 Logout", on_click=logout)

# ====== DASHBOARD CONTEXT ======
st.title(":green[Hierarchical Demographic Reading Behavior Analysis]")

st.markdown("---")

excel_path='datasets/literacy_classification.xlsx'
# excel_link='https://1drv.ms/x/c/1d5d70a3020880fe/ETdnjLXmJ8FNnR-fNpSMtsIBb0ClDAhziZZz-T-FnXBHgg?e=NtCcMi'
sheets = ['population_table','population_table01','literacy_rate']

# ====== COMPILED INFO ======
with st.expander('Compiled Info'):
    dataset = pd.read_excel(excel_path, sheet_name=sheets[0], engine='openpyxl')
    dataset = dataset.set_index('year')
    st.header('Demographic reading behavior across METRO cities in india')
    st.write(dataset)

st.markdown("---")

# ====== POPULATION TREND (years = [2011,2015,2016,...,2025])
with st.expander('Population Trend'):
    dataset = pd.read_excel(excel_path, sheet_name=sheets[1], engine='openpyxl')
    dataset = dataset.set_index('year')
    tags = dataset.columns.tolist()
    option = st.multiselect('Select Metro Cities', tags) 

    col01, col02 = st.columns([1,1])
    with col01:
        st.header('Population Table')
        st.write(dataset[option])

    with col02:
        st.header('Population Analysis')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.bar_chart(dataset[option],x_label='year',y_label='population')

st.markdown("---")

# ====== LITERACY TREND (years = [2011,2017,2024])======
with st.expander('Literacy Trend'):
    literacy_data = pd.read_excel(excel_path, sheet_name=sheets[2], engine='openpyxl')
    col01, col02 = st.columns([1,1])

    with col01:
        st.header('Literacy Table')
        literacy_data = literacy_data.set_index('city')
        st.write(literacy_data)

    with col02:
        st.header('Literacy Analysis')
        literacy_data = literacy_data.reset_index()
        city_selected = st.selectbox('Select a city', literacy_data['city'].tolist())
        city_data = literacy_data[literacy_data['city'] == city_selected].set_index('city').T 
        city_data.columns = ['Literacy %']
        city_data = city_data.reset_index().rename(columns={'index': 'Year'})
        st.write(f"Literacy data for :red[{city_selected}:]")
        st.bar_chart(city_data, x='Year', y='Literacy %')
        # chart = alt.Chart(city_data).mark_line(point=True).encode(
        #     x='Year',
        #     y='Literacy %'
        # ).properties(
        #     width=700,
        #     height=400
        # )

        # st.altair_chart(chart, use_container_width=True)


