import streamlit as st
import pandas as pd
import numpy as np

import quadratic.interpolator as qi
import regression.regression as rr

st.title("CMSC 150 Tools")
st.caption("by Zach Dwayne M. Glindro, 2022-02014 AB4L")
st.write("Choose a tool from the sidebar.")

# set background to cat.gif in this directory
st.image("cat.gif")
st.caption("by blake s, https://www.artstation.com/artwork/03RRw4")