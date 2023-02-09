import streamlit as st
import pandas as pd
import boto3
import time
import sqlite3



def extract_files(bucket_name, prefix):
    s3 = boto3.resource('s3',
         aws_access_key_id="AKIAWFZMBX3FS5T6CQ4I",
         aws_secret_access_key= "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")
    result = []
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=prefix):
        result.append(obj.key)
    return result

def link_gen(input):
    station = input[:4]
    year = input[4:8]
    month = input[8:10]
    day = input[10:12]

    fs = "https://noaa-nexrad-level2.s3.amazonaws.com/{}/{}/{}/{}/{}".format(year,month,day,station,input)
    return fs

def search_box():
    st.write("# NexRad Data Downloader 📡")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        year_val = cursor.execute("SELECT DISTINCT year FROM nexrad")
        year = st.selectbox(
            'Which Year ?',
            [i[0] for i in year_val],
            on_change = search_box
            )

    with col2:
        month_val = cursor.execute("SELECT DISTINCT month FROM nexrad WHERE year = '{}' ".format(year))
        month = st.selectbox(
            'What Month ?',
            [i[0] for i in month_val],
            on_change = search_box
        )
    with col3:
        day_val = cursor.execute("SELECT DISTINCT day FROM nexrad WHERE year = '{}' AND month = '{}'".format(year,month))
        day = st.selectbox(
            'What Day ?',
            [i[0] for i in day_val],
            on_change = search_box
        )
    with col4:
        station_val = cursor.execute("SELECT DISTINCT station FROM nexrad WHERE year = '{}' AND month = '{}' AND day = '{}'".format(year,month,day))
        station = st.selectbox(
            'What Hour ?',
            [i[0] for i in station_val],
            on_change = search_box
        )
    global path
    path = "{}/{}/{}/{}".format(year,month,day,station)

    st.button('Search 🔎',key='search',on_click=display_files)

    st.write("# OR")

    filename_input = st.text_input(
        "Enter filename 👇",
        placeholder="File Name",
    )
    link = " "
    if st.button('Get Link!',key='getLink'):
        link = link_gen(filename_input)
    st.write("Link: {}".format(link))

def update_first():
    st.session_state.count = 0
    st.write("Downloading.....")
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.write("Done!")

def display_files():
    directories = extract_files("noaa-nexrad-level2", path)
    df = pd.DataFrame({"name":directories})

    for i in range(len(df)):
        col5 , col6 = st.columns(2)
        with col5:
            name = df.iloc[i]['name']
            st.write(name)
        with col6:
            st.button("Download Now!",key=name ,on_click=update_first)

connection = sqlite3.connect("/Users/parvashah/Documents/damg_7245/meta_data.db")
cursor = connection.cursor()

search_box()




    