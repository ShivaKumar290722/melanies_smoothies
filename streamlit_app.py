import streamlit as st 
import pandas as pd
import requests
from snowflake.snowpark.functions import col  

st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# User input for the name on the smoothie
name_on_order = st.text_input("Name on Smoothie:")
if name_on_order:
    st.write("The name on your smoothie will be:", name_on_order)
else:
    st.write("Please enter a name for your smoothie.")

# Get Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch the fruit options from the table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df, use_container_width=True)

# User input for choosing the ingredients (list of fruit names)
ingredients_list = st.multiselect('Choose up to 5 ingredients:', pd_df['FRUIT_NAME'].tolist(), max_selections=5)

if ingredients_list:
    # Join fruit names into a single string for insertion
    ingredients_string = ' '.join(ingredients_list)
    
    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        st.subheader(fruit_chosen + ' Nutrition Information')

        # Fix API URL
        response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        if response.status_code == 200:
            json_data = response.json()
            # Normalize if needed
            sf_df = pd.json_normalize(json_data)
            st.dataframe(sf_df, use_container_width=True)
        else:
            st.error(f"Failed to get data for {fruit_chosen}")

    # Only enable submission if name is provided
    if name_on_order:
        time_to_insert = st.button('Submit Order')

        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
      
    else:
        st.warning("Please enter a name on your smoothie to submit the order.")


