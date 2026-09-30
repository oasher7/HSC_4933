#########################################################
# In Class Assignment 4 # Pandas and Numpy Data Cleaning
#########################################################
# Odelia Asher # oasher@usf.edu # 09/30/26
##########################################################

""" This script utilizes panda and numpy to manipulate data,
parses data to clean datasets for analysis, and differentiates use cases
for numpy and pandas in data manipulation
"""

# Imports
import pandas as pd
import numpy as np

# Load csv
df = pd.read_csv ("eye_health.csv")

# Print csv stats before cleaning
print (df.shape,
       df.dtypes,
       df.isna().sum(), # Print total number of NaN values
       df.nunique(),
       sep = "\n")

# Print number of duplicated values
print ("Duplicates: ", df.duplicated().sum())

df =  df.dropna(axis=1, how="all") # Drop columns with no data (only NaN)
df = df.drop(columns = [c for c in df.columns if c.endswith("ID")]) # Drop columns that end in "ID"

df = df.dropna(subset=["Data_Value"]) # Drop rows with no value in the column "Data_Value"
df = df.drop(columns = ["Geolocation", "Data_Value_Footnote_Symbol",\
                        "Data_Value_Footnote", "StateAbbr", "NonWeightedSample", "Geographic Level", "Numerator"])

df.columns = df.columns.str.lower().str.replace(" ","_") # Make column header snake_case

# Create new column "ci_width" and calculate margin of error
df["error"] = (df["high_confidence_limit"] - df["low_confidence_limit"]) / 2

# Create prevalence level descriptor
df["prevalence_level"] = np.select ([df["data_value"] < 5, df["data_value"] <= 7],\
                                    ["Low","Medium"],"High")

df.to_csv("eye_health_2022_clean.csv", index = False) # Save to csv the different name
print (pd.read_csv("eye_health_2022_clean.csv").shape == df.shape) # Print t/f if dimensions mathc
print (pd.read_csv("eye_health_2022_clean.csv").shape) # Print saved file dimensions
print (pd.read_csv("eye_health_2022_clean.csv").head) # Print dataframe head (first 5 lines)