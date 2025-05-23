# Import python packages
import streamlit as st 
import requests
from snowflake.snowpark.functions import col  

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

# User input for the name on the smoothie
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Get Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch the fruit options from the table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# User input for choosing the ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe , max_selections=5)

if ingredients_list:
    # Concatenate chosen ingredients into a string
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    st.write(ingredients_string)

    # SQL INSERT statement to insert the order details (both ingredients and name)
    my_insert_stmt = """ 
    INSERT INTO smoothies.public.orders (name_on_order, ingredients) 
    VALUES ('""" + name_on_order + """', '""" + ingredients_string + """')
    """

    # Show the insert statement (optional, for debugging)
    # st.write(my_insert_stmt)

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
