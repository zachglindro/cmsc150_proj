import numpy as np
import pandas as pd

# Generate augmented coefficient matrix for polynomial regression
def generate_augcoeffmatrix(data, order):
    augcoeffmatrix = pd.DataFrame(np.zeros((order + 1, order + 2)))

    x = data.iloc[:, 0]
    y = data.iloc[:, 1]

    # Fill LHS of augcoeffmatrix
    for i in range(order + 1):
        for j in range(order + 1):
            augcoeffmatrix.iloc[i, j] = sum(x**(i+j))

    # Fill RHS of augcoeffmatrix
    for i in range(order + 1):
        augcoeffmatrix.iloc[i, -1] = sum(y * x**i)

    return augcoeffmatrix

# Performs Gauss-Jordan elimination on a dataframe
def gauss_jordan(df):
    for i in range(len(df.index)):
        # Divide row by pivot
        df.iloc[i] /= df.iloc[i, i]

        # Subtract row from other rows
        for j in range(len(df.index)):
            if i != j:
                df.iloc[j] -= df.iloc[i] * df.iloc[j, i]

    return df

# Creates function for polynomial regression based on augcoeffmatrix
def create_function(df):
    function_parts = [f"{df.iloc[i, -1]}*(x**{i})" for i in range(len(df.index))]
    function = 'lambda x: ' + ' + '.join(function_parts)
    return function

def regression(text, sep, order):
    data = pd.read_csv(text, sep=sep, header=None)
    augcoeffmatrix = generate_augcoeffmatrix(data, order)
    augcoeffmatrix = gauss_jordan(augcoeffmatrix)

    f = eval(create_function(augcoeffmatrix))
    return f
