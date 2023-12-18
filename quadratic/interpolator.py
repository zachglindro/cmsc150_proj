import pandas as pd
import math as m

def gauss_jordan(df):
    for i in range(len(df.index)):
        # Divide row by pivot
        df.iloc[i] /= df.iloc[i, i]

        # Subtract row from other rows
        for j in range(len(df.index)):
            if i != j:
                df.iloc[j] -= df.iloc[i] * df.iloc[j, i]

    return df

def quadratic_interpolator(data):
    # Generate colnames
    colnames = [f'b{i}' for i in range(1, len(data.index))] + [f'c{i}' for i in range(2, len(data.index))] + ['rhs']
    
    # Generate matrix
    matrix = pd.DataFrame(columns=colnames)

    # rhs = f_n+1 - f_n
    matrix.iloc[:, -1] = data.iloc[1:, 1].values - data.iloc[:-1, 1].values

    # b_n = h_n (second condition: must be equal at the knots)
    for i in range(1, len(data.index)):
        matrix.loc[i-1, f'b{i}'] = data.iloc[i, 0] - data.iloc[i-1, 0]

    # c_n = (h_n)^2
    for i in range(1, len(data.index) - 1):
        matrix.loc[i, f'c{i+1}'] = (data.iloc[i+1, 0] - data.iloc[i, 0])**2

    # b_n + 2c_n*h_n - b_n+1 = 0 (continuity of derivatives)
    no_of_rows = len(matrix.index) - 1
    for i in range(1, len(data.index) - 1):
        matrix.loc[i+no_of_rows, f'b{i}'] = 1
        matrix.loc[i+no_of_rows, f'b{i+1}'] = -1

        if i == 1:
            continue

        matrix.loc[i+no_of_rows, f'c{i}'] = 2 * (data.iloc[i, 0] - data.iloc[i-1, 0])

    # fill nan values with 0
    matrix = matrix.fillna(0)

    # solve the augcoeffmatrix
    matrix = gauss_jordan(matrix)

    return matrix
    
# Creates functions for each interval
def create_functions(df):
    print(df)
    functions = []
    ranges = []

    # n-1 functions to be created
    for i in range(len(data.index) - 1):
        if i == 0:
            raw_lambda = f'lambda x: {data.iloc[i, 1]} + {df.iloc[i, -1]}*(x - {data.iloc[i, 0]})'
        else:
            raw_lambda = f'lambda x: {data.iloc[i, 1]} + {df.iloc[i, -1]}*(x - {data.iloc[i, 0]}) + {df.iloc[i+m.ceil(len(data.index)/2), -1]}*(x - {data.iloc[i,0]})**2'
        
        functions.append(eval(raw_lambda))

        raw_range_lambda = f'lambda x: {data.iloc[i,0]} <= x <= {data.iloc[i+1,0]}'
        print(raw_range_lambda)
        ranges.append(eval(raw_range_lambda))

    return functions, ranges

data = pd.read_csv('data.csv', sep='|')
data = data.sort_values(by='x')

solved = quadratic_interpolator(data)
functions, ranges = create_functions(solved)
print(ranges[0](3))