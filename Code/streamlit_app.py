

# to run streamlit code in .py files: in the folder where the .py file is, run
# streamlit run filename.py [ARGUMENTS]

import streamlit as st

st.set_page_config(
    page_icon='📖',
    initial_sidebar_state='expanded'
)


page = st.sidebar.selectbox(
    'Select a page:',
    ('About', 'Predict 30-day income')
)


if page == 'About':
    st.title('Income Optimizer for Airbnb Hosts')
    st.subheader('About this project')
    st.write('''
This is a Streamlit app that hosts my Poe vs. Austen model.
The best model I found was....
You can get in touch with me on these websites....
etc.
    ''')
elif page == 'Predict 30-day income':
    st.title('Predict your 30-day income')

    st.subheader("Please provide some information on your Airbnb listing")

    import numpy as np
    import pandas as pd
    import joblib

    X_train_m1 = pd.read_csv("../Data/m1_X_train.csv")
    property_type_list = list(X_train_m1['property_type_recoded'].unique())

    # build data input widgets
    property_type = st.selectbox("Property type", property_type_list)

    st.markdown('---')

    col1, col2, col3 = st.columns(3)
    with col1:
        county = st.selectbox('county',['San Francisco','San Mateo','Santa Clara'])
        neighborhood_list = X_train_m1.loc[X_train_m1['county']==county, 'neighborhood_recoded'].unique()
        neighborhood = st.selectbox('Neighborhood', neighborhood_list)
        accommodates = st.number_input("Total number of poeple", 1, 10)
        bedrooms = st.number_input("Number of bedrooms", 1, 5)


    with col2:
        beds = st.number_input("Number of beds", 1,6)
        bathrooms = st.selectbox("Number of bathrooms",
                          [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])
        bathroom_type = st.selectbox("Bathroom type",
                            ["Private","Shared"])
        number_of_reviews_ltm = st.number_input("Number of reviews last 12 months", 1)

    with col3:
        minimum_nights = st.number_input("minimum_nights", 1)
        maximum_nights = st.number_input("maximum_nights", 1)
        number_of_reviews = st.number_input("Total number of reviews", 1)
        number_of_reviews_l30d = st.number_input("Number of reviews last 30 days", 1)



    st.markdown('---')

    st.write("Please check the amenities available in your listing unit.")
    # amenities
    col11, col12, col13, col14, col15 = st.columns([0.8,1.2,1.8,2,2])
    with col11:
        wifi = st.checkbox("Wifi")
        pool = st.checkbox("Pool")

    with col12:
        BBQ_grill = st.checkbox("BBQ_grill")
        backyard = st.checkbox("Backyard")

    with col13:
        patio_or_balcony = st.checkbox("Patio/balcony")
        private_entrance = st.checkbox("Private entrance")

    with col14:
        workspace = st.checkbox("Dedicated workspace")
        indoor_fireplace = st.checkbox("Indoor fireplace")
    with col15:
        outdoor_furniture = st.checkbox("Outdoor furniture")


    st.markdown('---')
    # review scores
    st.write("What are your review scores?")
    col21, col22, col23, col24 = st.columns(4)
    with col21:
        review_scores_rating = st.number_input('Overall rating', 1.0, 5.0)
        review_scores_accuracy = st.number_input('Accuracy', 1.0, 5.0)

    with col22:
        review_scores_cleanliness = st.number_input('Cleanliness', 1.0, 5.0)
        review_scores_checkin = st.number_input('Checkin', 1.0, 5.0)

    with col23:
        review_scores_communication = st.number_input('Communication', 1.0, 5.0)
        review_scores_location = st.number_input('Location', 1.0, 5.0)
    with col24:
        review_scores_value = st.number_input('Value', 1.0, 5.0)

    st.markdown('---')
    # provision of info on listing webpage
    st.write("Is the following information provided on your Airbnb page?")
    col17, col18, col19 = st.columns(3)
    with col17:
        neighborhood_overview_f = st.checkbox("Neighborhood overview")
        host_about_f = st.checkbox("About the host")
    with col18:
        host_response_time_f = st.checkbox("Host repsonse time")
        host_response_rate_f = st.checkbox("Host response rate")
    with col19:
        host_neighbourhood_f = st.checkbox("Host neighbourhood")
        host_acceptance_rate_f = st.checkbox("Host acceptance rate")

    st.markdown('---')
    st.subheader("Your expected listing price")
    price_to_charge = st.slider("How much do you want to charge per night?", 0, 1000)

    #st.write("I'd like to charge $", price_to_charge, "per night")
    st.markdown('---')
    st.subheader("Income Prediction")


    # Model 1: Predict listing Predicted

    input_data_m1 = {
              #'price': price,
              #'price_pred': price_pred,
              'county': county,
              'neighborhood_recoded': neighborhood,
              'property_type_recoded': property_type,
              'accommodates': int(accommodates),
              'bedrooms': int(bedrooms),
              'beds': int(beds),
              'bathrooms': bathrooms,
              'bathroom_type': bathroom_type,
              'minimum_nights': int(minimum_nights),
              'maximum_nights': int(maximum_nights),
              # amenities
              'Wifi': wifi,
              'Dedicated_workspace': workspace,
              'Private_entrance': private_entrance,
              'Patio_or_balcony': patio_or_balcony,
              'Backyard': backyard,
              'BBQ_grill': BBQ_grill,
              'Outdoor_furniture': outdoor_furniture,
              'Indoor_fireplace': indoor_fireplace,
              'Pool': pool,
              # review scores
              'review_scores_rating': review_scores_rating,
              'review_scores_accuracy': review_scores_accuracy,
              'review_scores_cleanliness': review_scores_cleanliness,
              'review_scores_checkin': review_scores_checkin,
              'review_scores_communication': review_scores_communication,
              'review_scores_location': review_scores_location,
              'review_scores_value': review_scores_value,
              # number of reviews
              'number_of_reviews': number_of_reviews,
              'number_of_reviews_ltm': number_of_reviews_ltm,
              'number_of_reviews_l30d': number_of_reviews_l30d,
              # info availability
              'neighborhood_overview_f': neighborhood_overview_f,
              'host_about_f': host_about_f,
              'host_response_time_f': host_response_time_f,
              'host_response_rate_f': host_response_rate_f,
              'host_acceptance_rate_f': host_acceptance_rate_f,
              'host_neighbourhood_f': host_neighbourhood_f
              }
    input_data_df_m1 = pd.DataFrame(input_data_m1, index=[0])
    #st.dataframe(input_data_df_m1)






    # load saved model and predict
    m1_filename = '../Models/m1_gs_rf_joblib.pkl'
    m1 = joblib.load(m1_filename)
    price_pred = m1.predict(input_data_df_m1)[0]

    st.write("Predicted listing price is", round(price_pred,2), "dollars.")


    # Model 2

    input_data_m2 = {
              'price': price_to_charge,
              'price_pred': price_pred,
              'county': county,
              'neighborhood_recoded': neighborhood,
              'property_type_recoded': property_type,
              'accommodates': int(accommodates),
              'bedrooms': int(bedrooms),
              'beds': int(beds),
              'bathrooms': bathrooms,
              'bathroom_type': bathroom_type,
              'minimum_nights': int(minimum_nights),
              'maximum_nights': int(maximum_nights),
              # amenities
              'Wifi': wifi,
              'Dedicated_workspace': workspace,
              'Private_entrance': private_entrance,
              'Patio_or_balcony': patio_or_balcony,
              'Backyard': backyard,
              'BBQ_grill': BBQ_grill,
              'Outdoor_furniture': outdoor_furniture,
              'Indoor_fireplace': indoor_fireplace,
              'Pool': pool,
              # review scores
              'review_scores_rating': review_scores_rating,
              'review_scores_accuracy': review_scores_accuracy,
              'review_scores_cleanliness': review_scores_cleanliness,
              'review_scores_checkin': review_scores_checkin,
              'review_scores_communication': review_scores_communication,
              'review_scores_location': review_scores_location,
              'review_scores_value': review_scores_value,
              # number of reviews
              'number_of_reviews': number_of_reviews,
              'number_of_reviews_ltm': number_of_reviews_ltm,
              'number_of_reviews_l30d': number_of_reviews_l30d,
              # info availability
              'neighborhood_overview_f': neighborhood_overview_f,
              'host_about_f': host_about_f,
              'host_response_time_f': host_response_time_f,
              'host_response_rate_f': host_response_rate_f,
              'host_acceptance_rate_f': host_acceptance_rate_f,
              'host_neighbourhood_f': host_neighbourhood_f
              }
    input_data_df_m2 = pd.DataFrame(input_data_m2, index=[0])
    # st.dataframe(input_data_df_m2)

    m2_filename = '../Models/m21_gs_rf_joblib_poor.pkl'
    m2 = joblib.load(m2_filename)
    avail30_pred  = round(m2.predict(input_data_df_m2)[0])
    booking_pred = 30 - avail30_pred
    income_total = round(price_to_charge * avail30_pred, 2)

    st.write("Predicted 30-day vacancy is", round(avail30_pred,2), "days, and predicted booking days are", booking_pred, "days.")

    st.write("At your desired listing price ($", price_to_charge, "), your predicted total income for the next 30 days is", income_total, "dollars.")
