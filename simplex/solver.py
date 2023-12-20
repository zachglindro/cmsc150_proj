import pandas as pd
pd.set_option('display.max_columns', None)

history = []

# Takes in normal maximization matrix
def maximize(df, max_iterations = 5000):
    history.clear()
    df = df.astype(float)
    i = 0

    while df.iloc[-1].lt(0).any() and i < max_iterations:
        history.append(df.copy())

        # Select pivot column
        pivot_column = df.iloc[-1].idxmin()

        # Select pivot row
        ratios = df.iloc[:, -1] / df.loc[:, pivot_column]
        ratios = ratios[:-1]

        if ratios.le(0).all():
            return 404

        pivot_row = ratios[ratios.gt(0)].idxmin()

        # Normalize pivot row
        df.loc[pivot_row] /= df.loc[pivot_row, pivot_column]

        # Clear pivot column
        for row in df.index:
            if row != pivot_row:
                df.loc[row] -= df.loc[row, pivot_column] * df.loc[pivot_row]

        i += 1
    
    return df

# Takes in matrix post-transposition
# 1:n-1 columns are constraints
# nth column is the original objective function
# form: ax=b
def minimize(df, list_of_food_names, max_iterations = 5000):
    df = df.reset_index(drop=True)

    # Label last row index to "Answer"
    df.index = df.index[:-1].tolist() + ['Answer']

    # Add variable names
    df.columns = list(df.columns[:-1]) + ['Price/Serving']

    # Add slack variables
    column_names = list_of_food_names + ['z']
    for column_name in column_names:
        df.insert(len(df.columns)-1, column_name, 0)

    # Make last row negative
    df.iloc[-1] = df.iloc[-1] * -1

    # Add 1s diagonally to the slack variables, move the z coefficient to proper place
    for i in range(len(df.index)):
        df.iloc[i, len(df.columns)-len(df.index)-1+i] = 1
    df.iloc[-1, -1] = 0

    return maximize(df, max_iterations)

# Read data from constraints.tsv and food_data.tsv
def read_data():
    constraints = pd.read_csv('simplex/constraints.tsv', sep='\t', index_col=0)
    raw_data = pd.read_csv('simplex/food_data.tsv', sep='\t', index_col=0)

    # Remove $ from Price/Serving
    raw_data['Price/Serving'] = raw_data['Price/Serving'].str.replace('$', '').astype(float)

    return constraints, raw_data

# Get list of foods from food_data.tsv
def get_foods():
    raw_data = pd.read_csv('simplex/food_data.tsv', sep='\t', index_col=0)
    return raw_data.index.tolist()

# Master function. Needs correct list of food names
def solve(list_of_food_names):
    constraints, raw_data = read_data()
    data = raw_data.loc[list_of_food_names, :]

    # Drop Serving Size column because it's not needed for simplex
    data = data.drop(columns=['Serving Size'])

    # Swap Price/Serving and last column because Price is what we're minimizing
    data = data[[c for c in data.columns if c != 'Price/Serving'] + ['Price/Serving']]

    # Add the minimum and maximum constraints for the nutrients in the last row
    negatives = data.copy().multiply(-1).iloc[:, :-1].add_suffix('_max')
    data = pd.concat([negatives, data], axis=1)

    min = pd.DataFrame(constraints['Min']).transpose().reset_index(drop=True)
    max = pd.DataFrame(constraints['Max']).transpose().multiply(-1).reset_index(drop=True).add_suffix('_max')
    cons = pd.concat([max,min], axis=1)

    data = pd.concat([data, cons], axis=0)
    data.iloc[-1, -1] = 0

    # Each food has max 10 serving. Add this constraint
    num_rows, num_cols = data.shape

    # Insert rows for max serving constraint
    for i in range(num_rows - 1):
        before_last_column = len(data.columns) - 1
        data.insert(before_last_column, f'max_of_{list_of_food_names[i]}', 0)

    for i in range(num_rows - 1):
        # Set -1s diagonally for max serving constraint
        data.iloc[i, len(data.columns)-len(data.index)-1+i+1] = -1

        # Set bottom row to -10 for max serving constraint
        data.iloc[len(data.index)-1, len(data.columns)-len(data.index)-1+i+1] = -10

    # Do minimization
    solved = minimize(data, list_of_food_names)

    return solved