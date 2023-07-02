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

# Add a navbar
st.sidebar.title('Navigation')
navigation = st.sidebar.radio('Go to', ('Home', 'Weekly Meal Plan', 'BMI', 'Recipes', 'Search Ingredients', 'Recipe Details', 'Shopping List'))

if 'checked_ingredients' not in st.session_state:
    st.session_state.checked_ingredients = []  # Initialize the variable here

if navigation == 'Home':
    st.title('Welcome to Healthy Recipes!')
    st.write('This is a website designed to help you protect your health by finding nutritious recipes.')
    st.write('You can explore a variety of healthy recipes, view their nutrition information, and even check your BMI.')
    st.header('Home')

# Add buttons for navigation
col1, col2, col3, col4, col5, col6 = st.columns(6)
button_width = 100  # Set the width for all buttons

with col1:
    st.write(
        """
        <style>
        .custom-button-green {
            width: 100%;
            background-color: green;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button('Weekly Meal Plan', key='weekly_meal_plan_button', help='Weekly Meal Plan', args={'class': 'custom-button-green'}):
        navigation = 'Weekly Meal Plan'

with col2:
    st.write(
        """
        <style>
        .custom-button-green {
            width: 100%;
            background-color: green;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button('BMI', key='bmi_button', help='BMI', args={'class': 'custom-button-green'}):
        navigation = 'BMI'

with col3:
    st.write(
        """
        <style>
        .custom-button-green {
            width: 100%;
            background-color: green;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button('Recipes', key='recipes_button', help='Recipes', args={'class': 'custom-button-green'}):
        navigation = 'Recipes'

with col4:
    st.write(
        """
        <style>
        .custom-button-green {
            width: 100%;
            background-color: green;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button('Search Ingredients', key='search_ingredients_button', help='Search Ingredients', args={'class': 'custom-button-green'}):
        navigation = 'Search Ingredients'

with col5:
    st.write(
        """
        <style>
        .custom-button-green {
            width: 100%;
            background-color: green;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button('Recipe Details', key='recipe_details_button', help='Recipe Details', args={'class': 'custom-button-green'}):
        navigation = 'Recipe Details'

with col6:
    st.write(
        """
        <style>
        .custom-button-green {
            width: 100%;
            background-color: green;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button('Shopping List', key='shopping_list_button', help='Shopping List', args={'class': 'custom-button-green'}):
        navigation = 'Shopping List'


if navigation == 'BMI':
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
    st.header('Recipes')
    page = st.number_input('Page', min_value=1, step=1, value=1)
    start_idx = (page - 1) * 100
    end_idx = start_idx + 100
    recipes_df = df.iloc[start_idx:end_idx]
    selected_recipe = st.selectbox('Select a recipe:', [''] + recipes_df['name'].tolist())
    if selected_recipe:
        navigation = 'Recipe Details'
        name = selected_recipe

if navigation == 'Search Ingredients':
    st.header('Search Ingredients')
    ingredient = st.text_input('Enter an ingredient:')
    if ingredient:
        filtered_data = filter_recipes_by_ingredient(ingredient)
        if filtered_data.empty:
            st.write('No recipes found with this ingredient.')
        else:
            st.dataframe(filtered_data)

if navigation == 'Recipe Details':
    st.header('Recipe Details')
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
        checked_ingredients = st.multiselect('Select ingredients:', ingredients_list, default=st.session_state.checked_ingredients)
        st.session_state.checked_ingredients = checked_ingredients
        st.write('Checked Ingredients:', checked_ingredients)