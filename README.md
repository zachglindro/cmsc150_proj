# CMSC 150 Tools
Includes diet solver, polynomial regression, and quadratic spline interpolation tools.
![app](https://github.com/zdmgg/cmsc150_proj/assets/66626397/170b5844-d9d7-4367-9d24-10fb5b0c7eaa)

## Features
### Diet solver
- Choose from a selection of foods
- Minimize cost while still keeping in line with nutrient and calorie requirements

### Regression
- Performs polynomial regression on a given set of points
- Estimates a desired value based on the calulated model and desired order for the polynomial

### Interpolation
- Creates splines for interpolation based on a given set of points
- Estimates a desired value based on the calculated model

Also, cat.

## Requirements
Tested on Python 3.10.12.

Check [the Python website](https://www.python.org/downloads/) for installation (or for apt users, `sudo apt update && sudo apt install python3`).

## Installation
Install the program and its requisite packages using
```
git clone https://github.com/zdmgg/cmsc150_proj
cd cmsc150_proj
pip install -r requirements.txt
```

Run the program using streamlit:
```
streamlit run Start.py
```

The website can also be accessed at [glindro150.streamlit.app](https://glindro150.streamlit.app)

## Usage
After running `streamlit run Start.py` or accessing the website, the tools should load shortly on your browser.

### Diet solver
- Select foods using the multichooser, or select one using the presets located below.
- Click Solve! The app will let you know whether or not it is able to meet the required amount of nutrients.

![could_not_solve](https://github.com/zdmgg/cmsc150_proj/assets/66626397/e149b2ee-f378-4b32-9b0a-869bec699eef)

- If the app successfully creates a menu, it will show it in a table, containing the suggested amount of servings and their cost.

![image](https://github.com/zdmgg/cmsc150_proj/assets/66626397/8526a791-2644-4392-8e12-e983aef88c5e)

- Advanced: Guts! shows the iterations, augcoeffmatrix, and basic solutions using the augcoeffmatrix. The raw data for the constraints and the food table can be viewed in "View raw data."

### Quadratic spline interpolation
- Input your data in the first text area in x,y format. The first value will be used as the x-coordinate of the point, while the second will be used as the y-coordinate.
- Next, input the value to be interpolated. This value must be within the range of your data. The app will let you know if it isn't.

![qsi_outofrange](https://github.com/zdmgg/cmsc150_proj/assets/66626397/bc026afd-27a9-42ca-9429-f916c41c9ab1)

- If all inputs are valid, the app will output the functions used for each interval, the interpolated value, and a graph of the splines.

![qsi_valid](https://github.com/zdmgg/cmsc150_proj/assets/66626397/4489f5ba-c689-4f45-8557-e67c30bb35f2)


### Regression
- Input your data in the first text area in x,y format. The first value will be used as the x-coordinate of the point, while the second will be used as the y-coordinate.
- Next, input the value to be predicted and the order of the regression function. The order must be positive and less than the number of unique x-coordinates in your data. The app will let you know if it isn't.
- If all inputs are valid, the app will output the predicted value, the graph of the points with the trendline, and the regression function used.

![regression](https://github.com/zdmgg/cmsc150_proj/assets/66626397/84dbd023-b345-46e8-9e0c-bd1166bc90cf)


Also, ฅ^._.^ฅ

## Customization
The UI subfiles are located in /pages.
The data for the diet solver are located in /simplex, named constraints.tsv and food_data.tsv. These are files with tab-separated values; the app otherwise won't work if these files aren't in the folder, or the columns/rows are modified.
