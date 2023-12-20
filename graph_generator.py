# graph_generator.py
# Author: jdmremi
# Requires python 3.9.13 to be installed, as well as the matplotlib library.
# matplotlib can be installed by running 'pip3 install matplotlib'

# When the program runs, you will be asked to give the FULL path to your data set. E.g C:\Users\User\Documents\GENESYS30Data on Windows (or wherever your files are located).
# On Mac, the format is generally /users/User/Documents/Desktop/GENESYS30Data, or again, wherever your files are located.

# If done correctly, it should display the amount of files that are in that directory.
# Next, the program will visit each file. It will print out the max absorption and wavelength recorded, and print that out so that you know which trial belongs to each file.
# It will also print the name of the file.

# Choose a good name to name the file - e.g "Universal Indicator pH 7 Trial 1", because this will also be the title on the graph.
# Steps repeat for every file.
# Files will output to the GENESYS30Data/images directory

import csv
import os
import matplotlib.pyplot as plt

# Reads the csv from a file and returns it as a list.
def read_csv_values(path: str):
    with open(path, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
        return data[7:]
    
# Returns the maximum absorbance and wavelength in a given file
def get_max_absorption_and_wavelength(data: str):
    max_value = float('-inf')
    max_value_row = None
    for row in data:
        if len(row) >= 2:  # Ensure the row has at least two columns
            column2_data = float(row[1])  # Assuming column index starts from 0
            if column2_data > max_value:
                max_value = column2_data
                max_value_row = row

    return max_value_row

def main():
    file_directory = input("Enter the path containing lab data (This should be the GENESYS30Data) directory: ")

    files_list = [f"{file_directory}/{f}" for f in os.listdir(file_directory) if f.endswith(".csv")]

    # Create the output directory if it doesn't exist.
    if not os.path.exists(f"{file_directory}/images"):
        os.mkdir(f"{file_directory}/images")

    num_files = len(files_list)

    print(f"Found {num_files} file(s)")

    for file in files_list:
        rows = read_csv_values(file)
        max_absorption = get_max_absorption_and_wavelength(rows)

        print(f"Found file {file}. Max absorption: {max_absorption[1]} Wavelength: {max_absorption[0]}")
        graph_title_and_filename = input("What would you like to name this graph? ")
        
        wavelengths = [float(entry[0]) for entry in rows]
        absorbances = [float(entry[1]) for entry in rows]

        # Perform linear regression (optional):
        # slope, intercept, r_value, p_value, std_err = linregress(wavelengths, absorbances)
        # regression_line = [slope * x + intercept for x in wavelengths]

        # Creating the scatter plot
        plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
        plt.scatter(wavelengths, absorbances, c="blue", marker=".", alpha=0.7, label="Absorbance Data")
        # plt.plot(wavelengths, regression_line, color='red', label='Regression Line')    
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Absorbance")
        plt.legend()
        plt.title(f"{graph_title_and_filename} (Max absorption: {max_absorption[1]} at {max_absorption[0]}nm)")
        plt.savefig(f"{file_directory}/images/{graph_title_and_filename}.png")
        plt.close()

# Opcodes are `STORE_FAST` and not `STORE_GLOBAL` for functions so this may positively affect performance due to the amount of loops.
if __name__ == "__main__":
    main()