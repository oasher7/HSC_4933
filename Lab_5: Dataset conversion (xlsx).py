###############################################
# Lab 5: Dataset Conversion #
#---------------------------------------------#
# Odelia Asher # oasher@usf.edu # 10/04/2026
###############################################

""" This script converts a csv dataset to xlsx
and ensured that there are no duplicate columns
"""

# Import libraries
import pandas as pd

# Open the .csv file
df = pd.read_csv("Maternal Health Risk Data Set.csv")

# Look for duplicate columns and drop them
df= df.drop (columns = [c for i, c in enumerate (df.columns)
                        if df.columns.duplicated (keep=False)[i]])

# Save the dataset as a .xlsx
df.to_excel("Maternal Health Risk Data Set.xlsx",
            index=False, header=True)