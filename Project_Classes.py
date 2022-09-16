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
import string



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

        set_background(r"C:\Python_Project\my_trip.png")

        st.title("Travel Planning Application")
        # gc = geonamescache.GeonamesCache()
        # cities = gc.get_cities()

        selected_city = st.selectbox(
            'Enter Your Travel City : ',
            ('New York', 'Honolulu', 'Bankok', 'Barcelona', 'Dubai', 'Paris', 'london', 'Tel Aviv'))

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
                    self.Process_User_Input()
                    self.send_to_user_email(user_email)
                    break




    def Process_User_Input(self):

        with st.spinner('Your Vacation Is On Its Way,Please Wait...'):
            app_flights = Flights().find_flight(selected_city)
            app_hotels = Hotels().find_hotels(selected_city)
            app_restorants = Restorants().find_restorants(selected_city)
            time.sleep(5)
        st.success('Done! Please Check Your Email For Your Vacation Recommandations (Your Flights Are Listed Below) ')
        st.balloons()

    def send_to_user_email(self, user_email):

            email_sender = 'travel.app.tsafrir.noah@gmail.com'
            email_password = 'uryujyfrnczkcmdz'
            email_receiver = user_email

            subject = 'Check out your travel recommendations'
            flights_list = ' '.join(map(str,df_list_airports))
            #body = "Your Recommended Flights - " + flights_list + "\n" + "Your Recommended Hotels  - " + flights_list + "\n" + "Your Recommended Restorants - " + flights_list
            body = "Your Recommended Travel Information Are - \n\n\n" + "\n\n FLIGHTS \n\n " + df_airports.to_string() + "\n\n HOTELS \n\n " + df_hotels.to_string() + "\n\n RESTORANTS \n\n " + df_restorants.to_string()
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

        #print('Application process finished !')


class Flights():

    def find_flight(self, city):
        global df_list_airports
        global df_airports
        # print(city)
        url = "https://travel-advisor.p.rapidapi.com/airports/search"

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["travel_app"]
        mycol = mydb["Flights"]

        x = mycol.delete_many({})

        client = pymongo.MongoClient("mongodb://localhost:27017/")

        querystring = {"query": city, "locale": "en_US"}

        headers = {
            'X-RapidAPI-Key': 'fd7a716347msh5fdefeb55c31dc8p15334bjsn20218c896049',
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        list_json = json.loads(response.text)
        list_length = len(list_json)

        for i in range(0, list_length):
            # print(list_json[i])
            var_price = random.randint(900, 1200)
            var_flight_number = random.randint(10000, 15000)
            list_json[i]['flight_number'] = 'NY' + str(var_flight_number)
            list_json[i]['price_in_dollars'] = var_price
            mycol.insert_one(list_json[i])

        data = pd.DataFrame(list(mycol.find()))

        data_length = data.shape[0]

        data['Price'] = np.random.randint(900, 1000, data.shape[0])

        updated = data['longitude']

        data = data.applymap(str)

        df_airports = data.loc[:, ["name", "flight_number", "price_in_dollars"]]

        df_airports = df_airports.loc[
            df_airports["price_in_dollars"].apply(pd.to_numeric) <= int(selected_flight_budget)]

        df_list_airports = df_airports.values.tolist()

        df_airports.sort_values(by=['price_in_dollars'], ascending=False)

        st.table(df_airports)
        print(df_list_airports)
        return df_list_airports


class Hotels():

    def find_hotels(self, city):

        global df_hotels

        if city == 'New York':
            city = "60763"
        elif city == 'bangkok':
            city = "301643"
        elif city == 'Barcelona':
            city = "1465497"

        url = "https://travel-advisor.p.rapidapi.com/airports/search"

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["travel_app"]
        mycol = mydb["Hotels"]

        x = mycol.delete_many({})

        client = pymongo.MongoClient("mongodb://localhost:27017/")

        url = "https://travel-advisor.p.rapidapi.com/hotels/list"

        querystring = {"location_id": city, "adults": "1", "rooms": "1", "nights": "2", "offset": "0",
                       "currency": "USD", "order": "asc", "limit": "10", "sort": "recommended", "lang": "en_US"}

        headers = {
            'X-RapidAPI-Key': 'fd7a716347msh5fdefeb55c31dc8p15334bjsn20218c896049',
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        response_hotels = requests.request("GET", url, headers=headers, params=querystring)

        dict_json = json.loads(response_hotels.text)

        try:

                print(' dict json :',dict_json)

                json_length = len(dict_json)

                print('hotels_list_length :', json_length)

                for list_json in dict_json.values():

                    list_length = len(list_json)


                    try:
                        for i in range(0, list_length):
                            try:
                                # print(f"The value for your request is {list_json[i]}")
                                None
                                var_price = random.randint(50, 150)
                                var_flight_number = random.randint(10000, 15000)

                                list_json[i]['price_in_dollars'] = var_price

                                mycol.insert_one(list_json[i])
                            except KeyError:
                                None
                                # print(f"There is no parameter with the '{list_json[i]}' key. ")
                    except:
                        None


                df_hotels = pd.DataFrame(list(mycol.find()))

                #df_hotels = df_hotels.reset_index(inplace=True)

                additional_cols = ['price_in_dollars']

                df_hotels = df_hotels.reindex(df_hotels.columns.tolist(), axis=1)

                df_hotels = df_hotels.applymap(str)

                df_hotels = df_hotels.loc[:, ["name", "hotel_class", "price_in_dollars"]]

                df_hotels = df_hotels.loc[df_hotels["price_in_dollars"].apply(pd.to_numeric) <= int(selected_hotel_budget)]

                # df_hotels['hotel_class'] = df_hotels['hotel_class'].astype('int')

                df_hotels.sort_values(by=['hotel_class'], ascending=False)

                st.table(df_hotels)

        except Exception:
            pass

class Restorants():

    def find_restorants(self, city):

        global df_restorants

        if city == 'New York':
            city = "60763"
        elif city == 'bangkok':
            city = "301643"
        elif city == 'Barcelona':
            city = "1465497"

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["travel_app"]
        mycol = mydb["Restorants"]

        x = mycol.delete_many({})

        client = pymongo.MongoClient("mongodb://localhost:27017/")

        url = "https://travel-advisor.p.rapidapi.com/restaurants/list"

        querystring = {"location_id": city, "restaurant_tagcategory": "10591",
                       "open_now": "false", "lang": "en_US"}

        headers = {
            'X-RapidAPI-Key': 'fd7a716347msh5fdefeb55c31dc8p15334bjsn20218c896049',
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        response_restorants = requests.request("GET", url, headers=headers, params=querystring)

        dict_json = json.loads(response_restorants.text)

        try:

                for list_json in dict_json.values():
                    # print(list_json)
                    list_length = len(list_json)

                    # print(list_length)
                    try:
                        for i in range(0, list_length):
                            try:
                                # print(f"The value for your request is {list_json[i]}")
                                None
                                var_price = random.randint(50, 150)
                                var_flight_number = random.randint(10000, 15000)
                                list_json[i]['price_in_dollars'] = var_price

                                mycol.insert_one(list_json[i])
                            except KeyError:
                                None
                                # print(f"There is no parameter with the '{list_json[i]}' key. ")
                    except:
                        None

                df_restorants = pd.DataFrame(list(mycol.find()))

                df_restorants = df_restorants.applymap(str)

                df_restorants = df_restorants.loc[:, ["name", "rating", "price_in_dollars"]]

                df_restorants = df_restorants.loc[
                    df_restorants["price_in_dollars"].apply(pd.to_numeric) <= int(selected_restorants_budget)]

                # df_restorants['rating'] = df_restorants['rating'].astype('int')

                df_restorants.sort_values(by=['rating'], ascending=False)

                print(df_restorants)
                st.table(df_restorants)
                st.balloons()
        except Exception:
            pass

class send_mail():

    def __init__(self):

        self.send_email_python()

    def send_email_python(self):
        email_sender = 'tsafrir.naya@gmail.com'
        email_password = 'gxqqwjqjidggktya'
        email_receiver = user_email    #'tsafrir.aloni@gmail.com'

        subject = 'Check out your travel recommandations'
        body = """
        Flights - 
        Hotels - 
        Restorants - 
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
