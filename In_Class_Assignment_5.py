#########################################################
# In Class Assignment 5 # Linear Regression
# -------------------------------------------------------
# Odelia Asher # HSC4933 # oasher@usf.edu # 10/7/26
##########################################################

"""
This script creates scatterplot and performs linear
regression for a given dataset, saving outputs as png files
and returning regression stats.
"""

# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Environment variables
CSV_PATH = "Blood_Pressure_clean.csv"
X_COL = "sys_mmhg"
Y_COL = "dias_mmhg"

# Load csv and perform sanity check
df = pd.read_csv(CSV_PATH)
data = df[[X_COL, Y_COL]].dropna()

# Create scatterplot
fig,ax = plt.subplots(figsize=(8,6))
ax.scatter(data[X_COL],data[Y_COL],alpha=0.6, edgecolors="k", linewidth=0.3)
ax.set_xlabel(X_COL)
ax.set_ylabel(Y_COL)
ax.set_title(f"{Y_COL} vs. {X_COL} (n={len(data)})")
ax.grid(alpha=0.3)
fig.tight_layout()

# Save scaterplot
scatter_file = f"{X_COL}_vs_{Y_COL}_scatter.png"
fig.savefig(scatter_file, dpi=300)
print(f"Saved scatterplot -> {scatter_file}")

# Perform linear regression
X = sm.add_constant(data[X_COL])
model = sm.OLS(data[Y_COL], X).fit()

# Print regression summary
print ("OLS Regression Summary: ")
print (model.summary())

# Make new scatterplot with regression table
x_line = np.linspace(data[X_COL].min(), data[X_COL].max(), 100)
y_line = model.params["const"] + model.params [X_COL] * x_line
ax.plot(x_line, y_line, color="crimson", linewidth=2, label=f"OLS line (R²= {model.rsquared:.3f})")
ax.set_title(f"{Y_COL} vs. {X_COL} with OLS line(n={len(data)})")
ax.legend ()

# Save new scatterplot
ols_file = f"{X_COL}_vs{Y_COL}_ols.png"
fig.savefig (ols_file, dpi=300)
print(f"Saved scatterplot with OLS line -> {ols_file}")

# Display OLS regression
plt.show()
