import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

df = pd.read_csv('RAW_recipes.csv')

@st.cache_data
def get_recipe_data(name):
    recipe_data = df.loc[df['name'] == name]
    if recipe_data.empty:
        return None

    recipe = {
        'name': name,
        'minutes': recipe_data['minutes'].values[0],
        'tags': recipe_data['tags'].values[0],
        'nutrition': recipe_data['nutrition'].values[0],
        'steps': recipe_data['steps'].values[0],
        'description': recipe_data['description'].values[0],
        'ingredients': recipe_data['ingredients'].values[0],
    }

    return recipe

name = None

if 'checked_ingredients' not in st.session_state:
    st.session_state.checked_ingredients = []  # Initialize the variable here

if 'username' not in st.session_state:
    st.session_state.username = ''

# Add navbar
navigation = option_menu('Navigation', options=['Home', 'BMI', 'Recipes', 'Search Ingredients', 'Shopping List'], orientation="horizontal")

if st.session_state.username != '':
    st.header(f'Welcome to Plan your Meal, {st.session_state.username}!')
else:
    st.header('Welcome to Plan your Meal!')

# Use Streamlit container to stretch the navbar
with st.container():
    st.write('')
    st.write('')
    st.write(navigation)

st.write('Here you can find recipes and create an individual weekly plan. You can also determine your BMI and search for recipes based on ingredients. Then have a shopping list generated for you.')

st.header('Home')

st.text_input('Please enter your name', key='username')

# Display images
st.subheader('Featured Recipes')
col1, col2, col3 = st.columns(3)
with col1:
    st.image('amerikanische-pancakes.jpg', use_column_width=True, caption='Amerikanische Pancakes')
with col2:
    st.image('Teriyaki-chicken-bowls-8.jpg', use_column_width=True, caption='Teriyaki Chicken Bowls')
with col3:
    st.image('How-To-Make-Banana-Ice-Cream-071220172061.jpg.webp', use_column_width=True, caption='Banana Ice Cream')

if navigation == 'BMI':
    if st.session_state.username != '':
        st.header(f'BMI Calculator for {st.session_state.username}')
    else:
        st.header('BMI Calculator')

    st.write('Please enter your weight and height to calculate your BMI.')
    weight = st.number_input('Weight (in kg)')
    height = st.number_input('Height (in meters)')
    if weight > 0 and height > 0:
        bmi = calculate_bmi(weight, height)
        st.write('Your BMI:', bmi)
        st.write('Interpretation:')
        if bmi < 18.5:
            st.write('Underweight')
        elif 18.5 <= bmi < 25:
            st.write('Normal weight')

if navigation == 'Recipes':
    if st.session_state.username != '':
        st.header(f'Recipes for {st.session_state.username}')
    else:
        st.header('Recipes')

    page = st.number_input('Page', min_value=1, step=1, value=1)
    start_idx = (page - 1) * 100
    end_idx = start_idx + 100
    st.dataframe(df.iloc[start_idx:end_idx])

if navigation == 'Search Ingredients':
    if st.session_state.username != '':
        st.header(f'Search Ingredients for {st.session_state.username}')
    else:
        st.header('Search Ingredients')

    ingredient = st.text_input('Enter an ingredient')
    if st.button('Search'):
        filtered_data = filter_recipes_by_ingredient(ingredient)
        st.dataframe(filtered_data)

if navigation == 'Shopping List':
    if st.session_state.username != '':
        st.header(f'Shopping List for {st.session_state.username}')
    else:
        st.header('Shopping List')

    st.write('Here you can create your shopping list by selecting ingredients from the recipes.')

    recipe_name = st.selectbox('Select a recipe', df['name'])
    recipe = get_recipe_data(recipe_name)

    if recipe:
        st.write('Recipe:', recipe['name'])
        st.write('Ingredients:', recipe['ingredients'])
        if st.button('Add to shopping list'):
            st.session_state.checked_ingredients.append(recipe['ingredients'])
            st.success('Added to shopping list!')
        if st.button('Clear shopping list'):
            st.session_state.checked_ingredients = []
            st.success('Shopping list cleared!')
    else:
        st.warning('No recipe selected.')

    if len(st.session_state.checked_ingredients) > 0:
        st.subheader('Shopping List')
        for ingredients in st.session_state.checked_ingredients:
            st.write(ingredients)
    else:
        st.warning('Your shopping list is empty.')
