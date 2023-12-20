import streamlit as st
import pandas as pd
import numpy as np
import regression.regression as rr
import matplotlib.pyplot as plt

def regress(text, x, order):
    # Check if order is non-negative
    if order <= 0:
        st.error("Order must be positive.")
        return

    # Get the regression function
    f = rr.regression(text, ',', order)

    # Display in format f(x) = ... while removing lambda and x for printing in GUI
    readable_function = f.replace('lambda x: ', '').replace('**', '^').replace('*', '')

    # Get x, y points
    x_points = []
    y_points = []


    for line in text.splitlines():
        line = line.split(',')
        x_points.append(float(line[0]))
        y_points.append(float(line[1]))

    # Check if there are at least 2 unique points
    if len(set(x_points)) < 2:
        st.error("Give at least 2 unique points.")
        return

    # Check if order is valid
    if order >= len(set(x_points)):
        st.error(f"Order is too high, since you only have {len(set(x_points))} unique x points. Try adding more points, or set order to {len(set(x_points))-1} or lower.")
        return
    
    st.text(f"Estimated value of f({x}) = {eval(f)(x)}")

    # Plot points
    plt.scatter(x_points, y_points)

    fig, ax = plt.subplots()
    ax.scatter(x_points, y_points)

    # Plot regression line
    x_line = np.linspace(min(x_points), max(x_points), 1000)
    y_line = eval(f)(x_line)
    
    ax.plot(x_line, y_line)

    st.pyplot(fig)

    st.write(f"Regression function: f(x) = {readable_function}")
    

st.set_page_config(page_title="Polynomial Regression", page_icon=":bar_chart:")
st.title("Polynomial Regression")

text = st.text_area("Input x,y data here (separated by commas)", value="50,3.3\n50,2.8\n50,2.9\n70,2.3\n70,2.6\n70,2.1\n80,2.5\n80,2.9\n80,2.4\n90,3.0\n90,3.1\n90,2.8\n100,3.3\n100,3.5\n100,3.0")
x = st.number_input("Input x value to estimate", value=60.0000, format="%.4f", step=0.0001)
order = st.number_input("Input order of polynomial", value=2)
# TODO: use slider?

try:
    regress(text, x, order)
except:
    st.write("Invalid input.")