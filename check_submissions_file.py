import pandas as pd
import glob

# create an empty list to store unique values
unique_ids = []

# get a list of all csv files in the folder
csv_files = glob.glob('aw_posts/*.csv')

# loop through each csv file and extract unique ids
for file in csv_files:
    # read csv file into a pandas dataframe
    df = pd.read_csv(file)
    # extract the 'id' column and add to unique_ids list
    unique_ids.extend(df['id'].unique())
    print(len(df['id']))

# convert unique_ids list to a set to remove duplicates
unique_ids = list(set(unique_ids))

# print the unique ids
print(len(unique_ids))
