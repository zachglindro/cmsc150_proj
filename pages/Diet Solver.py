import streamlit as st
import pandas as pd
import simplex.solver as solver

st.set_page_config(page_title="Diet Solver", page_icon=":cooking:")
st.title("Diet Solver")

constraints, raw_data = solver.read_data()

foods = raw_data.index.tolist()
default = ['Frozen Broccoli',
            'Carrots,Raw',
            'Celery, Raw',
            'Frozen Corn',
            'Lettuce,Iceberg,Raw',
            'Roasted Chicken',
            'Potatoes, Baked',
            'Tofu',
            'Peppers, Sweet, Raw',
            'Spaghetti W/ Sauce',
            'Tomato,Red,Ripe,Raw',
            'Apple,Raw,W/Skin',
            'Banana',
            'Grapes',
            'Kiwifruit,Raw,Fresh',
            'Oranges',
            'Bagels',
            'Wheat Bread',
            'White Bread',
            'Oatmeal Cookies']

foods_to_include = st.multiselect("Select foods to include in diet", foods, default=default)

augcoeffmatrix = solver.solve(foods_to_include)

with st.expander("View raw data"):
    raw_data
    constraints