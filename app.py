import streamlit as st
import pandas as pd

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

def filter_recipes_by_ingredient(ingredient):
    filtered_data = df[df['ingredients'].str.contains(ingredient, case=False, na=False)]
    return filtered_data

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi

name = None



# Add a navbar
st.sidebar.title('Navigation')
navigation = st.sidebar.radio('Go to', ('Home', 'Weekly Meal Plan', 'BMI', 'Recipes', 'Search Ingredients', 'Recipe Details', 'Shopping List'))

if 'checked_ingredients' not in st.session_state:
    st.session_state.checked_ingredients = []  # Initialize the variable here

if 'username' not in st.session_state:
    st.session_state.username = ''

if navigation == 'Home':
    st.title('Welcome to Plan your Meal!')
    st.write('Here you can find recipes and create an individual weekly plan. You can also determine your BMI and search for recipes based on ingredients. Then have a shopping list generated for you.')

    st.header('Home')

    st.text_input('Please enter your name ', key='username')

    # Add buttons for navigation
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        if st.button('Weekly Meal Plan'):
            navigation = 'Weekly Meal Plan'
    with col2:
        if st.button('BMI'):
            navigation = 'BMI'
    with col3:
        if st.button('Recipes'):
            navigation = 'Recipes'
    with col4:
        if st.button('Search Ingredients'):
            navigation = 'Search Ingredients'
    with col5:
        if st.button('Recipe Details'):
            navigation = 'Recipe Details'
    with col6:
        if st.button('Shopping List'):
            navigation = 'Shopping List'

# Füge die Bilder nebeneinander hinzu
col1, col2, col3 = st.columns(3)
with col1:
    st.image('amerikanische-pancakes.jpg', use_column_width=True, caption='Amerikanische Pancakes')
with col2:
    st.image('Teriyaki-chicken-bowls-8.jpg', use_column_width=True, caption='Teriyaki Chicken Bowls')
with col3:
    st.image('Vanilla-Peanut-Butter-and-Banana-Ice-Cream.600-500x500.jpg', use_column_width=True, caption='Vanilla Peanut Butter and Banana Ice Cream')


if navigation == 'BMI':


    if st.session_state.username != '' :
        st.header('BMI Calculator for '  + st.session_state.username)
        st.session_state['username'] = st.session_state.username
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
        elif 25 <= bmi < 30:
            st.write('Overweight')
        else:
            st.write('Obese')

if navigation == 'Recipes':

    if st.session_state.username !='' :
        st.header('Recipes for '  + st.session_state.username)
        st.session_state['username'] = st.session_state.username
    else:
        st.header('Recipes')

    page = st.number_input('Page', min_value=1, step=1, value=1)
    start_idx = (page - 1) * 100
    end_idx = start_idx + 100
    st.dataframe(df.iloc[start_idx:end_idx])

if navigation == 'Search Ingredients':

    if st.session_state.username !='' :
        st.header('Search Ingredients for '  + st.session_state.username)
        st.session_state['username'] = st.session_state.username
    else:
        st.header('Search Ingredients')

    ingredient = st.text_input('Enter an ingredient:')
    if ingredient:
        filtered_data = filter_recipes_by_ingredient(ingredient)
        if filtered_data.empty:
            st.write('No recipes found with this ingredient.')
        else:
            st.dataframe(filtered_data)

if navigation == 'Recipe Details':


    if st.session_state.username !='' :
        st.header('Recipe Details for '  + st.session_state.username)
        st.session_state['username'] = st.session_state.username
    else:
        st.header('Recipe Details')


    name = st.text_input('Enter the recipe name:')
    if name:
        recipe = get_recipe_data(name)
        if recipe is None:
            st.write('Recipe not found.')
        else:
            st.write('Name:', recipe['name'])
            st.write('Minutes:', recipe['minutes'])
            st.write('Tags:', recipe['tags'])
            st.write('Nutrition:', recipe['nutrition'])
            st.write('Steps:', recipe['steps'])
            st.write('Description:', recipe['description'])
            st.write('Ingredients:', recipe['ingredients'])

if navigation == 'Shopping List':

    if st.session_state.username != '':
        st.header('Shopping List for '  + st.session_state.username)
        st.session_state['username'] = st.session_state.username
    else:
        st.header('Shopping List')

    selected_recipes = st.multiselect('Select recipes:', df['name'].tolist())
    if selected_recipes:
        ingredients_list = []
        for recipe_name in selected_recipes:
            recipe = get_recipe_data(recipe_name)
            if recipe is not None:
                ingredients = recipe['ingredients']
                ingredients_list.extend(ingredients.split(','))
        ingredients_list = [ingredient.strip() for ingredient in ingredients_list]
        ingredients_list = list(set(ingredients_list))  # Remove duplicates
        checked_ingredients = st.multiselect('Check off ingredients:', ingredients_list, format_func=lambda x: f"[x] {x}" if x in st.session_state.checked_ingredients else f"[ ] {x}")
        st.write('Generated Shopping List:')
        for ingredient in ingredients_list:
            if ingredient in checked_ingredients:
                st.write('- [x] ' + ingredient)
            else:
                st.write('- [ ] ' + ingredient)
    else:
        st.write('No recipes selected. Please choose at least one recipe to generate the shopping list.')

if navigation == 'Weekly Meal Plan':


    if st.session_state.username != '' :
        st.header('Weekly Meal Plan for '  + st.session_state.username)
        st.session_state['username'] = st.session_state.username
    else:
        st.header('Weekly Meal Plan')

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    selected_recipes = {}
    for day in days_of_week:
        recipe_name = st.selectbox(f'Select a recipe for {day}:', [''] + df['name'].tolist(), key=f'recipe_{day}')
        selected_recipes[day] = recipe_name
    st.write('Selected Recipes:')
    for day, recipe_name in selected_recipes.items():
        st.subheader(day)
        if recipe_name:
            recipe = get_recipe_data(recipe_name)
            if recipe is None:
                st.write('Recipe not found.')
            else:
                st.write('Name:', recipe['name'])
                st.write('Minutes:', recipe['minutes'])
                st.write('Tags:', recipe['tags'])
                st.write('Nutrition:', recipe['nutrition'])
                st.write('Steps:', recipe['steps'])
                st.write('Description:', recipe['description'])
                st.write('Ingredients:', recipe['ingredients'])
        else:
            st.write('No recipe selected for this day.')

# Custom CSS styles
st.write(
    """
    <style>
    body {
        background-color: #c6e6c6;
    }
    .stButton button.custom-button-green {
        background-color: green;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #c6e6c6;
        border-color: green;
        color: green;
    }
    .stNumberInput>div>div>input {
        background-color: #c6e6c6;
        border-color: green;
        color: green;
    }
    .stDataFrame>div>div>div>div>table {
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
