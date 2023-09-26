
# from https://stackoverflow.com/a/42010728

import pandas as pd
file_name = "res/term_library/term_library.csv"
file_name_output = "res/term_library/term_library_unique.csv"

df = pd.read_csv(file_name, sep=",")

# Notes:
# - the `subset=None` means that every column is used 
#    to determine if two rows are different; to change that specify
#    the columns as an array
# - the `inplace=True` means that the data structure is changed and
#   the duplicate rows are gone  

df.drop_duplicates(subset=['term'], inplace=True) # we use term here

# perform string changes to all terms, replacing underscores and getting terms individually
df['term'] = df['term'].str.lower().str.replace('_',' ')

# Write the results to a different file
df.to_csv(file_name_output, index=False)