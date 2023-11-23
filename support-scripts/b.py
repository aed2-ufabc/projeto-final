import pandas as pd

def sort_and_save_csv(input_file, output_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file, header=None)

    # Sort the DataFrame by the first column in descending order
    df = df.sort_values(by=df.columns[0], ascending=True)

    # Remove line breaks from the second column
    df.iloc[:, 1] = df.iloc[:, 1].replace('\n', ' ', regex=True)

    # Save the sorted DataFrame to a new CSV file
    df.to_csv(output_file, index=False, header=False)

    print(f"Sorted data saved to {output_file}")

# Replace 'input_file.csv' and 'output_file_sorted.csv' with the actual file paths
input_file = './files/remote1/a.csv'
output_file = 'output_file_sorted.csv'

remotes = ['remote4']
letters = ['ñ']

for remote in remotes:
    for l in letters:
        sort_and_save_csv('./files/'+remote+'/'+l+'.csv', './files/'+remote+'/'+l+'.csv')
