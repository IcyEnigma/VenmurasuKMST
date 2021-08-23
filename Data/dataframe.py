# This code uses our drive folder. You have to change path for making the dataframe.
import os # Importing the os library
file_dir = "/content/drive/MyDrive/PSG/Semester 3/Venmurasu Final" # Getting the working directory
file_list = os.listdir(file_dir) # Getting a list of files
file_list.sort() # Sorting the files in ascending order
x = file_list[:20] # Ignoring the other folders in the folder
data = {} # Empty dictionary
for file1 in x:
  key1 = file1[2:5] # Getting the language of the file
  if key1 not in list(data.keys()): # For key occurring first time
    current_file = load_file("/content/drive/MyDrive/PSG/Semester 3/Venmurasu Final/" + file1)
    data[key1] = [x for x in current_file.split("\n\n")] # List of lines in the language
  # Code if key already exists
  current_file = load_file("/content/drive/MyDrive/PSG/Semester 3/Venmurasu Final/" + file1)
  text = current_file.split("\n\n")
  for line in text:
    data[key1].append(line) # Keep appending lines of the same language in one list
import pandas as pd # Get the Pandas library
df = pd.DataFrame(data) # Make the dataframe
