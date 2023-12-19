import streamlit as st
import pandas as pd
import numpy as np
import quadratic.interpolator as qi

# TODO: does not work w/ 3 points
def interpolate(text, x):
    functions, ranges = qi.interpolateWithText(text)

    if x < ranges[0][0] or x > ranges[-1][1]:
        st.write("x is out of range.")
        return
    
    for i in range(len(ranges)):
        if ranges[i][0] <= x <= ranges[i][1]:
            st.text(f"Using function {i+1}, estimated value of f({x}) = {eval(functions[i])(x)}")
            break

    for i in range(len(functions)):
        st.text(f"Function {i+1} over {ranges[i]}:")

        # Display in format s_i(x) = ... while removing lambda and x
        func = functions[i].replace('lambda x: ', '').replace('**', '^').replace('*', '')
        st.latex(f's_{{{i+1}}}(x) = {func}')

    x = []
    y = []

    for i in range(len(functions)):
        func = eval(functions[i])

        x.append(np.linspace(ranges[i][0], ranges[i][1], 1000))
        y.append(func(x[i]))

    x = np.concatenate(x)
    y = np.concatenate(y)

    st.line_chart(pd.DataFrame({'x': x, 'y': y}), x='x', y='y')
    st.caption("Graph of the splines")

st.set_page_config(page_title="Quadratic Spline Interpolation", page_icon="chart_with_upwards_trend:")
st.title("Quadratic Spline Interpolation")

text = st.text_area("Input x, y data here (separated by commas)", value="3,2.5\n4.5,1\n7,2.5\n9,0.5")
x = st.number_input("Input x value to estimate", value=5.5000)
    
try:
    interpolate(text, x)
except:
    st.write("Invalid input.")
