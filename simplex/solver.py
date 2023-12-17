import pandas as pd
pd.set_option('display.max_columns', None)

# Takes in normal maximization matrix
def maximize(df, max_iterations = 5000):
    df = df.astype(float)
    i = 0

    while df.iloc[-1].lt(0).any() and i < max_iterations:
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
def minimize(df, max_iterations = 5000):
    df = df.reset_index(drop=True)

    # Add variable names
    df.columns = [f's{i}' for i in range(1, len(df.columns))] + ['rhs']

    # Add slack variables
    for i in range(1, len(df.index)):
        df.insert(len(df.columns)-1, f'x{i}', 0)
    df.insert(len(df.columns)-1, 'z', 0)

    # Make last row negative
    df.iloc[-1] = df.iloc[-1] * -1

    # Add 1s diagonally to the slack variables, move the z coefficient to proper place
    for i in range(len(df.index)):
        df.iloc[i, len(df.columns)-len(df.index)-1+i] = 1
    df.iloc[-1, -1] = 0

    return maximize(df, max_iterations)

# Read constraints.tsv
constraints = pd.read_csv('constraints.tsv', sep='\t', index_col=0)

# Read food_data.tsv
raw_data = pd.read_csv('food_data.tsv', sep='\t', index_col=0)

# Remove $ from Price/Serving
raw_data['Price/Serving'] = raw_data['Price/Serving'].str.replace('$', '').astype(float)

test_data = raw_data.loc[['Frozen Broccoli',
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
                          'Oatmeal Cookies'], :]

# Remove Serving Size column because it's not needed for simplex
test_data = test_data.drop(columns=['Serving Size'])

# Swap Price/Serving and last column because Price is what we're minimizing
test_data = test_data[[c for c in test_data.columns if c != 'Price/Serving'] + ['Price/Serving']]

# Add the minimum and maximum constraints for the nutrients in the last row
negatives = test_data.copy().multiply(-1).iloc[:, :-1].add_suffix('_max')
test_data = pd.concat([negatives, test_data], axis=1)

min = pd.DataFrame(constraints['Min']).transpose().reset_index(drop=True)
max = pd.DataFrame(constraints['Max']).transpose().multiply(-1).reset_index(drop=True).add_suffix('_max')
cons = pd.concat([max,min], axis=1)

test_data = pd.concat([test_data, cons], axis=0)
test_data.iloc[-1, -1] = 0

# Each food has max 10 serving. Add this constraint
num_rows, num_cols = test_data.shape

# Insert rows for max serving constraint
for i in range(num_rows - 1):
    before_last_column = len(test_data.columns) - 1
    test_data.insert(before_last_column, f'max_{i}', 0)


for i in range(num_rows - 1):
    # Set -1s diagonally for max serving constraint
    test_data.iloc[i, len(test_data.columns)-len(test_data.index)-1+i+1] = -1

    # Set bottom row to -10 for max serving constraint
    test_data.iloc[len(test_data.index)-1, len(test_data.columns)-len(test_data.index)-1+i+1] = -10


solved = minimize(test_data)
print(solved)