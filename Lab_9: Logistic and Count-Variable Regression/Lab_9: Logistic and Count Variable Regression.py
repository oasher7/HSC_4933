###############################################
# Odelia Asher # oasher@usf.edu # 10/25/2026
#----------------------------------------------
# HSC 4933: Python for Health Analytics
# Lab 9: Logistic and Count Variable Regression
################################################

"""
This script performs logistic and count-variable
regression modeling using a user-selected dataset and columns.
"""

# Import libraries
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from statsmodels.api import add_constant

# Prompt user for custom dataset
print ("Available datasets: ")
print ("1. birthwt.csv")
print ("2. places_2025.csv")

dataset = input ("Please select the dataset you would like to use:")

# Load entered dataset
if dataset == "1":
    CSV_PATH = "../birthwt.csv"
    df = pd.read_csv (CSV_PATH)
elif dataset == "2":
    CSV_PATH = "../places_2025.csv"
    df = pd. read_csv(CSV_PATH)
else:
    print ("Dataset not available")
    exit()

# Clean column names to 'snake case' format
df.columns = df.columns.str.lower().str.replace(' ', '_')

# List available column names
print ("Dataset column names: ")
columns = list (df.columns)
midpoint = (len(columns)+1)//2

for i in range (midpoint):
    left = columns [i]
    right = columns [i+midpoint] if i + midpoint < len(columns) else ""
    print (f"{left:<30}{right}")

# Prompt user for column names they want as predictors
print ("If entering multiple columns, separate by commas.")
predictors = [
    col.strip().lower()
    for col in input ("Please enter the column name(s) you would like to use as predictor(s): ").split(",")
            ]

# Prompt user for a column name they want as a response variable
response_var = input ("Please select the column name you would like to use as a response variable: ").strip().lower()

features =df[predictors + [response_var]].copy()

# Remove commas and convert values to numbers
for col in predictors + [response_var]:
    features[col] = pd.to_numeric(features[col].astype(str).str.replace(",","",regex = False),errors="coerce")

# Remove rows missing any of the values for regression
features = features.dropna()

x = features [predictors]
y = features[response_var]

# Prompt user for regression model selection
print ("Regression models:")
print ("1. Logistic Regression")
print ("2. Count-variable (Poisson) Regression")

regression = input ("Please enter which regression you would like to run:")

# Calculate logistic regression
if regression == "1":
    # Split into 80% training and 20% testing
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Initialize the Logistic Regression model
    model = LogisticRegression (solver= 'lbfgs', max_iter=1000)
    model.fit(x_train,y_train) # Train (fit) the model using training data

    # Calculate McFadden's pseudo R-squared using training data
    x_train_sm = sm.add_constant(x_train)
    logit_model = sm.Logit (y_train, x_train_sm).fit(disp=0)
    pseudo_r2 = logit_model.prsquared
    print (f"McFadden's Pseudo R-squared: {pseudo_r2:.4f}")

    # Make predictions on the test set
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)

    print (f"Model Accuracy: {accuracy:.2%}")
    print (classification_report(y_test, y_pred))

    # Compute confusion matrix array
    cm = confusion_matrix (y_test, y_pred)

    # Display the formatted matrix cleanly with default labels (0 and 1)
    disp = ConfusionMatrixDisplay (confusion_matrix=cm,display_labels=model.classes_)
    disp.plot()



# Calculate count-variable regression
elif regression == "2":
    df_scaled = features.copy()

    for col in predictors:
        df_scaled[col] = ((df_scaled[col] - df_scaled[col].mean()) / df_scaled[col].std())

    # Calculate and display VIF
    x_vif = add_constant (df_scaled[predictors])
    vif_df = pd.DataFrame()
    vif_df["Feature"] = x_vif.columns
    vif_df["VIF"] = [variance_inflation_factor(x_vif.values, i) for i in range(x_vif.shape[1])]
    print (vif_df.to_string(index=False))
    print ("-" * 40)

    # Create formula
    formula = response_var + " ~ " + " + ".join(predictors)

    # Run model
    print ("Fitting model...")
    model = smf.poisson(formula, data=df_scaled).fit()

    # Print model summary
    print(model.summary())

# Ask user if they would like to save the output to a .txt file
save_model = input ("Would you like to save your output to a .txt file? y/n:")

if save_model == "y":
    txt_file_name = input ("Please enter the file name you would like to save to:").strip().lower()
    txt_file = f"{txt_file_name}.txt"

    with open (txt_file, "w") as file:
        file.write (f"Dataset: {CSV_PATH}\n")
        file.write (f"Predictors: {predictors}\n")
        file.write (f"Response variable: {response_var}\n")

        if regression == "1":
            file.write(f"McFadden's Pseudo R-squared: {pseudo_r2:.4f}\n")
            file.write (f"Model Accuracy: {accuracy:.2%}\n")
            file.write("\nClassification Report:\n")
            file.write (classification_report(y_test, y_pred))
            file.write("\nConfusion Matrix:\n")
            file.write(str(cm))
        elif regression == "2":
            file.write("\nVIF Results:\n")
            file.write(vif_df.to_string(index=False))
            file.write("\n\nModel Summary:\n")
            file.write(str(model.summary()))

    print (f"Saved to {txt_file_name}")

elif save_model == "n":
    print ("Model not saved")