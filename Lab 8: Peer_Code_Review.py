# Lab 8: Peer Code Review # 10/18/2026
# Odelia Asher # oasher@usf.edu #
####################################

"""
This is a debugged peer's script from the previous Lab 7: Linear Regression Assignment,
that allows a user to choose a dataset and select X and Y variables that are used to
create a scatterplot and an OLS regression line.

This script was improved by adding a command line interface for plot formatting, and
expanding graphing capabilities to graph two dependent variables against the same
independent variable on the same plot.

"""

# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Prompt user for dataset and load dataset
csv_path = input("Please enter the dataset filename: ")
df = pd.read_csv(csv_path)

# Clean column names to lowercase and replaces spaces with underscores
df.columns = df.columns.str.lower().str.replace(" ", "_")

# List available columns
print("Columns:")
print(df.columns.to_list())

# Prompt user for X and variables
x_col = input("Enter X variable column name: ")
y_col = input ("Enter Y variable column name: ")

# Prompt user for optional second dependent variable
def second_y_variable():
    while True:
        y_choice = input("Would you like to enter a second Y variable y/n:")

        if y_choice == "y":
            second_y_col = input("Enter second Y variable column name:")
            return second_y_col

        elif y_choice == "n":
            return None

        else:
            print ("Invalid input. Please enter 'y' or 'n'")

second_y_col = second_y_variable() # This stores the user's selection

# Define the dependent variable columns
y_cols = [y_col]

if second_y_col is not None:
    y_cols.append(second_y_col)

# Remove missing rows from X or Y columns
data = df[[x_col] + y_cols].dropna()

# Removes commas and convert values to numbers
for col in [x_col] + y_cols:
    if data[col].astype(str).str.contains(",",na=False).any():
        data[col]=pd.to_numeric(data[col].astype(str).str.replace(",", "",regex=False))

# Command line interface that allows the user to format scatterplot
print ("Plot formatting selection" )

plot_color = input ("Enter preferred scatterplot color:").strip()
opacity = float(input ('Enter preferred opacity between 0 and 1: '))
line_color= input("Enter preferred regression line color:").strip()
line_width = float(input("Enter preferred regression line width:"))
gridlines = input ("Display gridlines? (T/F): ").strip().upper()
custom_title = input("Enter custom plot title:").strip()

# Restrict the user's formatting input to prevent errors
if not 0<= opacity <= 1:
    raise ValueError("Opacity value must be between 0 and 1")
if line_width <= 0:
    raise ValueError("Line width value must be greater than 0")
if gridlines not in ["T", "F"]:
    raise ValueError("Gridlines value must be either 'T' or 'F'")

show_gridlines = gridlines == "T"

# Create plain scatterplot
fig, ax = plt.subplots(figsize = (8, 6))

for y in y_cols:
    ax.scatter(
        data[x_col],
        data[y],
        color = plot_color,
        alpha = opacity,
        edgecolor = "k",
        linewidth =0.3,
    )

ax.set_xlabel(x_col)

if len(y_cols) == 1:
    ax.set_ylabel (y_cols[0])
    ax.set_title (custom_title)
else:
    ax.set_ylabel(y_col[0])
    ax.set_title(custom_title)

ax.grid(show_gridlines, alpha=0.3)
fig.tight_layout()

# Ask user if they want to save the plain scatterplot
save_plain = input("Would you like to save this scatterplot? (y/n): ")
if save_plain == "y":
    scatter_file = input("Enter custom filename: ")
    fig.savefig(scatter_file, dpi = 300)
    print(f"Saved scatterplot -> {scatter_file}")

elif save_plain == "n":
    print ("Scatter plot not saved")


# Calculate OLS regression line and print OLS regression line on scatterplot
x_line = np.linspace(data[x_col].min(), data[x_col].max(), 100)
X = sm.add_constant(data[x_col])

for y in y_cols:
    model = sm.OLS(data[y], X).fit()
    y_line = model.params["const"] + model.params[x_col] * x_line
    ax.plot(
        x_line,
        y_line,
        color= line_color,
        linewidth = line_width,
        label = f"OLS line (R^2 = {model.rsquared:.3f})")

ax.set_title(custom_title)
ax.legend()

# Ask user if they want to save the OLS scatterplot
save_ols = input("Would you like to save this scatterplot with OLS regression line? (y/n): ")
if save_ols == "y":
    ols_file = input("Enter custom filename: ")
    fig.savefig(ols_file, dpi=300)
    print(f"Saved scatterplot with OLS line -> {ols_file}")

elif save_ols == "n":
    print ("Scatter plot with OLS regression line not saved")

# Display OLS regression line
plt.show()


