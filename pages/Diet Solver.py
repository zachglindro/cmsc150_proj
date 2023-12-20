import streamlit as st
import pandas as pd
import simplex.solver as solver

# Gets the basic solution from the augmented coefficient matrix
def get_answer_table(augcoeffmatrix, foods_to_include, raw_data, show_all_foods=False):
    answer = pd.DataFrame(index=foods_to_include + ["Total"], columns=["Amount", "Serving Size", "Cost ($) per day"], data=0)
    
    for food in foods_to_include:
        answer.loc[food, "Amount"] = augcoeffmatrix.loc["Answer", food]
        answer.loc[food, "Serving Size"] = raw_data.loc[food, "Serving Size"]
        answer.loc[food, "Cost"] = raw_data.loc[food, "Price/Serving"] * augcoeffmatrix.loc["Answer", food]
    
    # Remove foods with 0 amount
    if not show_all_foods:
        answer = answer[answer["Amount"] != 0]

    answer.loc["Total", "Cost"] = answer["Cost"].sum()
    return answer

def start():
    # Get constraints and food data
    constraints, raw_data = solver.read_data()
    foods = raw_data.index.tolist()

     # Ask user to input which foods to include for the solver
    container = st.container()
    preset = st.radio(label="Or choose a preset", options=["All foods", "Test case"], index=None)

    test_case = ['Frozen Broccoli',
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

    # Choose preset if user clicks on one
    if preset == "All foods":
        foods_to_include = container.multiselect("Select foods to include in diet", foods, default=foods)
    elif preset == "Test case":
        foods_to_include = container.multiselect("Select foods to include in diet", foods, default=test_case)
    else:
        foods_to_include = container.multiselect("Select foods to include in diet", foods)

    # Get the final augcoeffmatrix
    augcoeffmatrix = None
    history = None
    if st.button("Solve"):
        if len(foods_to_include) == 0:
            st.error("Please select at least one food!")
            return

        bar = st.progress(0, text="Solving...")
        augcoeffmatrix = solver.solve(foods_to_include)

        # Check if no solution found
        if type(augcoeffmatrix) == int:
            bar.progress(0, text="No solution found.")
            return

        answer = get_answer_table(augcoeffmatrix, foods_to_include, raw_data)
        bar.progress(100, text="Solved!")

    # Print the answer table
    if augcoeffmatrix is not None:
        st.write("Optimized menu")
        st.dataframe(answer)

        with st.expander("Guts!"):
            history = solver.history
            for i in range(len(history)):
                st.write(f"Iteration {i}")
                st.write(history[i])
                st.write("")

                st.dataframe(get_answer_table(history[i], foods_to_include, raw_data, show_all_foods=True))

            st.write("Final augmented coefficient matrix")
            st.dataframe(get_answer_table(augcoeffmatrix, foods_to_include, raw_data, show_all_foods=True))
            augcoeffmatrix

    # Display raw data and constraints
    with st.expander("View raw data"):
        raw_data
        constraints

st.set_page_config(page_title="Diet Solver", page_icon=":cooking:")
st.title("Diet Solver")
start()

