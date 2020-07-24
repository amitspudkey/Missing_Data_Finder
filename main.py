import pandas as pd
from file_handling import *
from selection import *
from functions import *


print("Program: Missing Data Finder")
print("Release: 0.0.1")
print("Date: 2020-07-23")
print("Author: Brian Neely")
print()
print()
print("This program takes a csv and will look for missing data within a specified column or group of columns.")
print("Optionally, the complete data and data with missing values can be exported.")
print()
print()

# Find input file
file_in = select_file_in()

# Ask for delimination
delimination = input("Enter Deliminator: ")

# Open input csv using the unknown encoder function
data = open_unknown_csv(file_in, delimination)

# Create Column Header List
headers = list(data.columns.values)

# Get number of rows and columns
num_rows = data.shape[0]
num_columns = data.shape[1]

# Print number of rows
print("Number of rows: " + str(num_rows))
print("Number of Columns:" + str(num_columns))

# Select Column
columns = column_selection_multi(headers, "find missing data")

# Get index of all data
all_data_index = list(data.index)

# For each of the columns, print proportion of not missing and get list of indices with missing data
missing_data_index = list()
for i in columns:
    # Get rows without data
    rows_complete = data.dropna(subset=[i])

    # Print proportion of data without missing data
    num_rows_complete = rows_complete.shape[0]
    print("For Column [" + i + "]: " + str(num_rows - num_rows_complete) + " rows were missing data (" +
          str((num_rows - num_rows_complete) / num_rows * 100) + "%)")

    # Get index of complete data
    complete_index = list(rows_complete.index)

    # Get index of missing data
    missing_index = list_diff(all_data_index, complete_index)

    # Append to missing_data_index
    missing_data_index.append(missing_index)

# Flatten missing_data_index
missing_data_index_flat = [item for sublist in missing_data_index for item in sublist]

# Dedup missing_data_index_flat
missing_data_index_dedup = dedupe_list(missing_data_index_flat)

# Get list of complete data
complete_data_index = list_diff(all_data_index, missing_data_index_dedup)

# Print Results
print()
print(str(len(missing_data_index_dedup)) + " rows are missing atleast 1 data point in selected columns. (" +
      str(len(missing_data_index_dedup) / num_rows * 100) + "%)")

# Get complete data and export if desired
if y_n_question("Export rows with complete data (y/n): "):
    complete_data = data.iloc[complete_data_index]

    # Set output file
    file_out = select_file_out_csv(file_in)

    # Write CSV
    print("Writing CSV File...")
    complete_data.to_csv(file_out, index=False)
    print("Wrote CSV File!")
    print()

# Get missing data
if y_n_question("Export rows with missing data (y/n): "):
    missing_data = data.iloc[missing_data_index_dedup]

    # Set output file
    file_out = select_file_out_csv(file_in)

    # Write CSV
    print("Writing CSV File...")
    missing_data.to_csv(file_out, index=False)
    print("Wrote CSV File!")
    print()

print("Missing Data Finder Completed")
input("Press Enter to close...")
