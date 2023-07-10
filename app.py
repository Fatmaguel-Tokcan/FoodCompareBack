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

# Use Streamlit container to stretch the navbar
with st.container():
    st.write('')
    st.write('')
    st.write(navigation)

# Rest of the code
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

    def calculate_bmi(weight, height):
        bmi = weight / (height ** 2)
        return round(bmi, 2)

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

# Add feedback button at the bottom of the page
st.markdown(
    """
    <style>
    .feedback-btn-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
    }
    .feedback-btn-container button {
        background-color: blue;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="feedback-btn-container">
        <button onclick="document.getElementById('feedback-modal').style.display = 'block'"">Feedback</button>
    </div>
    """,
    unsafe_allow_html=True
)

# Add feedback modal
st.markdown(
    """
    <div class="feedback-btn-container">
        <button onclick="document.getElementById('feedback-modal').style.display = 'block'"">Feedback</button>
    </div>
    """,
    unsafe_allow_html=True
)