# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie:cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)
cnx = st.connect("snowflake")
session = cnx.session()

option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
)


name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your Smoother order will be ", name_on_order)

st.write("You selected:", option)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe,max_selections=5)


if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+"""')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
    st.write(my_insert_stmt)
