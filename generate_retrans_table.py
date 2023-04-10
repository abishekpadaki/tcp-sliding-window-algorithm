import pandas as pd

# open the text file
with open("txt_files/retransmissions.txt", "r") as file:
    # read all lines of the file
    lines = file.readlines()

# create an empty dictionary to store the data
data = {}

# loop through each line of the file
for line in lines:
    # split the line into two columns using comma as separator
    columns = line.strip().split(",")
    value = columns[0]
    count = int(columns[1])
    # add the value to the dictionary with the count as key
    if count in data:
        data[count].append(value)
    else:
        data[count] = [value]

# create a new dictionary with the values separated by commas
new_data = {"# of Retransmissions": [], "# of Packets": []}
for count, values in data.items():
    new_data["# of Retransmissions"].append(count)
    new_data["# of Packets"].append(len(values))

# create a DataFrame using the new dictionary
df = pd.DataFrame(new_data)

# print the DataFrame
print(df)
