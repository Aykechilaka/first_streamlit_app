
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')
#Let's put a pick list here so they can pick the fruit they want to include
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
#display the table on the page
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display the table on the page
streamlit.dataframe(fruits_to_show)

# #New section to display fruityvice api response
# streamlit.header("Fruityvice Fruit Advice!")
# fruit_choice = streamlit.text_input('What fruit would you like information about?' 'Kiwi')
# streamlit.write('The user entered', fruit_choice)
# #import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
# # streamlit.text(fruityvice_response.json())
# # normalize the data to make it look better
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# # display the normalized version
# streamlit.dataframe(fruityvice_normalized)


# #create the repeatable code block (called function)
# def get_fruityvice_data(this_fruit_choice):
#    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#    return fruityvice_normalized
# #New section to display fruityvice api response
# streamlit.header("Fruityvice Fruit Advice!")
# try:
#   fruit_choice = streamlit.text_input('What fruit would you like information about?')
#   if not fruit_choice:
#     sreamlit.error("please select a fruit to get information.")
#   else:
#     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#     streamlit.dataframe(fruityvice_normalized)
# except URLError as e:
#   streamlit.error()


#don't run anything past here while we troubleshoot
#streamlit.stop()

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("select * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_rows)

# add_my_fruit = streamlit.text_input('What fruit would you like to add?')
# streamlit.write('Thanks for adding ', add_my_fruit)
# my_cur.execute("insert into fruit_load_list values('from streamlit')")



###########################################################################


import streamlit
import snowflake.connector

streamlit.header('View Our Fruit List - Add Your Favorites')

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO fruit_load_list VALUES('"+ new_fruit +"')")
        my_cnx.commit()
    return "Thanks for adding " + new_fruit

def get_fruit_load_list(my_cnx):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        result = my_cur.fetchall()
    return result

# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

# Text input field for entering a new fruit
new_fruit = streamlit.text_input("Enter a new fruit:")

# Button to insert a new fruit
if streamlit.button('Add Fruit') and new_fruit:
    insert_row_snowflake(new_fruit)

# Add predefined fruits to the list
predefined_fruits = ["jackfruit", "papaya", "guava", "kiwi"]
for fruit in predefined_fruits:
    insert_row_snowflake(fruit)

###########################################################################



# import streamlit
# import snowflake.connector

# streamlit.header('View Our Fruit List - Add Your Favorites')

# # Allow the end user to add a fruit to the list
# def insert_row_snowflake(new_fruit):
#     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#     with my_cnx.cursor() as my_cur:
#         my_cur.execute("INSERT INTO fruit_load_list VALUES (?)", (new_fruit,))
#         my_cnx.commit()
#     my_cnx.close()
#     return "Thanks for adding " + new_fruit

# # Add a button to load the fruit
# if streamlit.button('Get Fruit List'):
#     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#     my_data_rows = get_fruit_load_list()
#     my_cnx.close()
#     streamlit.dataframe(my_data_rows)

# # Button to insert a new fruit
# if streamlit.button('Add Fruit'):
#     new_fruit = streamlit.text_input("Enter a fruit:")
#     if new_fruit:
#         insert_row_snowflake(new_fruit)

# # Add predefined fruits to the list
# predefined_fruits = ["jackfruit", "papaya", "guava", "kiwi"]
# for fruit in predefined_fruits:
#     insert_row_snowflake(fruit)
