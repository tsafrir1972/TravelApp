import subprocess
import requests
import os
import json
import pymongo
import functools
import re
import pandas as pd
import datetime as dt
import time
import streamlit as st
from PIL import Image
import random
import numpy as np
from random import sample
import base64
import os
from email.message import EmailMessage
import ssl
import smtplib




class TravelOptions:

    def __init__(self):

        self.get_user_input()

    def get_user_input(self):
        global selected_city
        global selected_flight_budget
        global selected_hotel_budget
        global selected_restorants_budget
        global user_email
        #global df_list_airports
        #global df_airports
        #global app_flights
        global our_email
        ############################### city choose ################################

        def get_base64(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()

        def set_background(png_file):
            bin_str = get_base64(png_file)
            page_bg_img = '''
                    <style>
                    .stApp {
                    background-image: url("data:image/png;base64,%s");
                    background-size: cover;
                    }
                    </style>
                    ''' % bin_str
            st.markdown(page_bg_img, unsafe_allow_html=True)

        #set_background(r"C:\Python_Project\my_trip.png")

        st.title("Travel Planning Application")
        # gc = geonamescache.GeonamesCache()
        # cities = gc.get_cities()

        selected_city = st.selectbox(
            'Enter Your Travel City : ',
            ('New York','San Francisco','Honolulu', 'Bankok', 'Barcelona', 'Dubai', 'Paris', 'london', 'Tel Aviv'))

        ############################### flight budget choose ########################

        global selected_flight_budget

        selected_flight_budget = st.selectbox(
            'Enter Your Flight Budget : ',
            ('500', '1000', '1500'))

        ########################### Hotel Budget Choose ######################################
        global selected_hotel_budget

        selected_hotel_budget = st.selectbox(
            'Enter Your Hotel Budget : ',
            ('50', '100', '150'))
        ########################### Restorants Budget Choose ######################################
        global selected_restorants_budget

        selected_restorants_budget = st.selectbox(
            'Enter Your Restorant Budget : ',
            ('50', '100', '150'))
        ########################### Enter Email ######################################
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        check_email = 'N'
        keys = random.sample(range(1000, 9999), 1)

        def check(email):

            if (re.fullmatch(regex, email)):

                check_email = 'Y'


            else:

                check_email = 'N'

            return check_email

        form = st.form(key='my_form')
        user_email = form.text_input(label='Enter Your Email', key=1)
        submit_button = form.form_submit_button(label='Submit')


        # user_email = st.text_input('Please Enter Your Email :')
        for i in keys:
            if submit_button:
                # print(check(user_email))

                if check(user_email) == 'N':
                    st.write('The email is invalid please type again and press submit')
                    None
                else:
                    #self.Process_User_Input()
                    #self.send_to_user_email(user_email)
                    break




