import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image


# =========== pdf summary report of website ===
def create_pdf_report():
    pass


# =========== load data ===
dataset = pd.read_excel('workFindingProgress.xlsx', usecols='A,B,C,D,G,I')
dataset_job_boards = pd.read_excel('workFindingProgress.xlsx', usecols='D')
dataset_job_location = pd.read_excel('workFindingProgress.xlsx', usecols='I')


st.set_page_config(page_title='ok', layout='wide')


# =========== sidebar ===
st.sidebar.header("Filters")
job_board = st.sidebar.multiselect('Job board filter', 
                                   options=dataset['JOB_BOARD'].unique(), 
                                   default=dataset['JOB_BOARD'].unique())
    
selection_query = dataset.query("JOB_BOARD == @job_board")


# =========== creating values for round diagram of job_boards ===
linkedIn_count = dataset.query('JOB_BOARD == "LinkedIn"')['JOB_BOARD'].count()
allJobs_count = dataset.query('JOB_BOARD == "AllJobs"')['JOB_BOARD'].count()
all_job_boards_count = dataset['JOB_BOARD'].count()

job_boards_count = [linkedIn_count, 
                    allJobs_count, 
                    all_job_boards_count - linkedIn_count - allJobs_count]

dataset_job_boards.dropna(inplace=True)


# =========== intro ===
st.title("My long IT way")
st.header(len(dataset.index))
st.text("vacancies I've already applied")
st.subheader("Below you can see the table with positions I applied")
st.dataframe(selection_query)


# =========== round diagram ===
pie_chart = px.pie(dataset_job_boards, 
                   title='Job Boards helping me', 
                   names=['LinkedIn', 'AllJobs', 'Other'], 
                   values=job_boards_count)

st.plotly_chart(pie_chart)


# =========== local styles configs ===
hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


# =========== graph with applications amount per day ===
dataset['APPLY_DATE'] = pd.to_datetime(dataset['APPLY_DATE'])
date_counts = dataset['APPLY_DATE'].value_counts().reset_index() # how much times each date repeats

date_counts.columns = ['Date', 'Applications']
date_counts = date_counts.sort_values(by='Date')

fig = px.bar(date_counts, x = 'Date', y ='Applications', title='Applications amount per day')
fig.update_xaxes(type='category', tickangle = 45)

st.plotly_chart(fig)


# =========== country of position diagram values ===
israel_count = dataset.query('COUNTRY_OF_POSITION == "Israel"')['COUNTRY_OF_POSITION'].count()
bulgaria_count = dataset.query('COUNTRY_OF_POSITION == "Bulgaria"')['COUNTRY_OF_POSITION'].count()
remote_count = dataset.query('COUNTRY_OF_POSITION == "Remote"')['COUNTRY_OF_POSITION'].count()

countries_count = dataset['COUNTRY_OF_POSITION'].count()

others_count = [israel_count, bulgaria_count, remote_count, countries_count-israel_count-bulgaria_count-remote_count]
dataset_job_location.dropna(inplace=True)


# =========== COUNTRY_OF_POSITION round diagram ===
pie_ch = px.pie(dataset_job_location, 
                   title='Position location', 
                   names=['Israel', 'Bulgaria', 'Remote', 'Others'], 
                   values=others_count)

st.plotly_chart(pie_ch)  
